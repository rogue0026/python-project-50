from gendiff.internal import diffcalc
from gendiff.parser.file_parser import read_file


def format_dict(d: dict, *, out_indent: str = "", sort_keys=True) -> str:
    in_indent = " " * 4
    parts = []
    items = d.items()
    if sort_keys:
        items = sorted(items)
    for k, v in items:
        if isinstance(v, dict):
            nested_result = format_dict(v,
                                        out_indent=out_indent + in_indent,
                                        sort_keys=sort_keys)
            part = f"{out_indent}{in_indent}{k}: {{\n{nested_result}"
            parts.append(part)
            parts.append(f"{out_indent}{in_indent}}}")
        else:
            part = f"{out_indent}{in_indent}{k}: {format_val(v)}"
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


def formatter(tree: dict, last_indent="") -> list:
    cur_indent = "    " + last_indent
    result = list()
    for key, meta_info in sorted(tree.items()):
        state = diffcalc.get_key_state(meta_info)
        match state:
            case "nested":
                handle_nested(key, meta_info, result, cur_indent)
            case "unchanged":
                handle_unchanged(key, meta_info, result, cur_indent)
            case "updated":
                handle_updated(key, meta_info, result, cur_indent)
            case "removed":
                handle_removed(key, meta_info, result, cur_indent)
            case "added":
                handle_added(key, meta_info, result, cur_indent)
    return result


def handle_unchanged(key, meta_info, result: list, cur_indent):
    old_value = diffcalc.get_old(meta_info)
    if isinstance(old_value, dict):
        formatted_value = format_dict(old_value,
                                      out_indent=cur_indent)
        result.append(f"{cur_indent}{key}: {{")
        result.append(formatted_value)
        result.append(f"{cur_indent}}}")
    else:
        formatted_value = format_val(old_value)
        result.append(f"{cur_indent}{key}: {formatted_value}")


def handle_nested(key, meta_info, result: list, cur_indent):
    children = diffcalc.get_children(meta_info)
    result.append(f"{cur_indent}{key}: {{")
    inner = formatter(children, last_indent=cur_indent)
    result.extend(inner)
    result.append(f"{cur_indent}}}")


def handle_updated(key, meta_info, result: list, cur_indent):
    old_value = diffcalc.get_old(meta_info)
    new_value = diffcalc.get_new(meta_info)
    if isinstance(old_value, dict):
        formatted_old = format_dict(old_value,
                                    out_indent=cur_indent)
        result.append(f"{cur_indent[2:]}- {key}: {{")
        result.append(formatted_old)
        result.append(f"{cur_indent}}}")
    else:
        formatted_old = format_val(old_value)
        result.append(f"{cur_indent[2:]}- {key}: {formatted_old}")

    if isinstance(new_value, dict):
        formatted_new = format_dict(new_value,
                                    out_indent=cur_indent)
        result.append(f"{cur_indent[2:]}+ {key}: {{")
        result.append(formatted_new)
        result.append(f"{cur_indent}}}")
    else:
        formatted_new = format_val(new_value)
        result.append(f"{cur_indent[2:]}+ {key}: {formatted_new}")


def handle_removed(key, meta_info, result: list, cur_indent):
    old_value = diffcalc.get_old(meta_info)
    if isinstance(old_value, dict):
        formatted = format_dict(old_value,
                                out_indent=cur_indent)
        result.append(f"{cur_indent[2:]}- {key}: {{")
        result.append(formatted)
        result.append(f"{cur_indent}}}")
    else:
        formatted = format_val(old_value)
        formatted = f"{cur_indent[2:]}- {key}: {formatted}"
        result.append(formatted)


def handle_added(key, meta_info, result: list, cur_indent):
    new_value = diffcalc.get_new(meta_info)
    if isinstance(new_value, dict):
        formatted = format_dict(new_value,
                                out_indent=cur_indent)
        result.append(f"{cur_indent[2:]}+ {key}: {{")
        result.append(formatted)
        result.append(f"{cur_indent}}}")
    else:
        formatted = format_val(new_value)
        formatted = f"{cur_indent[2:]}+ {key}: {formatted}"
        result.append(formatted)


def stylish(file_path1: str, file_path2: str) -> str:
    file1 = read_file(file_path1)
    file2 = read_file(file_path2)
    diff_tree = diffcalc.build_diff(file1, file2)
    formatted_diff = formatter(diff_tree)
    return "\n".join(["{"] + formatted_diff + ["}"])