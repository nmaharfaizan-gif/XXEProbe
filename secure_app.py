"""Secure localhost XML receiver for benign validation exercises."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from xml.etree import ElementTree
import json
from config import LAB_HOST, LAB_PORT, MAX_XML_BYTES


class SecureLabHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        raw_length = self.headers.get("Content-Length", "0")
        try:
            length = int(raw_length)
        except ValueError:
            self._send_json(400, {"status": "REJECTED", "reason": "Invalid Content-Length"})
            return
        if length <= 0 or length > MAX_XML_BYTES:
            self._send_json(413 if length > MAX_XML_BYTES else 400, {
                "status": "REJECTED", "reason": f"XML body must be between 1 and {MAX_XML_BYTES} bytes"
            })
            return
        raw = self.rfile.read(length)
        try:
            xml_text = raw.decode("utf-8")
        except UnicodeDecodeError:
            self._send_json(400, {"status": "REJECTED", "reason": "XML must be UTF-8"})
            return
        upper = xml_text.upper()
        if "<!DOCTYPE" in upper or "<!ENTITY" in upper:
            self._send_json(400, {"status": "REJECTED", "reason": "DTD and entity declarations are not accepted"})
            return
        try:
            root = ElementTree.fromstring(xml_text)
        except ElementTree.ParseError:
            self._send_json(400, {"status": "INVALID_XML", "reason": "XML parser rejected the document"})
            return
        self._send_json(200, {
            "status": "ACCEPTED",
            "root_element": root.tag,
            "message": "Well-formed XML accepted by the secure localhost demo",
        })

    def log_message(self, format, *args):
        return


def main() -> None:
    server = ThreadingHTTPServer((LAB_HOST, LAB_PORT), SecureLabHandler)
    print(f"XXEProbe Secure XML Lab: http://{LAB_HOST}:{LAB_PORT}")
    print("Bound to localhost only. Press CTRL+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSecure lab stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
