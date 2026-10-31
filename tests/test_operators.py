from arithmp.parser import Parser


def test_add():
    p = Parser().parse
    assert p(None, "1 + 1 == 2")
    assert p(None, "0 + 3 == 3")
