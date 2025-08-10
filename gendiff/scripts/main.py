import argparse

from gendiff.formatter import json, plain, stylish


def main():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("-f",
                        "--format",
                        help="set format of output",
                        default="stylish"
                        )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    args = parser.parse_args()
    match args.format:
        case "stylish":
            styled_diff = stylish.stylish(args.first_file, args.second_file)
            print(styled_diff)
        case "plain":
            plain_diff = plain.plain(args.first_file, args.second_file)
            print(plain_diff)
        case "json":
            json_diff = json.json_formatter(args.first_file, args.second_file)
            print(json_diff)


if __name__ == "__main__":
    main()
