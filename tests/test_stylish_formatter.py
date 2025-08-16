import pytest

from gendiff import generate_diff


@pytest.mark.parametrize("file1,file2,expected",
                         [("tests/test_data/file1.json",
                           "tests/test_data/file2.json",
                           "tests/test_data/file1_file2_expected.txt"),
                          ("tests/test_data/file1.yaml",
                           "tests/test_data/file2.yaml",
                           "tests/test_data/file1_file2_expected.txt"),
                          ("tests/test_data/complex_file1.json",
                           "tests/test_data/complex_file2.json",
                           "tests/test_data/complex_diff.txt"),
                          ("tests/test_data/complex_file1.yaml",
                           "tests/test_data/complex_file2.yaml",
                           "tests/test_data/complex_diff.txt"),
                          ("tests/test_data/file1.json",
                           "tests/test_data/empty.json",
                           "tests/test_data/file1_and_empty_expected.txt"),
                          ("tests/test_data/empty.json",
                           "tests/test_data/file1.json",
                           "tests/test_data/empty_and_file1_expected.txt")])
def test_stylish(file1, file2, expected):
    actual = generate_diff(file1, file2, "stylish")
    with open(expected) as file:
        exp = file.read()
        assert actual == exp
