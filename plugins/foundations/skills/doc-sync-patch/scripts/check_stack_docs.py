#!/usr/bin/env python3
"""Fallback stack-docs-drift checker for repos with no checker of their own.

Scope is deliberately narrow: Node and Go *runtime version* claims only,
since those are the two claims that have an unambiguous, structured source
of truth (.nvmrc / package.json engines.node, go.mod's `go` directive).
Framework/build-tool version claims in prose aren't matched here -- that
still needs a human (or Claude) reading both sides, since the doc phrasing
for those varies too much to regex reliably.

Usage:
    python3 check_stack_docs.py [--repo-root PATH]

Exits 1 if any mismatch is found, 0 otherwise (including when no
applicable manifest/doc files exist).
"""

import argparse
import json
import re
import sys
from pathlib import Path

DOC_FILES = ("README.md", "AGENTS.md")


def find_repo_root(raw: str | None) -> Path:
    return Path(raw).resolve() if raw else Path.cwd()


def get_declared_node_version(root: Path) -> str | None:
    nvmrc = root / ".nvmrc"
    if nvmrc.is_file():
        return nvmrc.read_text().strip().lstrip("v")

    package_json = root / "package.json"
    if package_json.is_file():
        try:
            data = json.loads(package_json.read_text())
        except json.JSONDecodeError:
            return None
        engines_node = data.get("engines", {}).get("node")
        if engines_node:
            match = re.search(r"(\d+(?:\.\d+)*)", engines_node)
            if match:
                return match.group(1)
    return None


def get_declared_go_version(root: Path) -> str | None:
    go_mod = root / "go.mod"
    if not go_mod.is_file():
        return None
    match = re.search(r"^go\s+(\d+\.\d+(?:\.\d+)?)", go_mod.read_text(), re.MULTILINE)
    return match.group(1) if match else None


def find_doc_claims(doc_text: str, keyword: str) -> list[str]:
    pattern = rf"{keyword}\.?\s*v?(\d+(?:\.\d+)*)"
    return re.findall(pattern, doc_text, re.IGNORECASE)


def normalize(version: str, precision: int) -> str:
    parts = version.split(".")
    return ".".join(parts[:precision])


def check_keyword(root: Path, doc_path: Path, keyword: str, manifest_version: str | None) -> list[str]:
    if manifest_version is None:
        return []
    doc_text = doc_path.read_text()
    claims = find_doc_claims(doc_text, keyword)
    mismatches = []
    for claim in claims:
        precision = min(claim.count(".") + 1, manifest_version.count(".") + 1)
        if normalize(claim, precision) != normalize(manifest_version, precision):
            mismatches.append(
                f"{doc_path.name}: claims {keyword} {claim}, manifest says {manifest_version}"
            )
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", default=None, help="Repo root to check (default: current directory)")
    args = parser.parse_args()

    root = find_repo_root(args.repo_root)
    node_version = get_declared_node_version(root)
    go_version = get_declared_go_version(root)

    mismatches: list[str] = []
    for doc_name in DOC_FILES:
        doc_path = root / doc_name
        if not doc_path.is_file():
            continue
        mismatches.extend(check_keyword(root, doc_path, "Node", node_version))
        mismatches.extend(check_keyword(root, doc_path, "Go", go_version))

    for line in mismatches:
        print(line)

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
