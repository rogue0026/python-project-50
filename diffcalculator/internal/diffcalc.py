import json
import os
from secrets import randbelow

import yaml


def _get_file_extension(p: str) -> str:
    _, tail = os.path.split(p)
    if len(tail) > 0:
        splitted = tail.split(".")
        return splitted[len(splitted) - 1]


def read_file(path_to_file: str):
    extension = _get_file_extension(path_to_file)
    result = None

    try:
        match extension:
            case "yaml":
                with open(path_to_file) as file:
                    result = yaml.safe_load(file)
            case "json":
                with open(path_to_file) as file:
                    result = json.load(file)
    except Exception as e:
        print(e)

    return result


def generate_diff_yaml(path_to_file1: str, path_to_file2: str):
    yaml1 = None
    yaml2 = None

    with open(path_to_file1) as f1:
        yaml1 = yaml.safe_load(f1)
    with open(path_to_file2) as f2:
        yaml2 = yaml.safe_load(f2)

    path_to_tmp_file1 = path_to_file1.replace(".yaml", "")
    path_to_tmp_file1 += f"{randbelow(1000000)}.json"
    path_to_tmp_file2 = path_to_file2.replace(".yaml", "")
    path_to_tmp_file2 += f"{randbelow(1000000)}.json"

    with open(path_to_tmp_file1, mode="w") as tmp_file1:
        tmp_file1.write(json.dumps(yaml1))
    with open(path_to_tmp_file2, mode="w") as tmp_file2:
        tmp_file2.write(json.dumps(yaml2))
    diff = generate_diff(path_to_tmp_file1, path_to_tmp_file2)
    os.remove(path_to_tmp_file1)
    os.remove(path_to_tmp_file2)
    return diff


def generate_diff(path1: str, path2: str):
    file1 = read_file(path1)
    file2 = read_file(path2)
    s1 = set(file1.items())
    s2 = set(file2.items())
    intersection = list(s1.intersection(s2))
    intersection = [("  " + el[0], el[1]) for el in intersection]
    s1_diff = [("- " + el[0], el[1]) for el in list(s1 - s2)]
    s2_diff = [("+ " + el[0], el[1]) for el in list(s2 - s1)]

    aggregated = list()
    aggregated.extend(intersection)
    aggregated.extend(s1_diff)
    aggregated.extend(s2_diff)

    aggregated.sort(key=lambda elem: elem[0][2:])
    # diff = {k: v for k, v in aggregated}
    # js = json.dumps(diff, indent=2).replace("\"", "").replace(",", "")
    return form_output(aggregated)


def form_output(lst: list) -> str:
    result = "{\n"
    for elem in lst:
        k, v = elem
        result += f"  {k}: {v}\n"
    result += "}"
    return result