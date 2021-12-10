import argparse


def get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('students', type=str, help='Path to file with students')
    parser.add_argument('rooms', type=str, help='Path to file with rooms')
    parser.add_argument('format', type=str, help='Format for output file')
    parser.add_argument('output', type=str, help='Path to save the output file')
    return parser
