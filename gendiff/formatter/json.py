import json


def json_formatter(diff_tree: dict) -> str:
    return json.dumps(diff_tree, indent=4)
