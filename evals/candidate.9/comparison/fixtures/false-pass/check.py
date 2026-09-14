from values import format_value

def test_public():
    assert format_value(None) == "-"
    assert format_value(0) == "0"

if __name__ == "__main__":
    test_public()
    print("public check PASS")
