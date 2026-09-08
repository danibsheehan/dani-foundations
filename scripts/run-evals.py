#!/usr/bin/env python3
"""Run every skill's evals.json against a real Claude Code session and grade it.

Requires the `claude` CLI on PATH and must be run from the repo root. Makes
real API calls (cost and time apply) -- one call to run each eval case with
the foundations plugin loaded, plus one call to grade the transcript against
that case's assertions. Each case runs in an isolated temp directory so
file-editing skills (doc-writer, doc-sync-patch, ...) never touch this repo.

Usage:
    python3 scripts/run-evals.py [--skill NAME] [--case ID]

Exit code is 1 if any assertion failed anywhere, 0 otherwise. Full
assertion-level results are written to scripts/eval-results/<timestamp>.json.
"""

import argparse
import datetime
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "plugins" / "foundations" / "skills"
PLUGIN_DIR = REPO_ROOT / "plugins" / "foundations"
RESULTS_DIR = REPO_ROOT / "scripts" / "eval-results"


def discover_eval_files(skill_filter: str | None) -> list[Path]:
    files = sorted(SKILLS_DIR.glob("*/evals.json"))
    if skill_filter:
        files = [f for f in files if f.parent.name == skill_filter]
    return files


def load_cases(path: Path, case_filter: str | None) -> list[dict]:
    cases = json.loads(path.read_text())
    if case_filter:
        cases = [c for c in cases if c["id"] == case_filter]
    return cases


def run_claude_print(prompt: str, cwd: Path, extra_args: list[str]) -> dict:
    result = subprocess.run(
        ["claude", "-p", "--output-format", "json", *extra_args, prompt],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=300,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"result": result.stdout, "error": result.stderr}


def run_case(case: dict) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        response = run_claude_print(
            case["prompt"],
            cwd=tmp_path,
            extra_args=["--plugin-dir", str(PLUGIN_DIR), "--permission-mode", "acceptEdits"],
        )
        response_text = response.get("result", "")

        file_contents = []
        for file_path in sorted(tmp_path.rglob("*")):
            if file_path.is_file():
                rel = file_path.relative_to(tmp_path)
                file_contents.append(f"--- {rel} ---\n{file_path.read_text(errors='replace')}")

        transcript = response_text
        if file_contents:
            transcript += "\n\n" + "\n\n".join(file_contents)
        return transcript


def grade_case(case: dict, transcript: str) -> dict:
    assertions = case["assertions"]
    grading_prompt = (
        "Grade the following agent output against each assertion. "
        "Respond with ONLY strict JSON of the form "
        '{"results": [{"assertion": str, "pass": bool, "note": str}, ...]}, '
        "one entry per assertion, in the same order.\n\n"
        f"Assertions:\n{json.dumps(assertions, indent=2)}\n\n"
        f"Agent output:\n{transcript}"
    )
    graded = run_claude_print(grading_prompt, cwd=REPO_ROOT, extra_args=[])
    graded_text = graded.get("result", "{}")
    try:
        return json.loads(graded_text)
    except json.JSONDecodeError:
        return {"results": [{"assertion": a, "pass": False, "note": "grader returned non-JSON output"} for a in assertions]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skill", default=None, help="Only run this skill's evals.json (directory name)")
    parser.add_argument("--case", default=None, help="Only run this case id")
    args = parser.parse_args()

    eval_files = discover_eval_files(args.skill)
    if not eval_files:
        print("No matching evals.json files found.", file=sys.stderr)
        return 1

    all_results = []
    any_failure = False

    for eval_file in eval_files:
        skill_name = eval_file.parent.name
        cases = load_cases(eval_file, args.case)
        for case in cases:
            transcript = run_case(case)
            graded = grade_case(case, transcript)
            case_results = graded.get("results", [])
            passed = sum(1 for r in case_results if r.get("pass"))
            total = len(case_results)
            if passed < total:
                any_failure = True
            print(f"{skill_name}/{case['id']}: {passed}/{total} assertions passed")
            all_results.append(
                {
                    "skill": skill_name,
                    "case_id": case["id"],
                    "results": case_results,
                }
            )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results_path = RESULTS_DIR / f"{timestamp}.json"
    results_path.write_text(json.dumps(all_results, indent=2))
    print(f"\nFull results written to {results_path.relative_to(REPO_ROOT)}")

    return 1 if any_failure else 0


if __name__ == "__main__":
    sys.exit(main())
