import json


def parse_file(path_to_file: str) -> dict:
    js_file = None
    try:
        js_file = json.load(open(path_to_file))
    except Exception as e:
        print(e)
    return js_file


def generate_diff(path_to_file1: str, path_to_file2: str):
    parsed_file1 = parse_file(path_to_file1)
    parsed_file2 = parse_file(path_to_file2)
    s1 = set(parsed_file1.items())
    s2 = set(parsed_file2.items())
    intersection = list(s1.intersection(s2))
    intersection = list(map(lambda el: ("  " + el[0], el[1]), intersection))
    s1_diff = list(map(lambda el: ("- " + el[0], el[1]), list(s1 - s2)))
    s2_diff = list(map(lambda el: ("+ " + el[0], el[1]), list(s2 - s1)))
    result_list = list()
    result_list.extend(intersection)
    result_list.extend(s1_diff)
    result_list.extend(s2_diff)
    result_list.sort(key=lambda elem: elem[0][2:])
    result = dict()
    for k, v in result_list:
        result[k] = v
    js = json.dumps(result, indent=2).replace("\"", "").replace(",", "")
    return js
