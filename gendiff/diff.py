from gendiff.formatter import json, plain, stylish

from .parser import read_file


def build_meta(key_state, old_val, new_val, children) -> dict:
    return {
        "key_state": key_state,
        "old_val": old_val,
        "new_val": new_val,
        "children": children,
    }


def get_key_state(meta: dict) -> str:
    state = meta.get("key_state")
    if state is None:
        raise Exception("key state not found")
    return state


def get_old(meta: dict):
    old = meta.get("old_val")
    return old


def get_new(meta: dict):
    new = meta.get("new_val")
    return new


def get_children(meta: dict) -> dict:
    children = meta.get("children")
    return children


def walk_files(file1: dict, file2: dict) -> dict:
    all_keys = sorted(file1.keys() | file2.keys())
    diff_tree = dict()
    for key in all_keys:
        if key in file1 and key in file2:
            val1 = file1.get(key)
            val2 = file2.get(key)
            if isinstance(val1, dict) and isinstance(val2, dict):
                inner_result = walk_files(val1, val2)
                key_meta_info = build_meta("nested", None, None, inner_result)
                diff_tree[key] = key_meta_info
            elif val1 == val2:
                key_meta_info = build_meta("unchanged", val1, val2, None)
                diff_tree[key] = key_meta_info
            else:
                key_meta_info = build_meta("updated", val1, val2, None)
                diff_tree[key] = key_meta_info
        elif key in file1:
            val1 = file1.get(key)
            key_meta_info = build_meta("removed", val1, None, None)
            diff_tree[key] = key_meta_info
        else:
            val2 = file2.get(key)
            key_meta_info = build_meta("added", None, val2, None)
            diff_tree[key] = key_meta_info
    return diff_tree


def generate_diff(file_path1: str, file_path2: str, format="stylish") -> str:
    file1 = read_file(file_path1)
    file2 = read_file(file_path2)
    diff_tree = walk_files(file1, file2)
    result = ""
    match format:
        case "stylish":
            result = stylish.stylish(diff_tree)
        case "plain":
            result = plain.plain(diff_tree)
        case "json":
            result = json.json_formatter(diff_tree)
    return result
