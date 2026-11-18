"""XXEProbe command-line entry point for safe localhost self-checks."""
import argparse
import json
from config import show_configuration, TOOL_NAME, VERSION
from detector import analyze_response
from payload_builder import build_baseline_payload, build_marker_payload, TEST_MARKER
from reporter import generate_report, read_listener_events


def run_self_test() -> int:
    print("=" * 54)
    print(f"{TOOL_NAME} — XML SECURITY LAB TOOL v{VERSION}")
    print("=" * 54)
    baseline = build_baseline_payload()
    marker_xml = build_marker_payload()
    print("\n[1] Baseline XML generated:")
    print(baseline)
    print("\n[2] Marker XML generated:")
    print(marker_xml)
    print("\n[3] Detector self-test (sample text only):")
    detection = analyze_response(f"Local sample contains {TEST_MARKER}")
    print(json.dumps(detection, indent=2))
    events, invalid = read_listener_events()
    print("\n[4] Listener log audit:")
    print(f"Valid local events: {len(events)}")
    print(f"Invalid log entries: {invalid}")
    print("XXE callback confirmation: NOT CONFIRMED")
    results = {
        "baseline_xml": "GENERATED",
        "marker_xml": "GENERATED",
        "detector": detection,
        "listener_valid_events": len(events),
        "listener_invalid_entries": invalid,
        "listener_status": "LOCAL_LOGGING_ONLY" if events else "NO_LOCAL_EVENTS",
        "xxe_confirmed": False,
    }
    print("\n[5] Report generation:")
    generate_report("Local self-test", results)
    print("\nSelf-test complete. This tool version does not confirm XXE vulnerabilities.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="XXEProbe safe localhost XML security lab")
    parser.add_argument("--config", action="store_true", help="Display configuration")
    parser.add_argument("--self-test", action="store_true", help="Run local builder, detector and report self-checks")
    args = parser.parse_args()
    if args.config:
        show_configuration()
        return 0
    return run_self_test()


if __name__ == "__main__":
    raise SystemExit(main())
