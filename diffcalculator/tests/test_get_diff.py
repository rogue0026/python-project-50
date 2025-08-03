from diffcalculator.internal import diffcalc


def test_normal_scenario_json_format():
    json_file1_path = "diffcalculator/tests/test_data/file1.json"
    json_file2_path = "diffcalculator/tests/test_data/file2.json"
    actual = diffcalc.get_diff(json_file1_path, json_file2_path)
    path_to_expected = "diffcalculator/tests/test_data/file1_file2_expected.txt"
    expected_content = None
    with open(path_to_expected) as file:
        expected_content = file.read()
    assert expected_content == actual


def test_with_empty_file_json_format():
    actual = None
    expected_content = None

    json_file1_path = "diffcalculator/tests/test_data/file1.json"
    empty_json_path = "diffcalculator/tests/test_data/empty.json"

    path_to_expected = "diffcalculator/tests/test_data/file1_and_empty_expected.txt"
    with open(path_to_expected) as file:
        expected_content = file.read()
    actual = diffcalc.get_diff(json_file1_path, empty_json_path)
    assert expected_content == actual

    path_to_expected = "diffcalculator/tests/test_data/empty_and_file1_expected.txt"
    with open(path_to_expected) as file:
        expected_content = file.read()
    actual = diffcalc.get_diff(empty_json_path, json_file1_path)
    assert expected_content == actual

    actual = diffcalc.get_diff(empty_json_path, empty_json_path)
    assert actual == "{}"


def test_normal_scenario_yaml_format():
    path_to_expected = "diffcalculator/tests/test_data/file1_file2_expected.txt"
    expected_content = None
    with open(path_to_expected) as file:
        expected_content = file.read()

    yaml_file1_path = "diffcalculator/tests/test_data/file1.yaml"
    yaml_file2_path = "diffcalculator/tests/test_data/file2.yaml"

    actual = diffcalc.get_diff(yaml_file1_path, yaml_file2_path)
    assert expected_content == actual


def test_with_empty_yaml():
    path_to_expected = "diffcalculator/tests/test_data/file1_and_empty_expected.txt"
    expected_content = None
    with open(path_to_expected) as file:
        expected_content = file.read()

    yaml_file1_path = "diffcalculator/tests/test_data/file1.yaml"
    yaml_empty = "diffcalculator/tests/test_data/empty.yaml"

    actual = diffcalc.get_diff(yaml_file1_path, yaml_empty)
    assert expected_content == actual

    path_to_expected = "diffcalculator/tests/test_data/empty_and_file1_expected.txt"
    expected_content = None
    with open(path_to_expected) as file:
        expected_content = file.read()
    actual = diffcalc.get_diff(yaml_empty, yaml_file1_path)
    assert expected_content == actual
