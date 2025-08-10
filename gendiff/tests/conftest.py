import pytest


@pytest.fixture
def file1_json():
    return "gendiff/tests/test_data/file1.json"


@pytest.fixture
def file2_json():
    return "gendiff/tests/test_data/file2.json"


@pytest.fixture
def file1_yaml():
    return "gendiff/tests/test_data/file1.yaml"


@pytest.fixture
def file2_yaml():
    return "gendiff/tests/test_data/file2.yaml"


@pytest.fixture
def complex_json_file1():
    return "gendiff/tests/test_data/complex_file1.json"


@pytest.fixture
def complex_json_file2():
    return "gendiff/tests/test_data/complex_file2.json"


@pytest.fixture
def complex_yaml_file1():
    return "gendiff/tests/test_data/complex_file1.yaml"


@pytest.fixture
def complex_yaml_file2():
    return "gendiff/tests/test_data/complex_file2.yaml"