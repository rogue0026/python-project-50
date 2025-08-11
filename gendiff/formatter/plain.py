
from gendiff import diff


def format_val(val) -> str:
    if val is True:
        return "true"
    elif val is False:
        return "false"
    elif val is None:
        return "null"
    elif isinstance(val, str):
        return f"'{val}'"
    elif isinstance(val, dict):
        return "[complex value]"
    else:
        return val


def walk_tree(diff_tree: dict, prop_name="") -> list:
    result = []
    for key, meta in sorted(diff_tree.items()):
        cur_prop = key
        if len(prop_name) > 0:
            cur_prop = f"{prop_name}.{key}"
        state = diff.get_key_state(meta)
        match state:
            case "nested":
                children = diff.get_children(meta)
                nested_results = walk_tree(children, cur_prop)
                result.extend(nested_results)
            case "added":
                new_value = diff.get_new(meta)
                val = format_val(new_value)
                s = f"Property '{cur_prop}' was added with value: {val}"
                result.append(s)
            case "removed":
                s = f"Property '{cur_prop}' was removed"
                result.append(s)
            case "updated":
                old = diff.get_old(meta)
                new = diff.get_new(meta)
                old = format_val(old)
                new = format_val(new)
                s = f"Property '{cur_prop}' was updated. From {old} to {new}"
                result.append(s)
    return result


def plain(diff_tree: dict) -> str:
    result = walk_tree(diff_tree)
    return "\n".join(result)
