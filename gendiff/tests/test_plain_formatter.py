
from gendiff.formatter.plain import plain


def test_with_complex_json(complex_json_file1, complex_json_file2):
    got = plain(complex_json_file1, complex_json_file2)
    with open("gendiff/tests/test_data/complex_diff_plain.txt") as file:
        expected = file.read()
        assert got == expected