import json

from gendiff import diff
from gendiff.parser import read_file


def json_formatter(path1: str, path2: str) -> str:
    file1 = read_file(path1)
    file2 = read_file(path2)
    diff_tree = diff.build_diff(file1, file2)
    result = walk_tree(diff_tree)
    return json.dumps(result, indent=4)


def walk_tree(diff_tree: dict) -> dict:
    result = dict()
    for key, meta_info in diff_tree.items():
        state = diff.get_key_state(meta_info)
        match state:
            case "nested":
                children = diff.get_children(meta_info)
                inner_result = walk_tree(children)
                result[key] = inner_result
            case "added":
                new_val = diff.get_new(meta_info)
                result[f"+{key}"] = new_val
            case "removed":
                old_val = diff.get_old(meta_info)
                result[f"-{key}"] = old_val
            case "updated":
                old_val = diff.get_old(meta_info)
                new_val = diff.get_new(meta_info)
                result[f"-{key}"] = old_val
                result[f"+{key}"] = new_val
            case "unchanged":
                old_val = diff.get_old(meta_info)
                result[f"{key}"] = old_val
    return result
