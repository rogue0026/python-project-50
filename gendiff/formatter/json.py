import json

from gendiff.internal import diffcalc
from gendiff.parser.file_parser import read_file


def json_formatter(path1: str, path2: str) -> str:
    file1 = read_file(path1)
    file2 = read_file(path2)
    diff_tree = diffcalc.build_diff(file1, file2)
    result = walk_tree(diff_tree)
    return json.dumps(result, indent=4)


def walk_tree(diff_tree: dict) -> dict:
    diff = dict()
    for key, meta_info in diff_tree.items():
        state = diffcalc.get_key_state(meta_info)
        match state:
            case "nested":
                children = diffcalc.get_children(meta_info)
                inner_result = walk_tree(children)
                diff[key] = inner_result
            case "added":
                new_val = diffcalc.get_new(meta_info)
                diff[f"+{key}"] = new_val
            case "removed":
                old_val = diffcalc.get_old(meta_info)
                diff[f"-{key}"] = old_val
            case "updated":
                old_val = diffcalc.get_old(meta_info)
                new_val = diffcalc.get_new(meta_info)
                diff[f"-{key}"] = old_val
                diff[f"+{key}"] = new_val
            case "unchanged":
                old_val = diffcalc.get_old(meta_info)
                diff[f"{key}"] = old_val
    return diff
