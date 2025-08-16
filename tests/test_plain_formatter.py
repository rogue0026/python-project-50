from gendiff import generate_diff


def test_with_complex_json(complex_json_file1, complex_json_file2):
    actual = generate_diff(complex_json_file1,
                           complex_json_file2,
                           format="plain")
    with open("tests/test_data/complex_diff_plain.txt") as file:
        expected = file.read()
        assert actual == expected
