from gendiff.formatter.stylish import stylish


def test_normal_scenario_json_format(file1_json, file2_json):
    actual = stylish(file1_json, file2_json)
    path_to_expected = "tests/test_data/file1_file2_expected.txt"
    with open(path_to_expected) as file:
        expected = file.read()
        assert actual == expected


def test_with_empty_file_json_format(file1_json):
    empty_json_path = "tests/test_data/empty.json"

    path_to_expected = "tests/test_data/file1_and_empty_expected.txt"
    with open(path_to_expected) as file:
        expected = file.read()
        actual = stylish(file1_json, empty_json_path)
        assert actual == expected

    path_to_expected = "tests/test_data/empty_and_file1_expected.txt"

    with open(path_to_expected) as file:
        expected = file.read()
        actual = stylish(empty_json_path, file1_json)
        assert actual == expected


def test_normal_scenario_yaml_format(file1_yaml, file2_yaml):
    path_to_expected = "tests/test_data/file1_file2_expected.txt"
    with open(path_to_expected) as file:
        expected = file.read()
        actual = stylish(file1_yaml, file2_yaml)
        assert actual == expected


def test_complex_json_file(complex_json_file1, complex_json_file2):
    path_to_expected = "tests/test_data/complex_diff.txt"
    with open(path_to_expected) as file:
        expected = file.read()
        actual = stylish(complex_json_file1, complex_json_file2)
    assert actual == expected


def test_complex_yaml_file(complex_yaml_file1, complex_yaml_file2):
    path_to_expected = "tests/test_data/complex_diff.txt"
    with open(path_to_expected) as file:
        expected = file.read()
        actual = stylish(complex_yaml_file1, complex_yaml_file2)
        assert actual == expected
