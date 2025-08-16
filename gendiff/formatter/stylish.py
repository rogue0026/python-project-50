from gendiff import diff


SIGN_INDENT = " " * 2
BASE_INDENT = " " * 4


def format_val(val, out_indent: str) -> str:
    if val is True:
        return "true"
    elif val is False:
        return "false"
    elif val is None:
        return "null"
    elif isinstance(val, dict):
        base_indent = " " * 4
        inner_indent = out_indent + base_indent
        dict_strings = ["{"]
        for key, value in sorted(val.items()):
            s = f"{inner_indent}{key}: {format_val(value, inner_indent)}"
            dict_strings.append(s)
        dict_strings.append(f"{out_indent}}}")
        return "\n".join(dict_strings)
    else:
        return str(val)


def stylish(diff_tree: dict, last_indent="") -> str:
    strings = ["{"]
    for key, meta_info in sorted(diff_tree.items()):
        key_state = diff.get_key_state(meta_info)
        new_val = diff.get_new(meta_info)
        new_val = format_val(new_val, last_indent + BASE_INDENT)
        old_val = diff.get_old(meta_info)
        old_val = format_val(old_val, last_indent + BASE_INDENT)
        match key_state:
            case "added":
                s_new = f"{last_indent}{SIGN_INDENT}+ {key}: {new_val}"
                strings.append(s_new)
            case "removed":
                s_old = f"{last_indent}{SIGN_INDENT}- {key}: {old_val}"
                strings.append(s_old)
            case "unchanged":
                s_old = f"{last_indent}{BASE_INDENT}{key}: {old_val}"
                strings.append(s_old)
            case "updated":
                s_old = f"{last_indent}{SIGN_INDENT}- {key}: {old_val}"
                s_new = f"{last_indent}{SIGN_INDENT}+ {key}: {new_val}"
                strings.append(s_old)
                strings.append(s_new)
            case "nested":
                children = diff.get_children(meta_info)
                inner_diff = stylish(children, last_indent + BASE_INDENT)
                s = f"{last_indent}{BASE_INDENT}{key}: {inner_diff}"
                strings.append(s)
    strings.append(f"{last_indent}}}")
    return "\n".join(strings)
