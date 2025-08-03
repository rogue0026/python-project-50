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


def sort_complex_file(complex_file: dict):
    first_file_keys = sorted(complex_file.keys(), key=lambda e: e)
    file_sorted = dict()
    for current_key in first_file_keys:
        value = complex_file[current_key]
        if isinstance(value, dict):
            file_sorted[current_key] = sort_complex_file(value)
        else:
            file_sorted[current_key] = value
    js = json.dumps(file_sorted)
    js = js.replace('"', "")
    js = js.replace(",", "")
    return js


def get_diff_modernized(file1: dict, file2: dict) -> dict:
    shared_keys = sorted(file1.keys() | file2.keys())
    result = dict()
    for key in shared_keys:
        if key in file1 and key in file2:
            val_from_file1 = file1[key]
            val_from_file2 = file2[key]
            if not isinstance(val_from_file1, dict) and not isinstance(
                val_from_file2, dict
            ):
                if val_from_file1 != val_from_file2:
                    result[f"- {key}"] = val_from_file1
                    result[f"+ {key}"] = val_from_file2
                else:
                    result[key] = val_from_file1
            if isinstance(val_from_file1, dict) and isinstance(val_from_file2, dict):
                result[key] = get_diff_modernized(val_from_file1, val_from_file2)
            else:
                result[f"- {key}"] = val_from_file1
                result[f"+ {key}"] = val_from_file2
        else:
            if key in file1 and key not in file2:
                val_from_file1 = file1[key]
                result[f"- {key}"] = val_from_file1
            elif key in file2 and key not in file1:
                val_from_file2 = file2[key]
                result[f"+ {key}"] = val_from_file2
    return result
