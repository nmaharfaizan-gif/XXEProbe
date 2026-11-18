"""Build harmless XML documents for baseline and marker tests."""
from xml.etree.ElementTree import Element, SubElement, tostring

TEST_MARKER = "XXEPROBE-TEST-2026"


def _serialize(root: Element) -> str:
    return tostring(root, encoding="unicode", short_empty_elements=True)


def build_baseline_payload() -> str:
    root = Element("root")
    message = SubElement(root, "message")
    message.text = "XXEProbe baseline test"
    return _serialize(root)


def build_marker_payload() -> str:
    root = Element("root")
    marker = SubElement(root, "marker")
    marker.text = TEST_MARKER
    return _serialize(root)


if __name__ == "__main__":
    print("Baseline XML:")
    print(build_baseline_payload())
    print("\nMarker XML:")
    print(build_marker_payload())
