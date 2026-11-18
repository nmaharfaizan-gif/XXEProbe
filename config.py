"""Central configuration for the XXEProbe localhost lab."""
from pathlib import Path

TOOL_NAME = "XXEProbe"
VERSION = "1.1.0"
DEVELOPER = "Faizan"
LAB_HOST = "127.0.0.1"
LAB_PORT = 8001
LISTENER_HOST = "127.0.0.1"
LISTENER_PORT = 8000
MAX_XML_BYTES = 16_384
PROJECT_ROOT = Path(__file__).resolve().parent
REPORT_DIRECTORY = PROJECT_ROOT / "reports"


def show_configuration() -> None:
    print("=" * 44)
    print(f"{TOOL_NAME} CONFIGURATION")
    print("=" * 44)
    print(f"Version: {VERSION}")
    print(f"Developer: {DEVELOPER}")
    print(f"Secure lab: http://{LAB_HOST}:{LAB_PORT}")
    print(f"Local event listener: http://{LISTENER_HOST}:{LISTENER_PORT}")
    print(f"Maximum XML body: {MAX_XML_BYTES} bytes")
    print(f"Reports: {REPORT_DIRECTORY}")
    print("=" * 44)


if __name__ == "__main__":
    show_configuration()
