import pytest

from diffcalculator.internal.diffcalc import generate_diff


@pytest.fixture
def non_empty_file1():
    return "./diffcalculator/tests/test_data/file1.json"


@pytest.fixture
def non_empty_file2():
    return "./diffcalculator/tests/test_data/file2.json"


@pytest.fixture
def empty_file():
    return "./diffcalculator/tests/test_data/file3.json"


def test_normal_scenario(non_empty_file1, non_empty_file2):
    diff = generate_diff(non_empty_file1, non_empty_file2)
    expected = open("./diffcalculator/tests/test_data/file1-2_expected.txt")
    assert diff == expected.read()


def test_empty_files(empty_file):
    diff = generate_diff(empty_file, empty_file)
    expected = open("./diffcalculator/tests/test_data/empty_diff_expected.txt")
    assert diff == expected.read()


def test_not_empty_and_empty(non_empty_file1, empty_file):
    diff = generate_diff(non_empty_file1, empty_file)
    expected = open("./diffcalculator/tests/test_data/file1-3_expected.txt")
    assert diff == expected.read()


def test_empty_and_not_empty(empty_file, non_empty_file1):
    diff = generate_diff(empty_file, non_empty_file1)
    expected = open("./diffcalculator/tests/test_data/file3-1_expected.txt")
    assert diff == expected.read()
