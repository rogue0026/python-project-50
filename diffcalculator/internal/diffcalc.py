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


def get_diff(first_path: str, second_path: str):
    first_file_content = read_file(first_path)
    second_file_content = read_file(second_path)
    s1 = set(first_file_content.items())
    s2 = set(second_file_content.items())
    files_intersection = [("  " + el[0], el[1]) for el in s1 & s2]
    first_file_diff = [("- " + el[0], el[1]) for el in list(s1 - s2)]
    second_file_diff = [("+ " + el[0], el[1]) for el in list(s2 - s1)]
    agg = list()
    agg.extend(files_intersection)
    agg.extend(first_file_diff)
    agg.extend(second_file_diff)
    agg.sort(key=lambda item: item[0][2:])
    diff = dict()
    for elem in agg:
        k, v = elem
        diff[k] = v
    output = json.dumps(diff, indent=2)
    output = output.replace('"', "")
    output = output.replace(",", "")
    return output


def get_diff_v2(file1: dict, file2: dict, depth=None) -> list:
    if depth is None:
        depth = 2
    all_keys = sorted(file1.keys() | file2.keys())
    result = list()
    for cur_key in all_keys:
        if cur_key in file1 and cur_key in file2:
            val_file1 = file1.get(cur_key)
            val_file2 = file2.get(cur_key)
            if isinstance(val_file1, dict) and isinstance(val_file2, dict):
                result.append(f"{' ' * depth}  {cur_key}: {{")
                nested_result = get_diff_v2(val_file1, val_file2, depth + 2)
                result.extend(nested_result)
                result.append(f"{' ' * (depth - 2)}}}")
            elif val_file1 == val_file2:
                result.append(f"{' ' * depth}  {cur_key}: {format_value(val_file1)}")
            else:
                result.append(f"{' ' * depth}- {cur_key}: {format_value(val_file1)}")
                result.append(f"{' ' * depth}+ {cur_key}: {format_value(val_file2)}")
        elif cur_key in file1:
            val_file1 = file1.get(cur_key)
            result.append(f"{' ' * depth}- {cur_key}: {format_value(val_file1)}")
        else:
            val_file2 = file2.get(cur_key)
            result.append(f"{' ' * depth}+ {cur_key}: {format_value(val_file2)}")
    return result


def format_value(value, depth=None) -> str:
    if depth is None:
        depth = 2
    if value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return "null"
    elif isinstance(value, dict):
        result = ["{"]
        for k, v in sorted(value.items()):
            if not isinstance(v, dict):
                result.append(f"{' ' * depth}{k}: {v}")
            else:
                result.append(f"{' ' * depth}{k}: {format_value(v, depth + 2)}")
        result.append(f"{' ' * (depth - 2)}}}")
        return "\n".join(result)
    else:
        return str(value)