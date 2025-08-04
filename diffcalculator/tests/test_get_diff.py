import pytest
from diffcalculator.internal import diffcalc


@pytest.fixture
def file1_json():
    json_file1_path = "diffcalculator/tests/test_data/file1.json"
    return diffcalc.read_file(json_file1_path)


@pytest.fixture
def file2_json():
    json_file2_path = "diffcalculator/tests/test_data/file2.json"
    return diffcalc.read_file(json_file2_path)


@pytest.fixture
def file1_yaml():
    yaml_file1_path = "diffcalculator/tests/test_data/file1.yaml"
    return diffcalc.read_file(yaml_file1_path)


@pytest.fixture
def file2_yaml():
    yaml_file2_path = "diffcalculator/tests/test_data/file2.yaml"
    return diffcalc.read_file(yaml_file2_path)


@pytest.fixture
def complex_file1():
    path = "diffcalculator/tests/test_data/complex_file1.json"
    return diffcalc.read_file(path)


@pytest.fixture
def complex_file2():
    path = "diffcalculator/tests/test_data/complex_file2.json"
    return diffcalc.read_file(path)


def test_normal_scenario_json_format(file1_json, file2_json):
    actual = diffcalc.stylish(file1_json, file2_json)
    path_to_expected = "diffcalculator/tests/test_data/file1_file2_expected.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    assert actual == expected


def test_with_empty_file_json_format():
    json_file1_path = "diffcalculator/tests/test_data/file1.json"
    empty_json_path = "diffcalculator/tests/test_data/empty.json"

    file1 = diffcalc.read_file(json_file1_path)
    empty_file = diffcalc.read_file(empty_json_path)
    actual = diffcalc.stylish(file1, empty_file)

    path_to_expected = "diffcalculator/tests/test_data/file1_and_empty_expected.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    assert actual == expected

    path_to_expected = "diffcalculator/tests/test_data/empty_and_file1_expected.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    actual = diffcalc.stylish(empty_file, file1)
    assert actual == expected


def test_normal_scenario_yaml_format(file1_yaml, file2_yaml):
    actual = diffcalc.stylish(file1_yaml, file2_yaml)
    path_to_expected = "diffcalculator/tests/test_data/file1_file2_expected.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    assert actual == expected


def test_complex_json_file(complex_file1, complex_file2):
    path_to_expected = "diffcalculator/tests/test_data/complex_diff.txt"
    expected = None
    with open(path_to_expected) as file:
        expected = file.read()
    actual = diffcalc.stylish(complex_file1, complex_file2)
    assert actual == expected