#!/usr/bin/env python3
"""Create, inspect and re-annotate nodes in the analysis claim tree.

A node is a directory holding `claim.md`, `run.sh`, `scripts/`, `results/`,
`provenance/`, and optionally `env/`. Children are subdirectories. The kind of
parent-child relationship (`alternatives` or `sub-analyses`) is a property of a
node's whole set of children, recorded in the parent's `claim.md`.

Invariants this script maintains, so they cannot drift by hand:
  * a node whose children are alternatives has exactly one main path, and its
    `run.sh` calls only that child;
  * a node whose children are sub-analyses calls every child, in directory order,
    followed by its own scripts;
  * an alternatives node stores no scripts of its own (it is a pure switch).

Dual interface:
    API:  create_node(parent, name, claim, kind=None) -> Path
          read_node(path) -> dict
          set_main_path(node, child_name) -> None
          regenerate_run_sh(node) -> str
    CLI:  python node.py new <parent> <name> --claim "..." [--kind alternatives|sub-analyses]
          python node.py show <path>
          python node.py tree [root]
          python node.py promote <alternatives-node> <child-name>
          python node.py rebuild <path>
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALTERNATIVES = "alternatives"
SUB_ANALYSES = "sub-analyses"
KINDS = (ALTERNATIVES, SUB_ANALYSES)

CLAIM_TEMPLATE = """# Claim

{claim}

## Children

kind: {kind}
main-path: {main_path}

## Environment

inherits: the project main environment (`environment/`)

## Answers

_(What this node's analysis yielded. Each answer belongs in the claim collection
under `Human-AI-collaboration/claims/` with a pointer to the result grounding it.)_
"""

RUN_HEADER = """#!/usr/bin/env bash
# Main script for node: {name}
# Generated shape -- edit the "own scripts" block; the child calls are maintained
# by `node.py rebuild`, which enforces the alternatives/sub-analyses semantics.
set -euo pipefail
cd "$(dirname "$0")"
REPO_ROOT="$(cd "{up}" && pwd)"
# Node scripts run under the pinned analysis environment (AGENTS.md §2), not under
# .venv, which is the repository's own machinery. A node needing something beyond it
# declares env/ and overrides PYTHON below.
PYTHON="$REPO_ROOT/environment/env/bin/python"
"""


def _field(text: str, key: str) -> str | None:
    m = re.search(rf"^{re.escape(key)}:\s*(.*)$", text, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    return None if v in ("", "-", "none", "n/a") else v


def repo_root(node: Path) -> Path:
    """The repository root: the nearest ancestor holding AGENTS.md."""
    for p in [node.resolve(), *node.resolve().parents]:
        if (p / "AGENTS.md").exists():
            return p
    raise SystemExit(f"no repository root (no AGENTS.md above): {node}")


def _up_to_root(node: Path) -> str:
    """Relative path from a node directory up to the repository root."""
    depth = len(node.resolve().relative_to(repo_root(node)).parts)
    return "/".join([".."] * depth) if depth else "."


def children(node: Path) -> list[Path]:
    """Child nodes, in directory order (which is the order a parent runs them)."""
    return sorted(
        p for p in node.iterdir()
        if p.is_dir() and (p / "claim.md").exists()
    )


def read_node(path: str | Path) -> dict:
    node = Path(path)
    claim_file = node / "claim.md"
    if not claim_file.exists():
        raise SystemExit(f"not a node (no claim.md): {node}")
    text = claim_file.read_text()
    body = text.split("## Children")[0]
    claim = "\n".join(
        l for l in body.splitlines() if l.strip() and not l.startswith("#")
    ).strip()
    return {
        "path": node,
        "claim": claim,
        "kind": _field(text, "kind"),
        "main_path": _field(text, "main-path"),
        "children": children(node),
        "has_env": (node / "env").is_dir(),
        # Only files are callable steps. A subdirectory of scripts/ is supporting
        # material -- a model contract directory, a package -- and is called by one
        # of the files beside it rather than by run.sh.
        "scripts": sorted(
            p for p in (node / "scripts").glob("*")
            if p.is_file() and p.name != ".gitkeep"
        ) if (node / "scripts").is_dir() else [],
    }


def regenerate_run_sh(node: str | Path, write: bool = True) -> str:
    """Rebuild a node's run.sh so its child calls match the declared semantics."""
    node = Path(node)
    info = read_node(node)
    kids = info["children"]
    lines = [RUN_HEADER.format(name=node.name, up=_up_to_root(node))]

    if kids:
        kind = info["kind"]
        if kind not in KINDS:
            raise SystemExit(
                f"{node}: has children but 'kind:' is {kind!r}; "
                f"must be one of {KINDS}"
            )
        if kind == ALTERNATIVES:
            main = info["main_path"]
            names = [k.name for k in kids]
            if main not in names:
                raise SystemExit(
                    f"{node}: kind is alternatives but main-path {main!r} "
                    f"is not among the children {names}"
                )
            if info["scripts"]:
                raise SystemExit(
                    f"{node}: an alternatives node is a pure switch and must store "
                    f"no scripts of its own, but scripts/ is not empty"
                )
            lines.append("# Alternatives: only the main path is run here.")
            lines.append(f"# Not taken: {', '.join(n for n in names if n != main)}"
                         if len(names) > 1 else "# (only one alternative so far)")
            lines.append(f'bash "{main}/run.sh"')
        else:
            lines.append("# Sub-analyses: every child runs, in order.")
            for k in kids:
                lines.append(f'bash "{k.name}/run.sh"')

    own = info["scripts"]
    if own:
        lines.append("")
        lines.append("# Own scripts")
        for s in own:
            runner = "bash" if s.suffix == ".sh" else '"$PYTHON"'
            lines.append(f'{runner} "scripts/{s.name}"')
    elif not kids:
        lines.append("")
        lines.append("# Own scripts -- add calls here as scripts/ fills up.")

    text = "\n".join(lines).rstrip() + "\n"
    if write:
        run = node / "run.sh"
        run.write_text(text)
        run.chmod(0o755)
    return text


def create_node(parent: str | Path, name: str, claim: str, kind: str | None = None) -> Path:
    """Create a child node under `parent`. `kind` sets the *new node's own* child kind."""
    parent = Path(parent)
    if not (parent / "claim.md").exists():
        raise SystemExit(f"parent is not a node: {parent}")
    node = parent / name
    if node.exists():
        raise SystemExit(f"already exists: {node}")

    for sub in ("scripts", "results", "provenance"):
        (node / sub).mkdir(parents=True)
        (node / sub / ".gitkeep").touch()

    (node / "claim.md").write_text(
        CLAIM_TEMPLATE.format(claim=claim.strip(), kind=kind or "-", main_path="-")
    )
    regenerate_run_sh(node)

    parent_info = read_node(parent)
    if parent_info["kind"] == ALTERNATIVES and parent_info["main_path"] is None:
        set_main_path(parent, name)  # first alternative becomes the main path
    else:
        try:
            regenerate_run_sh(parent)
        except SystemExit as e:
            print(f"note: parent run.sh not rebuilt -- {e}", file=sys.stderr)
    return node


def set_main_path(node: str | Path, child_name: str) -> None:
    node = Path(node)
    text = (node / "claim.md").read_text()
    if _field(text, "kind") != ALTERNATIVES:
        raise SystemExit(f"{node}: main-path only applies to an alternatives node")
    if not (node / child_name / "claim.md").exists():
        raise SystemExit(f"{node}: no such child node: {child_name}")
    text = re.sub(r"^main-path:.*$", f"main-path: {child_name}", text, count=1, flags=re.M)
    (node / "claim.md").write_text(text)
    regenerate_run_sh(node)


def print_tree(root: str | Path, indent: str = "", suffix: str = "") -> None:
    info = read_node(root)
    marker = ""
    if info["kind"] == ALTERNATIVES:
        marker = f"  [alternatives -> {info['main_path']}]"
    elif info["kind"] == SUB_ANALYSES:
        marker = "  [sub-analyses]"
    first = info["claim"].splitlines()[0] if info["claim"] else "(no claim)"
    print(f"{indent}{Path(root).name}/{marker}{suffix}")
    print(f"{indent}    {first}")
    for k in info["children"]:
        off = ("  <- not taken; run by the stability node"
               if info["kind"] == ALTERNATIVES and k.name != info["main_path"] else "")
        print_tree(k, indent + "  ", off)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="create a child node")
    p.add_argument("parent")
    p.add_argument("name")
    p.add_argument("--claim", required=True, help="the analytical aim, one or two sentences")
    p.add_argument("--kind", choices=KINDS, help="kind of THIS node's own children")

    p = sub.add_parser("show", help="print one node")
    p.add_argument("path")

    p = sub.add_parser("tree", help="print the tree")
    p.add_argument("root", nargs="?", default="analysis")

    p = sub.add_parser("promote", help="make a child the main path")
    p.add_argument("node")
    p.add_argument("child")

    p = sub.add_parser("rebuild", help="regenerate run.sh from the declared semantics")
    p.add_argument("path")
    p.add_argument("--recursive", action="store_true")

    a = ap.parse_args(argv)

    if a.cmd == "new":
        node = create_node(a.parent, a.name, a.claim, a.kind)
        print(f"created {node}")
    elif a.cmd == "show":
        info = read_node(a.path)
        print(f"{info['path']}")
        print(f"  claim: {info['claim']}")
        print(f"  kind: {info['kind']}   main-path: {info['main_path']}")
        print(f"  children: {[c.name for c in info['children']] or '-'}")
        print(f"  own scripts: {[s.name for s in info['scripts'] if s.name != '.gitkeep'] or '-'}")
        print(f"  env override: {'yes' if info['has_env'] else 'no'}")
    elif a.cmd == "tree":
        print_tree(a.root)
    elif a.cmd == "promote":
        set_main_path(a.node, a.child)
        print(f"main path of {a.node} is now {a.child}")
    elif a.cmd == "rebuild":
        targets = [Path(a.path)]
        if a.recursive:
            targets = [p.parent for p in Path(a.path).rglob("claim.md")]
        for t in sorted(targets):
            regenerate_run_sh(t)
            print(f"rebuilt {t}/run.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
