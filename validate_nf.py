from pathlib import Path
import argparse

### SUB FUNCTIONS

# check existence of file given path object
def file_exists(path):
    return path.exists()

### MAIN FUNCTION

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of nextflow config to validate", type=str)
    args = parser.parse_args()

    path = Path(args.path)

    if file_exists(path):
        print("Valid")
    else:
        print("Invalid: File does not exist")

if __name__ == '__main__':
    main()
