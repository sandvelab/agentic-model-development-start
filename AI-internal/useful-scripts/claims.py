#!/usr/bin/env python3
"""Maintain the claim collection — the bridge between results and text (Rule 9).

Writing is two steps: results -> claim collection -> manuscript. A claim is a short
statement the analysis supports, carrying an explicit pointer to the stored result
grounding it. Nothing is written into the manuscript that does not trace to a claim.

The collection lives in `Human-AI-collaboration/claims/claims.md`, one block per
claim:

    ## C7
    Region sets A and B co-occur more than expected under the uniform null.
    grounds: analysis/02_measure/a_jaccard/results/summary.tsv
    node: analysis/02_measure/a_jaccard
    scope: holds for the strict filtering convention only
    alternatives: the base-pair measure gives a weaker effect (see C9)
    by: agent-autonomous

`by:` is the agency field: human-set, agent-on-human-assessment, or agent-autonomous.

Dual interface:
    API:  load(root=".") -> list[dict]
          add(statement, grounds, node=None, **fields) -> str   # returns the new id
          audit(root=".") -> dict                               # resolution + coverage
    CLI:  python claims.py add "statement" --grounds path [--node path] [--by ...]
          python claims.py list [--node path]
          python claims.py audit
          python claims.py check-text <manuscript.md>
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

COLLECTION = Path("Human-AI-collaboration/claims/claims.md")
FIELDS = ("grounds", "node", "scope", "alternatives", "by")
AGENCY = ("human-set", "agent-on-human-assessment", "agent-autonomous")


def _path(root: str | Path) -> Path:
    return Path(root) / COLLECTION


def _strip_fences(text: str) -> str:
    """Drop fenced code blocks, so a format example in the file is not read as a claim."""
    return re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)


def load(root: str | Path = ".") -> list[dict]:
    p = _path(root)
    if not p.exists():
        return []
    claims: list[dict] = []
    for block in re.split(r"^## ", _strip_fences(p.read_text()), flags=re.M)[1:]:
        lines = block.strip().splitlines()
        if not lines:
            continue
        claim: dict = {"id": lines[0].strip(), "statement": "", "raw": "## " + block.rstrip()}
        statement: list[str] = []
        for line in lines[1:]:
            m = re.match(rf"^\s*({'|'.join(FIELDS)}):\s*(.*)$", line)
            if m:
                claim[m.group(1)] = m.group(2).strip()
            elif line.strip():
                statement.append(line.strip())
        claim["statement"] = " ".join(statement)
        claims.append(claim)
    return claims


def _next_id(claims: list[dict]) -> str:
    ns = [int(m.group(1)) for c in claims if (m := re.fullmatch(r"C(\d+)", c["id"]))]
    return f"C{max(ns) + 1 if ns else 1}"


def add(statement: str, grounds: str, root: str | Path = ".", **fields) -> str:
    p = _path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(
            "# Claim collection\n\nEverything the analysis supports, each statement bound to "
            "the result grounding it. The manuscript is written from this file; nothing enters "
            "the manuscript that is not here.\n"
        )
    claims = load(root)
    cid = _next_id(claims)
    by = fields.get("by")
    if by and by not in AGENCY:
        raise SystemExit(f"by: must be one of {AGENCY}")
    block = [f"\n## {cid}", statement.strip(), f"grounds: {grounds}"]
    for f in ("node", "scope", "alternatives", "by"):
        if fields.get(f):
            block.append(f"{f}: {fields[f]}")
    with p.open("a") as fh:
        fh.write("\n".join(block) + "\n")
    return cid


def audit(root: str | Path = ".") -> dict:
    root = Path(root)
    claims = load(root)
    unresolved, ungrounded, no_agency = [], [], []
    for c in claims:
        g = c.get("grounds")
        if not g:
            ungrounded.append(c["id"])
            continue
        for target in [t.strip().strip("`") for t in g.split("·")]:
            if target and not (root / target).exists():
                unresolved.append((c["id"], target))
        if not c.get("by"):
            no_agency.append(c["id"])

    # Which results are cited by no claim at all?
    cited = {t.strip().strip("`") for c in claims for t in c.get("grounds", "").split("·") if t.strip()}
    uncited = []
    for res in sorted((root / "analysis").rglob("results/*")):
        if res.is_dir() or res.name == ".gitkeep":
            continue
        rel = res.relative_to(root).as_posix()
        if rel not in cited:
            uncited.append(rel)
    return {
        "total": len(claims),
        "unresolved": unresolved,
        "ungrounded": ungrounded,
        "no_agency": no_agency,
        "uncited_results": uncited,
    }


def check_text(manuscript: str | Path, root: str | Path = ".") -> list[str]:
    """Retrospective audit: sentences in a draft with no matching claim.

    Deliberately crude — it matches on shared content words, and its job is to
    narrow where a human should look, not to decide. A flagged sentence is either
    unsupported or points at a claim that was never recorded; both are worth knowing.
    """
    claims = load(root)
    vocab = [set(re.findall(r"[a-z]{5,}", c["statement"].lower())) for c in claims]
    text = Path(manuscript).read_text()
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^#.*$", " ", text, flags=re.M)
    flagged = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        s = sentence.strip()
        if len(s.split()) < 6:
            continue
        words = set(re.findall(r"[a-z]{5,}", s.lower()))
        if not words:
            continue
        if not any(len(words & v) / len(words) > 0.25 for v in vocab if v):
            flagged.append(s)
    return flagged


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add")
    p.add_argument("statement")
    p.add_argument("--grounds", required=True, help="path(s) to the grounding result, ' · ' separated")
    p.add_argument("--node")
    p.add_argument("--scope")
    p.add_argument("--alternatives")
    p.add_argument("--by", choices=AGENCY)

    p = sub.add_parser("list")
    p.add_argument("--node")

    sub.add_parser("audit")

    p = sub.add_parser("check-text")
    p.add_argument("manuscript")

    a = ap.parse_args(argv)

    if a.cmd == "add":
        cid = add(a.statement, a.grounds, a.root, node=a.node, scope=a.scope,
                  alternatives=a.alternatives, by=a.by)
        print(f"added {cid}")
    elif a.cmd == "list":
        for c in load(a.root):
            if a.node and c.get("node") != a.node:
                continue
            print(f"{c['id']}: {c['statement']}")
            print(f"     grounds: {c.get('grounds', '-')}   by: {c.get('by', '-')}")
    elif a.cmd == "audit":
        r = audit(a.root)
        print(f"{r['total']} claim(s)")
        for label, items in (("unresolved grounds", r["unresolved"]),
                             ("claims with no grounds", r["ungrounded"]),
                             ("claims with no agency field", r["no_agency"]),
                             ("results cited by no claim", r["uncited_results"])):
            if items:
                print(f"\n{label} ({len(items)}):")
                for i in items:
                    print(f"  {i}")
        bad = r["unresolved"] or r["ungrounded"]
        print("\nEvery claim resolves." if not bad else "\nFix the unresolved claims.")
        return 1 if bad else 0
    elif a.cmd == "check-text":
        flagged = check_text(a.manuscript, a.root)
        if not flagged:
            print("Every sentence matches a claim.")
            return 0
        print(f"{len(flagged)} sentence(s) with no matching claim — check each:\n")
        for s in flagged:
            print(f"  - {s}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
