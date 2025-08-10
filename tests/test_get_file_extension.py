import pytest

from gendiff.parser import get_file_extension


@pytest.fixture
def json_paths():
    return ["some/path/to.file/filename.json",
            "another.path/tofile/filename.json",
            "filename.json"]


@pytest.fixture
def yaml_paths():
    return ["some/path/to/filename.yaml",
            "some/path/to/file.name.yaml"]


@pytest.fixture
def yml_paths():
    return ["some/path/to/filename.yml",
            "some/path/to/file.name.yml"]


@pytest.fixture
def without_extension():
    return ["some/path/to/file",
            "another/path/to/ano.ther/file"]


def test_get_file_extension(json_paths,
                            yaml_paths,
                            yml_paths,
                            without_extension):

    for json_file_path in json_paths:
        assert get_file_extension(json_file_path) == "json"

    for yaml_file_path in yaml_paths:
        assert get_file_extension(yaml_file_path) == "yaml"

    for yml_path in yml_paths:
        assert get_file_extension(yml_path) == "yml"

    for file_without_extension in without_extension:
        assert get_file_extension(file_without_extension) == ""
