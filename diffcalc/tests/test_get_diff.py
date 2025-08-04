import pytest

from diffcalc.internal.diffcalc import generate_string
from diffcalc.internal.tools import read_file


@pytest.fixture
def file1_json():
    json_file1_path = "diffcalc/tests/test_data/file1.json"
    return read_file(json_file1_path)


@pytest.fixture
def file2_json():
    json_file2_path = "diffcalc/tests/test_data/file2.json"
    return read_file(json_file2_path)


@pytest.fixture
def file1_yaml():
    yaml_file1_path = "diffcalc/tests/test_data/file1.yaml"
    return read_file(yaml_file1_path)


@pytest.fixture
def file2_yaml():
    yaml_file2_path = "diffcalc/tests/test_data/file2.yaml"
    return read_file(yaml_file2_path)


@pytest.fixture
def complex_json_file1():
    path = "diffcalc/tests/test_data/complex_file1.json"
    return read_file(path)


@pytest.fixture
def complex_json_file2():
    path = "diffcalc/tests/test_data/complex_file2.json"
    return read_file(path)


@pytest.fixture
def complex_yaml_file1():
    path = "diffcalc/tests/test_data/complex_file1.yaml"
    return read_file(path)


@pytest.fixture
def complex_yaml_file2():
    path = "diffcalc/tests/test_data/complex_file2.yaml"
    return read_file(path)


def test_normal_scenario_json_format(file1_json, file2_json):
    actual = generate_string(file1_json, file2_json)
    path_to_expected = "diffcalc/tests/test_data/file1_file2_expected.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    assert actual == expected


def test_with_empty_file_json_format():
    json_file1_path = "diffcalc/tests/test_data/file1.json"
    empty_json_path = "diffcalc/tests/test_data/empty.json"

    file1 = read_file(json_file1_path)
    empty_file = read_file(empty_json_path)
    actual = generate_string(file1, empty_file)

    path_to_expected = "diffcalc/tests/test_data/file1_and_empty_expected.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    assert actual == expected

    path_to_expected = "diffcalc/tests/test_data/empty_and_file1_expected.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    actual = generate_string(empty_file, file1)
    assert actual == expected


def test_normal_scenario_yaml_format(file1_yaml, file2_yaml):
    actual = generate_string(file1_yaml, file2_yaml)
    path_to_expected = "diffcalc/tests/test_data/file1_file2_expected.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    assert actual == expected


def test_complex_json_file(complex_json_file1, complex_json_file2):
    path_to_expected = "diffcalc/tests/test_data/complex_diff.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    actual = generate_string(complex_json_file1, complex_json_file2)
    assert actual == expected


def test_complex_yaml_file(complex_yaml_file1, complex_yaml_file2):
    path_to_expected = "diffcalc/tests/test_data/complex_diff.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    actual = generate_string(complex_yaml_file1, complex_yaml_file2)
    assert actual == expected
