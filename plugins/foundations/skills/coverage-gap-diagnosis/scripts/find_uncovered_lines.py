#!/usr/bin/env python3
"""Report uncovered line ranges for specific files from a coverage artifact.

Replaces eyeballing a terminal coverage table or an HTML report with
deterministic parsing. Supports two artifact formats:

  - Istanbul-style JSON (e.g. Vitest/Jest coverage-final.json)
  - Go coverage profile text (coverage.out)

This is diagnostic only -- it reports *where* coverage is missing. It does
not say *what* behavior is untested; that still requires reading the
source at the reported ranges.

Usage:
    python3 find_uncovered_lines.py --coverage <path> <file> [<file> ...]

<file> arguments should be the changed-files list already computed by the
skill's own Step 1 (git diff), not recomputed by this script.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def detect_format(coverage_path: Path) -> str:
    return "istanbul" if coverage_path.suffix == ".json" else "go"


def collapse_ranges(lines: set[int]) -> list[tuple[int, int]]:
    if not lines:
        return []
    ordered = sorted(lines)
    ranges = []
    start = prev = ordered[0]
    for line in ordered[1:]:
        if line == prev + 1:
            prev = line
            continue
        ranges.append((start, prev))
        start = prev = line
    ranges.append((start, prev))
    return ranges


def parse_istanbul(coverage_path: Path, target_files: list[str]) -> dict[str, list[tuple[int, int]] | None]:
    data = json.loads(coverage_path.read_text())
    result: dict[str, list[tuple[int, int]] | None] = {f: None for f in target_files}

    for abs_path, file_cov in data.items():
        for target in target_files:
            if not abs_path.endswith(target):
                continue
            statement_map = file_cov.get("statementMap", {})
            hits = file_cov.get("s", {})
            uncovered_lines: set[int] = set()
            for stmt_id, loc in statement_map.items():
                if hits.get(stmt_id, 1) == 0:
                    start_line = loc["start"]["line"]
                    end_line = loc["end"]["line"]
                    uncovered_lines.update(range(start_line, end_line + 1))
            result[target] = collapse_ranges(uncovered_lines)

    return result


def parse_go_profile(coverage_path: Path, target_files: list[str]) -> dict[str, list[tuple[int, int]] | None]:
    line_pattern = re.compile(
        r"^(?P<file>\S+):(?P<start_line>\d+)\.\d+,(?P<end_line>\d+)\.\d+ \d+ (?P<count>\d+)$"
    )
    result: dict[str, list[tuple[int, int]] | None] = {f: None for f in target_files}
    uncovered_by_file: dict[str, set[int]] = {f: set() for f in target_files}

    for raw_line in coverage_path.read_text().splitlines():
        match = line_pattern.match(raw_line)
        if not match:
            continue
        file_path = match.group("file")
        for target in target_files:
            if not file_path.endswith(target):
                continue
            if result[target] is None:
                result[target] = []
            if int(match.group("count")) == 0:
                start_line = int(match.group("start_line"))
                end_line = int(match.group("end_line"))
                uncovered_by_file[target].update(range(start_line, end_line + 1))

    for target, lines in uncovered_by_file.items():
        if result[target] is not None:
            result[target] = collapse_ranges(lines)

    return result


def format_ranges(ranges: list[tuple[int, int]]) -> str:
    return ", ".join(f"{start}-{end}" if start != end else str(start) for start, end in ranges)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--coverage", required=True, help="Path to coverage-final.json or coverage.out")
    parser.add_argument("files", nargs="+", help="Changed files to check, as they appear in the coverage artifact")
    args = parser.parse_args()

    coverage_path = Path(args.coverage)
    if not coverage_path.is_file():
        print(f"error: coverage artifact not found: {coverage_path}", file=sys.stderr)
        return 0

    parser_fn = parse_istanbul if detect_format(coverage_path) == "istanbul" else parse_go_profile
    results = parser_fn(coverage_path, args.files)

    for target in args.files:
        ranges = results.get(target)
        if ranges is None:
            print(f"{target}: no coverage data found")
        elif not ranges:
            print(f"{target}: fully covered")
        else:
            print(f"{target}: lines {format_ranges(ranges)} uncovered")

    return 0


if __name__ == "__main__":
    sys.exit(main())
