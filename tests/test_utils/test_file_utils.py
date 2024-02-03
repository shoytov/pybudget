import os

import pytest

from src.utils.file_utils import check_file_exist, create_file


class TestFileUtils:
    file_path_exist = "test.txt"
    path_to_create_file = "created.txt"

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        with open(self.file_path_exist, "w") as test_file:
            test_file.write("")

    @pytest.fixture(scope="session", autouse=True)
    def teardown(self):
        yield None
        os.remove(self.file_path_exist)
        os.remove(self.path_to_create_file)

    @pytest.mark.parametrize("file_path, result", ((file_path_exist, True), ("123.txt", False)))
    def test_check_file_exist(self, file_path, result):
        assert check_file_exist(file_path) is result

    def test_create_file(self):
        create_file(self.path_to_create_file)
        assert check_file_exist(self.path_to_create_file) is True
