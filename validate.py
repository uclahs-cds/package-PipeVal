from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="full path of parameter", type=str)
args = parser.parse_args()
path = Path(args.path)

# check existence
if path.exists():
    print("File extension is: " + path.suffix)
else:
    print("File does not exist.")
