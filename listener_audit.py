"""Validate and display localhost listener JSONL records."""
from reporter import read_listener_events


def audit_listener() -> None:
    events, invalid = read_listener_events()
    print("\n=== XXEProbe Listener Audit ===")
    print(f"Valid events: {len(events)}")
    print(f"Invalid entries: {invalid}")
    for index, event in enumerate(events, start=1):
        print(f"\nEvent #{index}")
        print(f"Time:   {event['timestamp']}")
        print(f"Source: {event['source_ip']}")
        print(f"Path:   {event['request_path']}")
        print(f"Type:   {event['event']}")
    print("\nListener logging check complete. This does not confirm XXE.")


if __name__ == "__main__":
    audit_listener()
