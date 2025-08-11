from gendiff import diff


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
    base_indent = " " * 4
    sign_indent = " " * 2
    strings = []
    strings.append("{")
    for key, meta_info in sorted(diff_tree.items()):
        key_state = diff.get_key_state(meta_info)
        match key_state:
            case "added":
                new_val = diff.get_new(meta_info)
                new_val = format_val(new_val, last_indent + base_indent)
                s = f"{last_indent}{sign_indent}+ {key}: {new_val}"
                strings.append(s)
            case "removed":
                old_val = diff.get_old(meta_info)
                old_val = format_val(old_val, last_indent + base_indent)
                s = f"{last_indent}{sign_indent}- {key}: {old_val}"
                strings.append(s)
            case "unchanged":
                old_val = diff.get_old(meta_info)
                old_val = format_val(old_val, last_indent + base_indent)
                s = f"{last_indent}{base_indent}{key}: {old_val}"
                strings.append(s)
            case "updated":
                old_val = diff.get_old(meta_info)
                old_val = format_val(old_val, last_indent + base_indent)
                old_s = f"{last_indent}{sign_indent}- {key}: {old_val}"
                new_val = diff.get_new(meta_info)
                new_val = format_val(new_val, last_indent + base_indent)
                new_s = f"{last_indent}{sign_indent}+ {key}: {new_val}"
                strings.append(old_s)
                strings.append(new_s)
            case "nested":
                children = diff.get_children(meta_info)
                inner_diff = stylish(children, last_indent + base_indent)
                s = f"{last_indent}{base_indent}{key}: {inner_diff}"
                strings.append(s)
    strings.append(f"{last_indent}}}")
    return "\n".join(strings)
