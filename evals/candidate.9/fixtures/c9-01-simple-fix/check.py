from values import format_value

def test_none_and_true():
    assert format_value(None) == "-"
    assert format_value(True) == "True"
