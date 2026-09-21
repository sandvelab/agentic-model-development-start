#!/usr/bin/env python3
"""Check the structural invariants the ten rules imply.

This is the part of the setup that does not depend on anyone remembering. An
instruction in AGENTS.md can be honoured for twenty steps and dropped at the
twenty-first without anything looking wrong; these checks have no attention
budget. Run at the end of every analysis and before every commit.

A failing check is fixed at the cause. Never weaken a check so it passes.

Checks
  tree        every node is well-formed; alternatives nodes have exactly one main
              path, store no scripts of their own, and call only that child;
              sub-analysis parents call every child; children are named for the
              relationship they stand in (numbered siblings, lettered alternatives)
  provenance  every file under a node's results/ has a provenance record, and every
              record names an existing script, commit and environment
  hashes      every file a record gives a sha256 for exists, and the record names that
              file's current digest somewhere -- so a script cannot change without a
              section being appended
  plots       every plot image has its plotted values and its plotting script beside it
  seeds       every script that draws randomness has a recorded seed
  claims      every claim in the collection resolves to an existing result
  git         the working tree is clean, and every commit a provenance record names is
              an ancestor of HEAD -- not merely an object that exists
  crossing    no result file looks like a value transcribed between steps by hand

Dual interface:
    API:  run_checks(root=".", only=None) -> list[Finding]
    CLI:  python check_invariants.py [--root .] [--only tree,plots] [--quiet]
          exits non-zero if anything failed
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PLOT_SUFFIXES = {".png", ".pdf", ".svg", ".jpg", ".jpeg"}
DATA_SUFFIXES = {".tsv", ".csv", ".txt", ".json", ".parquet"}
SCRIPT_SUFFIXES = {".py", ".R", ".r", ".sh", ".jl"}
RANDOM_HINTS = re.compile(
    r"\b(random|rand\(|randn|sample\(|shuffle|permut|np\.random|torch\.rand|"
    r"set\.seed|rng|Random\()", re.I
)
SEED_HINTS = re.compile(r"\b(seed|set_seed|manual_seed|set\.seed|SEED)\b")
# A node's scripts/ may hold a subdirectory of supporting material -- a model's contract
# directory, a vendored package -- and an external runner may build that model's
# environment *inside* it. A built environment is not a script of this node: it is
# generated, git ignores it, and its contents are third-party source. Walking into it
# would have this file reporting that numpy draws randomness without recording a seed,
# which is true and useless.
GENERATED = ("__pycache__", "site-packages", "node_modules")


def script_files(directory: Path) -> list[Path]:
    """Every script file a node owns, skipping generated and vendored trees."""
    if not directory.is_dir():
        return []
    return sorted(
        p for p in directory.rglob("*")
        if p.is_file() and p.suffix in SCRIPT_SUFFIXES
        and not any(part.startswith(".") or part in GENERATED
                    for part in p.relative_to(directory).parts)
    )


SUB_ANALYSIS_NAME = re.compile(r"^\d{2}_[A-Za-z]")
ALTERNATIVE_NAME = re.compile(r"^[a-z]_[A-Za-z]")


@dataclass
class Finding:
    check: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"[{self.check}] {self.path}: {self.message}"


def nodes(root: Path) -> list[Path]:
    return sorted(p.parent for p in (root / "analysis").rglob("claim.md"))


def _field(text: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", text, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    return None if v in ("", "-", "none", "n/a") else v


def check_tree(root: Path) -> list[Finding]:
    out: list[Finding] = []
    for node in nodes(root):
        rel = str(node.relative_to(root))
        run = node / "run.sh"
        if not run.exists():
            out.append(Finding("tree", rel, "no run.sh"))
            continue
        run_text = run.read_text()
        claim_text = (node / "claim.md").read_text()
        kids = sorted(p for p in node.iterdir() if p.is_dir() and (p / "claim.md").exists())
        if not kids:
            continue
        kind = _field(claim_text, "kind")
        if kind not in ("alternatives", "sub-analyses"):
            out.append(Finding("tree", rel, f"has children but kind is {kind!r}"))
            continue
        # AGENTS.md §8: a child's name carries the relationship it stands in.
        # Sub-analyses run in order and are numbered; alternatives are unordered and
        # mutually exclusive and are lettered. A number on an alternative asserts a
        # sequence that does not exist.
        wanted = ALTERNATIVE_NAME if kind == "alternatives" else SUB_ANALYSIS_NAME
        for k in kids:
            if not wanted.match(k.name):
                out.append(Finding(
                    "tree", f"{rel}/{k.name}",
                    f"child of a {kind} node should be named "
                    f"{'a_name, b_name (lettered)' if kind == 'alternatives' else 'NN_name (numbered)'}"))
        if kind == "alternatives":
            main = _field(claim_text, "main-path")
            names = [k.name for k in kids]
            if main not in names:
                out.append(Finding("tree", rel, f"main-path {main!r} not among {names}"))
                continue
            called = set(re.findall(r'bash "([^"/]+)/run\.sh"', run_text))
            if called != {main}:
                out.append(Finding(
                    "tree", rel,
                    f"alternatives node must call only the main path {main!r}, calls {sorted(called)}"))
            own = [p for p in (node / "scripts").glob("*") if p.name != ".gitkeep"] \
                if (node / "scripts").is_dir() else []
            if own:
                out.append(Finding(
                    "tree", rel,
                    f"alternatives node is a pure switch but stores {len(own)} script(s)"))
        else:
            called = set(re.findall(r'bash "([^"/]+)/run\.sh"', run_text))
            missing = {k.name for k in kids} - called
            if missing:
                out.append(Finding(
                    "tree", rel, f"sub-analyses node does not call {sorted(missing)}"))
    return out


def _provenance_records(node: Path) -> dict[str, str]:
    prov = node / "provenance"
    if not prov.is_dir():
        return {}
    return {p.name: p.read_text() for p in prov.glob("*.md")}


def check_provenance(root: Path) -> list[Finding]:
    out: list[Finding] = []
    for node in nodes(root):
        rel = str(node.relative_to(root))
        results = node / "results"
        if not results.is_dir():
            continue
        records = _provenance_records(node)
        blob = "\n".join(records.values())
        for f in sorted(results.rglob("*")):
            if f.is_dir() or f.name == ".gitkeep":
                continue
            name = f.relative_to(results).as_posix()
            # A project that runs the same script under several combinations (a
            # stability sweep) writes to `results/<combination>/`. One script produces
            # the same artefact under every combination, by the same invocation, so a
            # record may name the artefact by its combination-invariant path,
            # `results/$COMBO/<file>`, and cover every combination of it. The obligation
            # is unchanged: some record still has to name the artefact. Such a project
            # should also add a check that every combination directory is one its
            # manifest planned -- see AI-internal/skill-references/checks-to-add.md.
            head, _, tail = name.partition("/")
            aliases = [name]
            if tail:
                aliases += [f"$COMBO/{tail}", f"<combo>/{tail}"]
            if not any(alias in blob for alias in aliases):
                out.append(Finding("provenance", f"{rel}/results/{name}",
                                   "no provenance record names this result"))
        for rec_name, rec in records.items():
            for key in ("script:", "commit:", "environment:"):
                if key not in rec:
                    out.append(Finding("provenance", f"{rel}/provenance/{rec_name}",
                                       f"record is missing '{key}'"))
    return out


# A record's `script:` block names the files that produced the result and gives a sha256
# for each. Nothing makes those digests keep up with the files on its own, and the failure
# has one common shape: a batch appends its section when it runs the script, changes the
# script again later in the same batch, and does not append again. Nothing looks wrong
# afterwards, which is why this is code and not a resolution to be more careful. It is
# checked at the level of files rather than of `script:` lines, because a record may hash
# a shared library it imports as well as its own script, and the library changes too.
DIGEST = re.compile(r"sha256:([0-9a-f]{8,64})")
# The tokens a `script:` block is made of, matched in one pass so they come out in the order
# they appear and cannot overlap. `dir` is a heading like
# `the model itself, scripts/my_model/:`, which the bare filenames under it are relative
# to; `MLproject` is in the path alternative because some model runners' contracts require
# that name and it has no suffix to recognise it by.
RECORD_TOKEN = re.compile(
    r"(?P<digest>sha256:[0-9a-f]{8,64})"
    r"|(?P<dir>[\w./$-]+/(?=[:\s]|$))"
    r"|(?P<path>[\w./$-]*(?:\.(?:py|sh|R|r|jl|toml|lock|ya?ml|ipynb)|MLproject)\b)")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _script_blocks(text: str) -> list[str]:
    """Each `script:` field with the continuation lines that belong to it."""
    out, lines = [], text.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("script:"):
            continue
        block = [line]
        for nxt in lines[i + 1:]:
            if not nxt.strip() or nxt.startswith("```") or re.match(r"^[a-z-]+:", nxt):
                break
            block.append(nxt)
        out.append("\n".join(block))
    return out


def _hashed_files(block: str) -> list[tuple[str, str]]:
    """(directory, path) for each file the block names *and gives a digest for*.

    A path claims the digest that is the next token after it. If the next token is another
    path it carries no digest of its own -- `scripts/run_hier_nb.py   (unchanged)` followed
    by the model files that did change -- and nothing is claimed on its behalf. A record
    naming a library without hashing it is being less precise, not wrong, and is left alone.
    """
    tokens = [(m.lastgroup, m.group()) for m in RECORD_TOKEN.finditer(block)]
    out, directory = [], ""
    for j, (kind, value) in enumerate(tokens):
        if kind == "dir":
            directory = value
        elif kind == "path":
            following = tokens[j + 1] if j + 1 < len(tokens) else None
            if following and following[0] == "digest":
                out.append((directory, value))
    return out


def check_hashes(root: Path) -> list[Finding]:
    """Every file a record hashes exists, and the record names its current digest.

    Somewhere in the record, not in its newest section: an old section records the version
    that ran then and is right to keep it. The obligation is that the record has caught up
    with the file, not that it has forgotten what came before. An abbreviated digest --
    `sha256:cbd3158db12438ac...` -- satisfies it as a prefix, because abbreviating is a formatting choice and not a weaker claim.

    What this does not check, and it matters because this file is a large part of why the
    records are trusted: that a digest is paired with the run it sits beside, that a library
    a script imports is named at all, or that anything in the record is true. It narrows
    where a human has to look. It does not do the looking.
    """
    out: list[Finding] = []
    for node in nodes(root):
        rel = node.relative_to(root)
        for rec_name, rec in _provenance_records(node).items():
            where = f"{rel}/provenance/{rec_name}"
            recorded = DIGEST.findall(rec)
            seen: set[str] = set()
            for directory, named in (f for b in _script_blocks(rec)
                                     for f in _hashed_files(b)):
                if named in seen:
                    continue
                seen.add(named)
                candidates = [node / named, root / named]
                if directory:
                    candidates += [node / directory / named, root / directory / named]
                path = next((p for p in candidates if p.is_file()), None)
                if path is None:
                    out.append(Finding("hashes", where,
                                       f"gives a sha256 for '{named}', which is not a "
                                       f"file at this node or at the repository root"))
                    continue
                current = sha256_of(path)
                if not any(current.startswith(d) for d in recorded):
                    out.append(Finding("hashes", where, (
                        f"{path.relative_to(root)} now hashes to {current[:12]}…, which "
                        f"this record does not name: the file changed and no section was "
                        f"appended")))
    return out


def check_plots(root: Path) -> list[Finding]:
    out: list[Finding] = []
    for node in nodes(root):
        rel = str(node.relative_to(root))
        results = node / "results"
        if not results.is_dir():
            continue
        for f in sorted(results.rglob("*")):
            if f.suffix.lower() not in PLOT_SUFFIXES:
                continue
            stem = f.with_suffix("")
            has_data = any(stem.with_suffix(s).exists() for s in DATA_SUFFIXES)
            has_script = any(
                (node / "scripts" / f"{stem.name}{s}").exists() for s in SCRIPT_SUFFIXES
            ) or any(stem.with_suffix(s).exists() for s in SCRIPT_SUFFIXES)
            if not has_data:
                out.append(Finding("plots", f"{rel}/results/{f.name}",
                                   "no plotted-values file beside the figure"))
            if not has_script:
                out.append(Finding("plots", f"{rel}/results/{f.name}",
                                   "no plotting script for this figure"))
    return out


def check_seeds(root: Path) -> list[Finding]:
    out: list[Finding] = []
    for node in nodes(root):
        rel = str(node.relative_to(root))
        for s in script_files(node / "scripts"):
            text = s.read_text(errors="replace")
            if RANDOM_HINTS.search(text) and not SEED_HINTS.search(text):
                out.append(Finding(
                    "seeds", f"{rel}/scripts/{s.relative_to(node / 'scripts')}",
                    "draws randomness but records no seed"))
    return out


def check_claims(root: Path) -> list[Finding]:
    out: list[Finding] = []
    coll = root / "Human-AI-collaboration" / "claims" / "claims.md"
    if not coll.exists():
        return out
    # Drop fenced code blocks first: the collection documents its own format with an
    # example, and an example must not be checked as if it were a real claim.
    text = re.sub(r"^```.*?^```", "", coll.read_text(), flags=re.S | re.M)
    for m in re.finditer(r"^\s*[-*]?\s*grounds:\s*(.+)$", text, re.M):
        for target in [t.strip() for t in m.group(1).split("·")]:
            target = target.strip("`[] ")
            if not target or target.startswith("("):
                continue
            if not (root / target).exists():
                out.append(Finding("claims", target, "claim points at a result that does not exist"))
    return out


def check_git(root: Path) -> list[Finding]:
    out: list[Finding] = []
    if not (root / ".git").is_dir():
        return [Finding("git", ".", "not a git repository -- Rule 4 cannot be satisfied")]
    try:
        st = subprocess.run(["git", "-C", str(root), "status", "--porcelain"],
                            capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return [Finding("git", ".", f"could not run git: {e}")]
    if st:
        n = len(st.splitlines())
        out.append(Finding("git", ".", f"working tree not clean ({n} changed path(s))"))
    # Every hash on every `commit:` line, and each one has to be an ancestor of HEAD.
    #
    # Every hash on the line, because a record may annotate its hashes -- `commit: 9993d37
    # (the script), 3fb1280 (the inputs)` -- and a pattern anchored to one bare hash would
    # skip exactly the records that are being more informative.
    #
    # An ancestor of HEAD, not merely an object in the store: an object orphaned by a
    # rewritten commit is still in the store of the tree that rewrote it, and is still
    # copied by a *local* clone, so `cat-file -e` passes here and in every clone taken from
    # here. It would not survive a push. Ancestry is the property the record needs -- the
    # commit it names has to be one a reader can check out.
    for node in nodes(root):
        for rec_name, rec in _provenance_records(node).items():
            for line in re.findall(r"^commit:\s*(.+)$", rec, re.M):
                for sha in re.findall(r"\b[0-9a-f]{7,40}\b", line):
                    where = f"{node.relative_to(root)}/provenance/{rec_name}"
                    if subprocess.run(["git", "-C", str(root), "merge-base",
                                       "--is-ancestor", sha, "HEAD"],
                                      capture_output=True).returncode == 0:
                        continue
                    known = subprocess.run(["git", "-C", str(root), "cat-file", "-e",
                                            f"{sha}^{{commit}}"], capture_output=True)
                    out.append(Finding("git", where, (
                        f"recorded commit {sha} is not an ancestor of HEAD"
                        if known.returncode == 0 else
                        f"recorded commit {sha} does not exist")))
    return out


def check_crossing(root: Path) -> list[Finding]:
    """Heuristic for Rule 1's hardest failure: a value carried between steps by hand.

    A literal numeric constant sitting in a script with a comment naming another
    step is the visible symptom. Reported as a warning to look at, not a proof.

    The comment has to be on the constant's own line: a whitespace class would match
    newlines, and then a constant followed by a blank line and an unrelated paragraph of
    prose starting with one of the words below would be reported too. The separator is
    spaces and tabs only, so a trailing comment naming another step is caught and a
    docstring two lines further down is not.
    """
    out: list[Finding] = []
    pat = re.compile(r"^[ \t]*[A-Z_]{3,}[ \t]*=[ \t]*-?\d+\.?\d*[ \t]*#.*\b(from|per|see|step|output|above)\b",
                     re.M | re.I)
    for node in nodes(root):
        for s in script_files(node / "scripts"):
            for m in pat.finditer(s.read_text(errors="replace")):
                out.append(Finding("crossing", f"{node.relative_to(root)}/scripts/{s.name}",
                                   f"hard-coded value may have crossed a step by hand: "
                                   f"{m.group(0).strip()[:70]}"))
    return out


CHECKS = {
    "tree": check_tree,
    "provenance": check_provenance,
    "hashes": check_hashes,
    "plots": check_plots,
    "seeds": check_seeds,
    "claims": check_claims,
    "git": check_git,
    "crossing": check_crossing,
}


def run_checks(root: str | Path = ".", only: list[str] | None = None) -> list[Finding]:
    root = Path(root).resolve()
    names = only or list(CHECKS)
    findings: list[Finding] = []
    for n in names:
        if n not in CHECKS:
            raise SystemExit(f"unknown check: {n} (have {', '.join(CHECKS)})")
        findings.extend(CHECKS[n](root))
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--only", help="comma-separated subset of: " + ", ".join(CHECKS))
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    a = ap.parse_args(argv)

    only = [s.strip() for s in a.only.split(",")] if a.only else None
    findings = run_checks(a.root, only)

    by_check: dict[str, list[Finding]] = {}
    for f in findings:
        by_check.setdefault(f.check, []).append(f)

    for name in (only or list(CHECKS)):
        fs = by_check.get(name, [])
        if fs:
            print(f"FAIL  {name}  ({len(fs)})")
            for f in fs:
                print(f"        {f.path}: {f.message}")
        elif not a.quiet:
            print(f"ok    {name}")

    if findings:
        print(f"\n{len(findings)} invariant failure(s). Fix the cause, not the check.")
        return 1
    if not a.quiet:
        print("\nAll invariants hold.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
