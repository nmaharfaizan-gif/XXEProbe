"""Read local listener logs and generate transparent JSON reports."""
import json
from datetime import datetime, timezone
from config import PROJECT_ROOT, REPORT_DIRECTORY, TOOL_NAME, VERSION, DEVELOPER

LOG_FILE = REPORT_DIRECTORY / "oob_events.jsonl"
REPORT_FILE = REPORT_DIRECTORY / "xxe_report.json"


def read_listener_events() -> tuple[list[dict], int]:
    events: list[dict] = []
    invalid_entries = 0
    if not LOG_FILE.exists():
        return events, invalid_entries
    with LOG_FILE.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                if isinstance(item, dict) and all(k in item for k in ("timestamp", "source_ip", "request_path", "event")):
                    events.append(item)
                else:
                    invalid_entries += 1
            except (json.JSONDecodeError, UnicodeDecodeError):
                invalid_entries += 1
    return events, invalid_entries


def generate_report(endpoint: str, results: dict) -> dict:
    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    events, invalid_entries = read_listener_events()
    report = {
        "tool": TOOL_NAME,
        "version": VERSION,
        "developer": DEVELOPER,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "test_environment": "Localhost-only educational lab",
        "endpoint": endpoint,
        "results": results,
        "listener_audit": {
            "valid_events": len(events),
            "invalid_entries": invalid_entries,
            "events": events,
            "status": "LOCAL_LISTENER_LOGGING_VERIFIED" if events else "NO_LISTENER_EVENTS_FOUND",
            "xxe_callback_confirmed": False,
        },
        "security_assessment": {
            "xxe_confirmed": False,
            "status": "NOT CONFIRMED",
            "limitations": [
                "The project sends only benign XML documents to its own localhost lab.",
                "Marker matching and parser-error text matching are heuristic self-checks.",
                "A local listener event proves only that the listener received a local request.",
                "This version does not perform or claim exploit-based XXE verification.",
            ],
        },
        "remediation": [
            "Disable DTD processing when it is not required.",
            "Disable external entity resolution in XML parsers.",
            "Use a hardened XML parser and keep it updated.",
            "Apply request-size limits and validate expected XML structure.",
        ],
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report saved: {REPORT_FILE.relative_to(PROJECT_ROOT)}")
    print(f"Valid listener events: {len(events)}")
    print(f"Invalid listener entries: {invalid_entries}")
    return report


if __name__ == "__main__":
    sample = {
        "marker_analysis": "SELF_TEST_ONLY",
        "error_text_analysis": "SELF_TEST_ONLY",
        "listener_event_analysis": "LOCAL_LISTENER_LOGGING_ONLY",
        "xxe_confirmed": False,
    }
    generate_report("Local self-test", sample)
