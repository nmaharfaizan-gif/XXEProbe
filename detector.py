"""Conservative response text checks; these checks do not prove XXE."""
from payload_builder import TEST_MARKER

ERROR_PATTERNS = (
    "xml parsing error",
    "entity not defined",
    "external entity",
    "doctype is disallowed",
    "xml syntax error",
    "xml parsing failed",
    "invalid xml",
)


def check_marker(response: str) -> dict:
    if not isinstance(response, str) or not response.strip():
        return {"status": "INVALID_RESPONSE", "evidence": "Response is empty or not text", "xxe_confirmed": False}
    found = TEST_MARKER in response
    return {
        "status": "MARKER_FOUND" if found else "MARKER_NOT_FOUND",
        "evidence": TEST_MARKER if found else "No test marker detected",
        "xxe_confirmed": False,
    }


def check_errors(response: str) -> dict:
    if not isinstance(response, str) or not response.strip():
        return {"status": "INVALID_RESPONSE", "evidence": [], "xxe_confirmed": False}
    found = [pattern for pattern in ERROR_PATTERNS if pattern in response.casefold()]
    return {
        "status": "PARSER_ERROR_TEXT_FOUND" if found else "NO_PARSER_ERROR_TEXT",
        "evidence": found,
        "xxe_confirmed": False,
    }


def analyze_response(response: str) -> dict:
    return {
        "marker_analysis": check_marker(response),
        "error_text_analysis": check_errors(response),
        "security_conclusion": "Text matching is indicative only and cannot confirm an XXE vulnerability.",
        "xxe_confirmed": False,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(analyze_response(f"Example response {TEST_MARKER}"), indent=2))
