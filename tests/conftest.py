import pytest


@pytest.fixture
def file1_json():
    return "tests/test_data/file1.json"


@pytest.fixture
def file2_json():
    return "tests/test_data/file2.json"


@pytest.fixture
def complex_json_file1():
    return "tests/test_data/complex_file1.json"


@pytest.fixture
def complex_json_file2():
    return "tests/test_data/complex_file2.json"
