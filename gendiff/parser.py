import json
from os import path

import yaml


def get_file_extension(path_to_file: str) -> str:
    _, ext = path.splitext(path_to_file)
    return ext[1:]


def read_file(path_to_file: str) -> dict:
    file_extension = get_file_extension(path_to_file)
    file_content = None
    match file_extension:
        case "json":
            with open(path_to_file) as file:
                file_content = json.load(file)
        case "yaml":
            with open(path_to_file) as file:
                file_content = yaml.safe_load(file)
        case "yml":
            with open(path_to_file) as file:
                file_content = yaml.safe_load(file)
    if file_content is None:
        file_content = {}
    return file_content
