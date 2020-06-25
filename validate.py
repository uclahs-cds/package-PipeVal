import argparse
parser = argparse.ArgumentParser()
parser.add_argument("path", help="full path of parameter")
args = parser.parse_args()
print(args.path)