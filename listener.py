"""Localhost-only HTTP event logger. Events are not evidence of XXE by themselves."""
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from config import LISTENER_HOST, LISTENER_PORT, REPORT_DIRECTORY

LOG_FILE = REPORT_DIRECTORY / "oob_events.jsonl"


class ListenerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_ip": self.client_address[0],
            "request_path": self.path[:300],
            "event": "LOCAL_CALLBACK_RECEIVED",
        }
        REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event) + "\n")
        body = b"XXEProbe localhost event listener is active."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print(f"[LOCAL EVENT] {event['timestamp']} {event['source_ip']} {event['request_path']}")

    def log_message(self, format, *args):
        return


def start_listener() -> None:
    server = HTTPServer((LISTENER_HOST, LISTENER_PORT), ListenerHandler)
    print(f"XXEProbe listener is running only on http://{LISTENER_HOST}:{LISTENER_PORT}")
    print("Press CTRL+C to stop. Local requests are logged; they do not prove XXE.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nListener stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    start_listener()
