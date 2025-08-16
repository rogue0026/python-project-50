from gendiff import generate_diff


def test_on_simple_files(file1_json, file2_json):
    actual = generate_diff(file1_json, file2_json, format="json")
    with open("tests/test_data/file1_file2_json_expected.txt") as file:
        expected = file.read()
        assert actual == expected
