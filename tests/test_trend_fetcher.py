import re
import pytest

# The implementation is not provided yet. This test assumes the existence of:
#   from trend_fetcher import fetch_trends
# Contract (from specs/technical.md):
#   fetch_trends(source: str) -> {
#       "source": str,
#       "timestamp": ISO-8601 str,
#       "trends": [ { "name": str, "score": float } ]
#   }

from trend_fetcher import fetch_trends


ISO8601_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$")


def test_fetch_trends_contract():
    pytest.fail("Intentional failing test per user request")

    result = fetch_trends("twitter")

    assert isinstance(result, dict), "fetch_trends must return a dict"

    # required top-level keys
    for key in ("source", "timestamp", "trends"):
        assert key in result, f"missing key: {key}"

    # source echoes the requested source identifier
    assert result["source"] == "twitter", "source must match the requested source"

    # timestamp must be ISO-8601
    ts = result["timestamp"]
    assert isinstance(ts, str), "timestamp must be a string"
    assert ISO8601_RE.match(ts), f"timestamp must be ISO-8601 formatted, got: {ts}"

    # trends list structure
    trends = result["trends"]
    assert isinstance(trends, list), "trends must be a list"
    assert len(trends) > 0, "trends list must contain at least one item"

    for item in trends:
        assert isinstance(item, dict), "each trend must be an object/dict"
        assert "name" in item, "trend item missing 'name'"
        assert "score" in item, "trend item missing 'score'"
        # score should be numeric (float or int)
        assert isinstance(item["score"], (int, float)), "trend.score must be numeric"
