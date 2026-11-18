"""Send benign XML validation cases to the XXEProbe localhost lab."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
import urllib.error
import urllib.request
from config import LAB_HOST, LAB_PORT, REPORT_DIRECTORY
from payload_builder import build_baseline_payload, build_marker_payload

LAB_URL = f"http://{LAB_HOST}:{LAB_PORT}/"


def send_xml(xml_data: str) -> tuple[int | None, str]:
    request = urllib.request.Request(
        LAB_URL, data=xml_data.encode("utf-8"),
        headers={"Content-Type": "application/xml; charset=utf-8"}, method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=4) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", errors="replace")
    except (OSError, TimeoutError) as error:
        return None, f"Could not contact localhost lab: {error}"


def main() -> int:
    test_cases = {
        "baseline_xml": (build_baseline_payload(), 200),
        "marker_xml": (build_marker_payload(), 200),
        "malformed_xml": ("<root><message>unfinished</root>", 400),
        "doctype_rejection": ("<!DOCTYPE root><root><message>safe rejection check</message></root>", 400),
    }
    results = {}
    passed = 0
    print("=" * 52)
    print("XXEPROBE LOCAL XML VALIDATION TESTS")
    print("=" * 52)
    for name, (xml_data, expected) in test_cases.items():
        status, response = send_xml(xml_data)
        success = status == expected
        passed += int(success)
        results[name] = {
            "expected_http_status": expected,
            "actual_http_status": status,
            "passed": success,
            "response": response,
        }
        print(f"{name}: {'PASS' if success else 'FAIL'} (expected {expected}, got {status})")
    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    output = REPORT_DIRECTORY / "lab_test_results.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults saved: {output}")
    print(f"Summary: {passed}/{len(test_cases)} passed")
    print("These are local XML handling checks, not XXE exploit tests.")
    return 0 if passed == len(test_cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
