"""Summarize localhost validation results into a final lab report."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from datetime import datetime, timezone
from config import REPORT_DIRECTORY, TOOL_NAME, VERSION, DEVELOPER

INPUT_FILE = REPORT_DIRECTORY / "lab_test_results.json"
OUTPUT_FILE = REPORT_DIRECTORY / "final_lab_report.json"


def analyze_results() -> int:
    if not INPUT_FILE.exists():
        print("Results not found. Start lab/secure_app.py, then run lab/test_client.py.")
        return 1
    try:
        results = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not read test results: {error}")
        return 1
    tests = {}
    for name, data in results.items():
        tests[name] = {
            "expected_http_status": data.get("expected_http_status"),
            "actual_http_status": data.get("actual_http_status"),
            "outcome": "PASSED" if data.get("passed") is True else "FAILED",
            "response": data.get("response", ""),
        }
    passed = sum(item["outcome"] == "PASSED" for item in tests.values())
    report = {
        "tool": TOOL_NAME,
        "version": VERSION,
        "developer": DEVELOPER,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "environment": "127.0.0.1 localhost-only lab",
        "summary": {"passed": passed, "total": len(tests), "all_passed": bool(tests) and passed == len(tests)},
        "tests": tests,
        "security_conclusion": "These checks validate benign XML handling and defensive rejection behavior. They do not establish whether any parser is XXE-vulnerable.",
        "remediation": [
            "Disable DTD processing when it is not required.",
            "Disable external entity resolution.",
            "Use a hardened XML parser.",
            "Apply input-size limits and validate expected document structure.",
        ],
    }
    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
    for name, item in tests.items():
        print(f"{name}: {item['outcome']}")
    print(f"\nFinal report: {OUTPUT_FILE}")
    print(f"Summary: {passed}/{len(tests)} passed")
    return 0 if report["summary"]["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(analyze_results())
