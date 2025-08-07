from diffcalc.parser.file_parser import read_file


def format_dict(d: dict, *, outer_indent: str="", sort_keys=True) -> str:
    inner_indent = " " * 4
    parts = []
    items = d.items()
    if sort_keys:
        items = sorted(items)
    for k, v in items:
        if isinstance(v, dict):
            nested_result = format_dict(v,
                                        outer_indent=outer_indent + inner_indent,
                                        sort_keys=sort_keys)
            part = f"{outer_indent}{inner_indent}{k}: {{\n{nested_result}"
            parts.append(part)
            parts.append(f"{outer_indent}{inner_indent}}}")
        else:
            part = f"{outer_indent}{inner_indent}{k}: {format_val(v)}"
            parts.append(part)
    return "\n".join(parts)


def format_val(val) -> str:
    if val is True:
        return "true"
    elif val is False:
        return "false"
    elif val is None:
        return "null"
    else:
        return str(val)


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


def build_diff(file1: dict, file2: dict) -> dict:
    all_keys = sorted(file1.keys() | file2.keys())
    diff_tree = dict()
    for key in all_keys:
        if key in file1 and key in file2:
            val1 = file1.get(key)
            val2 = file2.get(key)
            if isinstance(val1, dict) and isinstance(val2, dict):
                inner_result = build_diff(val1, val2)
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


def stylish(tree: dict, last_indent="") -> list:
    current_indent = "    " + last_indent
    result = list()
    for key, meta_info in sorted(tree.items()):
        state = get_key_state(meta_info)
        match state:
            case "nested":
                children = get_children(meta_info)
                result.append(f"{current_indent}{key}: {{")
                inner = stylish(children, last_indent=current_indent)
                result.extend(inner)
                result.append(f"{current_indent}}}")
            case "unchanged":
                old_value = get_old(meta_info)
                if isinstance(old_value, dict):
                    formatted_value = format_dict(old_value,
                                                  outer_indent=current_indent)
                    result.append(f"{current_indent}{key}: {{")
                    result.append(formatted_value)
                    result.append(f"{current_indent}}}")
                else:
                    formatted_value = format_val(old_value)
                    result.append(f"{current_indent}{key}: {formatted_value}")
            case "updated":
                old_value = get_old(meta_info)
                new_value = get_new(meta_info)
                if isinstance(old_value, dict):
                    formatted_old = format_dict(old_value,
                                                outer_indent=current_indent)
                    result.append(f"{current_indent[2:]}- {key}: {{")
                    result.append(formatted_old)
                    result.append(f"{current_indent}}}")
                else:
                    formatted_old = format_val(old_value)
                    result.append(f"{current_indent[2:]}- {key}: {formatted_old}")

                if isinstance(new_value, dict):
                    formatted_new = format_dict(new_value,
                                                outer_indent=current_indent)
                    result.append(f"{current_indent[2:]}+ {key}: {{")
                    result.append(formatted_new)
                    result.append(f"{current_indent}}}")
                else:
                    formatted_new = format_val(new_value)
                    result.append(f"{current_indent[2:]}+ {key}: {formatted_new}")

            case "removed":
                old_value = get_old(meta_info)
                if isinstance(old_value, dict):
                    formatted_old = format_dict(old_value,
                                                outer_indent=current_indent)
                    result.append(f"{current_indent[2:]}- {key}: {{")
                    result.append(formatted_old)
                    result.append(f"{current_indent}}}")
                else:
                    formatted_old = format_val(old_value)
                    formatted_old = f"{current_indent[2:]}- {key}: {formatted_old}"
                    result.append(formatted_old)
            case "added":
                new_value = get_new(meta_info)
                if isinstance(new_value, dict):
                    formatted_new = format_dict(new_value,
                                                outer_indent=current_indent)
                    result.append(f"{current_indent[2:]}+ {key}: {{")
                    result.append(formatted_new)
                    result.append(f"{current_indent}}}")
                else:
                    formatted_new = format_val(new_value)
                    formatted_new = f"{current_indent[2:]}+ {key}: {formatted_new}"
                    result.append(formatted_new)
    return result


f1 = read_file("diffcalc/tests/test_data/complex_file1.json")
f2 = read_file("diffcalc/tests/test_data/complex_file2.json")

diff = build_diff(f1, f2)
got = "\n".join(["{"] + stylish(diff) + ["}"])
with open("diffcalc/tests/test_data/complex_diff.txt") as file:
    expected = file.read()
    assert expected == got

