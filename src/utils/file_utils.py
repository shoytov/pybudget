import os


def check_file_exist(file_path: str) -> bool:
    return os.path.exists(file_path)


def create_file(file_path: str) -> None:
    open(file_path, "w").close()
