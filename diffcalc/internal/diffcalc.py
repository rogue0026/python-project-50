def generate_string(file1: dict, file2: dict) -> str:
    return "\n".join(["{"] + compute_diff(file1, file2) + ["}"])


def compute_diff(file1: dict, file2: dict, depth=1) -> list:
    base_indent = "    "
    ind = base_indent * depth
    all_keys = sorted(list(file1.keys() | file2.keys()))
    diff = []
    for key in all_keys:
        if key in file1 and key in file2:
            val1 = file1.get(key)
            val2 = file2.get(key)
            if isinstance(val1, dict) and isinstance(val2, dict):
                diff.append(f"{ind}{key}: {{")
                nest_diff = compute_diff(val1, val2, depth + 1)
                diff.extend(nest_diff)
                diff.append(f"{ind}}}")
            elif val1 == val2:
                diff.append(f"{ind}{key}: {map_val(val1, ind, depth + 1)}")
            else:
                old = f"{ind[2:]}- {key}: {map_val(val1, ind, depth + 1)}"
                diff.append(old)
                new = f"{ind[2:]}+ {key}: {map_val(val2, ind, depth + 1)}"
                diff.append(new)
        elif key in file1:
            val1 = file1.get(key)
            old = f"{ind[2:]}- {key}: {map_val(val1, ind, depth + 1)}"
            diff.append(old)
        else:
            val2 = file2.get(key)
            new = f"{ind[2:]}+ {key}: {map_val(val2, ind, depth + 1)}"
            diff.append(new)
    return diff


def map_val(value, curly_brace_indent: str, depth=1) -> str:
    base_indent = "    "
    ind = base_indent * depth
    if value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return "null"
    elif isinstance(value, dict):
        result = ["{"]
        for k, v in value.items():
            if isinstance(v, dict):
                result.append(f"{ind}{k}: {map_val(v, ind, depth + 1)}")
            else:
                result.append(f"{ind}{k}: {v}")
        result.append(f"{curly_brace_indent}}}")
        return "\n".join(result)
    else:
        return str(value)