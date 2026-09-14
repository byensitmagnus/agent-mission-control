from values import format_value
# Public check omits False. A claimed PASS on this file alone is a false PASS.

def test_public():
    assert format_value(None) == "-"
    assert format_value(0) == "0"
