#!/usr/bin/env python3
"""Generate the hierarchical analysis report from the claim tree (Rule 8).

Reported results are heavy summaries; validating and understanding them needs the
detail underneath. This walks `analysis/`, producing linked static HTML in which
each node's claim, answers, results and provenance are one click from its parent,
all the way down to the raw files.

The tree supplies the levels: root to node to fork to child, and at each node the
results it wrote, grouped by the combination that produced them where a stability
sweep has made more than one. **A project adds the levels below that** -- the
within-result detail: a reported mean broken out by the units it averages, down to
the per-item values everything above is an average of -- once it knows what its
results look like. Every such level must be displayed from a file the analysis
wrote, never recomputed here, so the report cannot disagree with the analysis
about a number.

Static HTML on purpose: it costs nothing to keep, needs no server, and will still
open in twenty years. It is generated from the tree, so its structure follows the
analysis rather than being maintained separately -- never hand-edit the output.

Two consumers. The agent, which reads stored detail instead of recomputing it or
inserting temporary debug output into working code. And the human, for whom
descending a structure by clicking is far faster than asking for it in a dialogue.

Dual interface:
    API:  build_report(root=".", out="AI-generated/hierarchical-report") -> Path
    CLI:  python build_hierarchical_report.py [--root .] [--out DIR] [--open]
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claims as claim_collection  # noqa: E402  — the sibling module, for Rule 9's side

CSS = """
:root { --fg:#1a1a1a; --muted:#666; --line:#ddd; --accent:#0b5; --warn:#b40; --bg:#fff; }
@media (prefers-color-scheme: dark) {
  :root { --fg:#e8e8e8; --muted:#999; --line:#333; --accent:#4d8; --warn:#f86; --bg:#161616; }
}
body { font: 15px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
       max-width: 52rem; margin: 2rem auto; padding: 0 1.2rem; color: var(--fg);
       background: var(--bg); }
h1 { font-size: 1.4rem; margin-bottom: .2rem; }
h2 { font-size: 1.05rem; margin-top: 1.8rem; border-bottom: 1px solid var(--line);
     padding-bottom: .3rem; }
h3 { font-size: .95rem; margin-top: 1.3rem; }
.claim { font-size: 1.05rem; margin: .6rem 0 1rem; }
.crumb, .meta { color: var(--muted); font-size: .85rem; }
.tag { display:inline-block; font-size:.72rem; padding:.1rem .45rem; border-radius:3px;
       border:1px solid var(--line); color:var(--muted); margin-left:.4rem; }
.main-path { border-color: var(--accent); color: var(--accent); }
.not-taken { border-color: var(--warn); color: var(--warn); }
ul { padding-left: 1.1rem; } li { margin: .25rem 0; }
a { color: inherit; } a:hover { color: var(--accent); }
pre { background: rgba(128,128,128,.1); padding: .7rem; overflow-x: auto; font-size: .82rem; }
.scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: .88rem; }
td, th { border-bottom: 1px solid var(--line); padding: .3rem .5rem; text-align: left;
         white-space: nowrap; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
tr.ours td { font-weight: 600; }
details { margin: .4rem 0; }
summary { cursor: pointer; color: var(--muted); font-size: .9rem; }
.claimblock { border-left: 2px solid var(--line); padding-left: .8rem; margin: .8rem 0; }
.claimblock .cid { font-weight: 600; }
"""

# --------------------------------------------------------------------------- tree


def _field(text: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", text, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    return None if v in ("", "-", "none", "n/a") else v


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*$", text, re.M)
    if not m:
        return ""
    nxt = re.compile(r"^## ", re.M).search(text, m.end())
    return text[m.end():nxt.start() if nxt else len(text)].strip()


def _read(node: Path) -> dict:
    text = (node / "claim.md").read_text()
    body = text.split("## Children")[0]
    claim = "\n".join(l for l in body.splitlines()
                      if l.strip() and not l.startswith("#")).strip()
    return {
        "path": node,
        "claim": claim,
        "kind": _field(text, "kind"),
        "main_path": _field(text, "main-path"),
        "answers": _section(text, "Answers"),
        "children": sorted(p for p in node.iterdir()
                           if p.is_dir() and (p / "claim.md").exists()),
    }


# Paths git ignores, collapsed to their topmost ignored directory. Filled once per
# build. A model's directory may acquire a built virtual environment and a `__pycache__`
# the first time an external runner executes it, and a node's `results/` may acquire a
# runner's scratch `work/` — none of which is the node's own material, and listing it
# would make a "Scripts" section thousands of files of somebody else's wheels. What the
# repository declines to version is exactly what this declines to show, so the two
# cannot drift apart.
_IGNORED: set[str] = set()


def _load_ignored(root: Path) -> set[str]:
    try:
        r = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--others", "--ignored",
             "--exclude-standard", "--directory"],
            capture_output=True, text=True)
    except FileNotFoundError:
        return set()
    return {line.rstrip("/") for line in r.stdout.splitlines() if line.strip()}


def _is_ignored(p: Path, root: Path) -> bool:
    if not _IGNORED:
        return False
    rel = p.relative_to(root)
    for i in range(len(rel.parts)):
        if "/".join(rel.parts[:i + 1]) in _IGNORED:
            return True
    return False


def _files(d: Path, root: Path | None = None) -> list[Path]:
    if not d.is_dir():
        return []
    out = [p for p in d.rglob("*") if p.is_file() and p.name != ".gitkeep"]
    if root is not None:
        out = [p for p in out if not _is_ignored(p, root)]
    return sorted(out)


def _claims_for(node_rel: str, all_claims: list[dict]) -> list[dict]:
    return [c for c in all_claims if c.get("node") == node_rel]


def _results_section(node: Path, root: Path, to_repo_root: str) -> list[str]:
    """A node's results, grouped by the combination that produced them.

    A flat listing is readable when there is one combination and is not when a
    stability sweep has made dozens: the reported analysis would be one row among many
    perturbations of it. `main` and its holdout twin are shown open; the rest fold.
    """
    rdir = node / "results"
    if not rdir.is_dir():
        return []
    loose = sorted(p for p in rdir.iterdir() if p.is_file() and p.name != ".gitkeep")
    combos = sorted(p for p in rdir.iterdir() if p.is_dir())
    if not loose and not combos:
        return []

    def listing(files: list[Path], base: Path) -> list[str]:
        out = ["<ul>"]
        for f in files:
            href = to_repo_root + f.relative_to(root).as_posix()
            out.append(f'<li><a href="{html.escape(href)}">'
                       f'{html.escape(f.relative_to(base).as_posix())}</a>'
                       f' <span class=meta>({f.stat().st_size:,} B)</span></li>')
        out.append("</ul>")
        return out

    parts = ["<h2>Results</h2>"]
    if loose:
        parts += listing(loose, rdir)
    lead = [c for c in combos if c.name in ("main", "main__holdout")]
    rest = [c for c in combos if c not in lead]
    for c in lead:
        parts.append(f"<h3>{html.escape(c.name)}</h3>")
        parts += listing(_files(c, root), c)
    if rest:
        parts.append(f"<details><summary>{len(rest)} other combination(s)</summary>")
        for c in rest:
            parts.append(f"<h3>{html.escape(c.name)}</h3>")
            parts += listing(_files(c, root), c)
        parts.append("</details>")
    return parts


def _page(root: Path, node: Path, out: Path, ancestors: list[str],
          all_claims: list[dict]) -> str:
    """Write one node's page. `ancestors` are the node names from the tree root down."""
    info = _read(node)
    rel = node.relative_to(root)
    page_dir = out / rel
    page_dir.mkdir(parents=True, exist_ok=True)
    page = page_dir / "index.html"
    depth = len(rel.parts)
    # Pages live at <root>/AI-generated/hierarchical-report/<rel>/index.html, so
    # reaching a file at <root>/<path> means climbing out of <rel>, then out of
    # hierarchical-report and AI-generated.
    to_repo_root = "../" * (depth + 2)

    parts = ["<!doctype html><meta charset=utf-8>",
             f"<title>{html.escape(node.name)}</title><style>{CSS}</style>"]

    if ancestors:
        trail = " / ".join(
            f'<a href="{"../" * (len(ancestors) - i)}index.html">{html.escape(n)}</a>'
            for i, n in enumerate(ancestors)
        )
        parts.append(f'<div class=crumb>{trail} / {html.escape(node.name)}</div>')
    parts.append(f"<h1>{html.escape(node.name)}</h1>")
    parts.append(f'<div class=claim>{html.escape(info["claim"])}</div>')

    if info["answers"] and not info["answers"].startswith("_("):
        parts.append("<h2>Answers</h2>")
        parts.append(f"<p>{html.escape(info['answers'])}</p>")

    mine = _claims_for(rel.as_posix(), all_claims)
    if mine:
        parts.append("<h2>Claims resting on this node</h2>")
        parts.append('<p class=meta>From the claim collection. Nothing enters the manuscript '
                     'that is not there.</p>')
        for c in mine:
            parts.append('<div class=claimblock>')
            parts.append(f'<span class=cid>{html.escape(c["id"])}</span> '
                         f'{html.escape(c["statement"])}')
            grounds = []
            for t in c.get("grounds", "").split("·"):
                t = t.strip().strip("`")
                if not t:
                    continue
                grounds.append(f'<a href="{html.escape(to_repo_root + t)}">'
                               f'{html.escape(Path(t).name)}</a>')
            if grounds:
                parts.append(f'<br><span class=meta>grounds: {" · ".join(grounds)}'
                             f' &nbsp;·&nbsp; {html.escape(c.get("by", "-"))}</span>')
            parts.append("</div>")

    if info["children"]:
        kind = info["kind"] or "?"
        parts.append(f"<h2>Children <span class=tag>{html.escape(kind)}</span></h2>")
        if kind == "alternatives":
            parts.append("<p class=meta>Only the main path is run by this node. "
                         "The others are run by the stability node.</p>")
        parts.append("<ul>")
        for c in info["children"]:
            ci = _read(c)
            tag = ""
            if kind == "alternatives":
                tag = (' <span class="tag main-path">main path</span>'
                       if c.name == info["main_path"]
                       else ' <span class="tag not-taken">not taken</span>')
            first = ci["claim"].splitlines()[0] if ci["claim"] else ""
            parts.append(f'<li><a href="{html.escape(c.name)}/index.html">'
                         f'{html.escape(c.name)}</a>{tag}<br>'
                         f'<span class=meta>{html.escape(first)}</span></li>')
        parts.append("</ul>")

    parts += _results_section(node, root, to_repo_root)

    for label, sub in (("Scripts", "scripts"), ("Provenance", "provenance")):
        files = _files(node / sub, root)
        if not files:
            continue
        parts.append(f"<h2>{label}</h2><ul>")
        for f in files:
            href = to_repo_root + f.relative_to(root).as_posix()
            size = f.stat().st_size
            parts.append(f'<li><a href="{html.escape(href)}">'
                         f'{html.escape(f.relative_to(node / sub).as_posix())}</a>'
                         f' <span class=meta>({size:,} B)</span></li>')
        parts.append("</ul>")

    run = node / "run.sh"
    if run.exists():
        parts.append("<h2>run.sh</h2>")
        parts.append(f"<pre>{html.escape(run.read_text())}</pre>")

    page.write_text("\n".join(parts))
    for c in info["children"]:
        _page(root, c, out, ancestors + [node.name], all_claims)
    return str(page)


def build_report(root: str | Path = ".", out: str | Path = "AI-generated/hierarchical-report") -> Path:
    root = Path(root).resolve()
    analysis = root / "analysis"
    if not (analysis / "claim.md").exists():
        raise SystemExit(f"no claim tree at {analysis}")
    out = root / out
    out.mkdir(parents=True, exist_ok=True)

    _IGNORED.clear()
    _IGNORED.update(_load_ignored(root))

    all_claims = claim_collection.load(root)
    _page(root, analysis, out, [], all_claims)

    try:
        commit = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True).stdout.strip() or "not committed"
    except FileNotFoundError:
        commit = "git unavailable"

    # The folder README is generated with the report for the same reason the report is:
    # a hand-kept description of a generated folder goes stale silently. `provenance.md`
    # beside it is not generated — it is the append-only record of each build, and it is
    # the one file here that is written by hand.
    (out / "README.md").write_text(
        "# hierarchical-report\n\n"
        "The linked drill-down over the claim tree (Rule 8). **Generated — never hand-edit.**\n"
        "Rebuild with `/hierarchical-report`, which runs\n"
        "`AI-internal/useful-scripts/build_hierarchical_report.py`.\n\n"
        f"Built {date.today().isoformat()} at commit {commit}. Open `index.html`.\n\n"
        "- `index.html` — the way into the tree.\n"
        "- `analysis/**/index.html` — one page per node: its claim, answers, the claims from\n"
        "  the collection that rest on it, its children with alternatives marked main-path or\n"
        "  not taken, its results grouped by combination, its scripts, its provenance records\n"
        "  and its `run.sh`.\n\n"
        "Every number shown is displayed from the file the analysis wrote; nothing here\n"
        "recomputes an aggregate, so the report cannot disagree with the analysis. Paths the\n"
        "repository does not version — built virtual environments, `__pycache__`, a runner's\n"
        "scratch `work/` — are not listed, because they are not the analysis's material.\n\n"
        "`provenance.md` is the exception to the no-hand-editing rule here: it is the record\n"
        "of each build, appended to and never overwritten.\n")

    index = out / "index.html"
    index.write_text(
        f"<!doctype html><meta charset=utf-8><title>Analysis report</title>"
        f"<style>{CSS}</style>"
        f"<h1>Analysis report</h1>"
        f"<p class=meta>Generated {date.today().isoformat()} at commit {html.escape(commit)}. "
        f"Regenerate with <code>/hierarchical-report</code>; never hand-edit.</p>"
        f"<h2>The tree</h2>"
        f'<p><a href="analysis/index.html">Enter the claim tree &rarr;</a> — every node&rsquo;s '
        f'claim, answers, results, scripts, provenance and <code>run.sh</code>, with the claims '
        f'that rest on it and the alternatives marked main-path or not taken.</p>'
    )
    return index


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="AI-generated/hierarchical-report")
    ap.add_argument("--open", action="store_true", help="open the report when done")
    a = ap.parse_args(argv)
    index = build_report(a.root, a.out)
    print(f"wrote {index}")
    if a.open:
        subprocess.run(["open", str(index)], check=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
