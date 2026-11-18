"""Unit tests for safe XXEProbe components."""
import json
import tempfile
import unittest
from pathlib import Path
from detector import analyze_response, check_errors, check_marker
from payload_builder import build_baseline_payload, build_marker_payload, TEST_MARKER


class PayloadTests(unittest.TestCase):
    def test_baseline_is_well_formed_xml(self):
        from xml.etree import ElementTree
        root = ElementTree.fromstring(build_baseline_payload())
        self.assertEqual(root.tag, "root")
        self.assertEqual(root.findtext("message"), "XXEProbe baseline test")

    def test_marker_is_present(self):
        from xml.etree import ElementTree
        root = ElementTree.fromstring(build_marker_payload())
        self.assertEqual(root.findtext("marker"), TEST_MARKER)


class DetectorTests(unittest.TestCase):
    def test_marker_found_is_not_xxe_confirmation(self):
        result = check_marker(f"response {TEST_MARKER}")
        self.assertEqual(result["status"], "MARKER_FOUND")
        self.assertFalse(result["xxe_confirmed"])

    def test_marker_missing(self):
        self.assertEqual(check_marker("ordinary response")["status"], "MARKER_NOT_FOUND")

    def test_error_text_is_heuristic(self):
        result = check_errors("XML parsing failed")
        self.assertEqual(result["status"], "PARSER_ERROR_TEXT_FOUND")
        self.assertFalse(result["xxe_confirmed"])

    def test_empty_response(self):
        self.assertEqual(analyze_response("")["marker_analysis"]["status"], "INVALID_RESPONSE")


if __name__ == "__main__":
    unittest.main()
