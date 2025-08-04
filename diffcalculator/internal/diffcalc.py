import json
import yaml

import os


def get_file_extension(path_to_file: str) -> str:
    _, ext = os.path.splitext(path_to_file)
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
        file_content = dict()
    return file_content


def format_value(value, curly_brace_indent: str, depth=1) -> str:
    base_indent = "    "
    computed_indent = base_indent * depth
    if value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return "null"
    elif isinstance(value, dict):
        result = ["{"]
        for k, v in value.items():
            if isinstance(v, dict):
                result.append(f"{computed_indent}{k}: {format_value(v, computed_indent, depth + 1)}")
            else:
                result.append(f"{computed_indent}{k}: {v}")
        result.append(f"{curly_brace_indent}}}")
        return "\n".join(result)
    else:
        return str(value)


def stylish(file1: dict, file2: dict) -> str:
    return "\n".join(["{"] + get_diff(file1, file2) + ["}"])


def get_diff(file1: dict, file2: dict, depth=1) -> list:
    base_indent = "    "
    computed_indent = base_indent * depth
    all_keys = sorted(list(file1.keys() | file2.keys()))
    diff = []
    for key in all_keys:
        if key in file1 and key in file2:
            val_file1 = file1.get(key)
            val_file2 = file2.get(key)
            if isinstance(val_file1, dict) and isinstance(val_file2, dict):
                diff.append(f"{computed_indent}{key}: {{")
                nest_diff = get_diff(val_file1, val_file2, depth + 1)
                diff.extend(nest_diff)
                diff.append(f"{computed_indent}}}")
            elif val_file1 == val_file2:
                diff.append(f"{computed_indent}{key}: {format_value(val_file1, computed_indent, depth+1)}")
            else:
                diff.append(f"{computed_indent[2:]}- {key}: {format_value(val_file1, computed_indent, depth+1)}")
                diff.append(f"{computed_indent[2:]}+ {key}: {format_value(val_file2, computed_indent, depth+1)}")
        elif key in file1:
            val_file1 = file1.get(key)
            diff.append(f"{computed_indent[2:]}- {key}: {format_value(val_file1, computed_indent, depth+1)}")
        else:
            val_file2 = file2.get(key)
            diff.append(f"{computed_indent[2:]}+ {key}: {format_value(val_file2, computed_indent, depth+1)}")
    return diff
