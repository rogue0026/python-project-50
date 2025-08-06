import argparse


def setup_arg_parser():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("-f",
                        "--format",
                        help="set format of output",
                        default="stylish")
    parser.add_argument("first_file")
    parser.add_argument("second_file")

    return parser


def start_program():
    parser = setup_arg_parser()
    args = parser.parse_args()
    generate_diff(args.first_file, args.second_file)


def generate_diff(path1, path2, format_name="stylish"):
    file1 = read_file(path1)
    file2 = read_file(path2)
    diff_string = generate_string(file1, file2)
    print(diff_string)
