import argparse
import json


def run_gendiff():
    parser = argparse.ArgumentParser(
            description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("-f", "--format", help="set format of output")
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.parse_args()


def parse_file(path_to_file: str) -> str | None:
    js_file = None
    try:
        js_file = json.load(open(path_to_file))
    except Exception as e:
        print(e)
    return js_file
