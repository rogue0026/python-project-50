import argparse

from diffcalculator.internal.diffcalc import generate_diff


def setup_arg_parser():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("-f", "--format", help="set format of output")
    parser.add_argument("first_file")
    parser.add_argument("second_file")

    return parser


def start_program():
    parser = setup_arg_parser()
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)
