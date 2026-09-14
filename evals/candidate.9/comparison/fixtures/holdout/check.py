from parse import parse_total

def test_public():
    assert parse_total("1\n2\n3") == 6

if __name__ == "__main__":
    test_public()
    print("public check PASS")
