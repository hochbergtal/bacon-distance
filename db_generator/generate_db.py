import sys
from data_parser import DataParser

TITLE_PRINCIPALS_NAME = "title.principals.tsv"
TITLE_BASICS_NAME = "title.basics.tsv"
NAME_BASICS_NAME = "name.basics.tsv"
DEFAULT_RESULT_NAME = "db.json"


def main() -> None:
    if len(sys.argv) == 1:
        result_file_path = DEFAULT_RESULT_NAME
    elif len(sys.argv) == 2:
        result_file_path = sys.argv[1]
    else:
        print(f"Usage:\n{sys.argv[0]} [result file path]")
        return

    parser = DataParser(TITLE_PRINCIPALS_NAME, TITLE_BASICS_NAME, NAME_BASICS_NAME)
    parser.fill_ids()
    parser.fill_names()
    parser.dump_to_file(result_file_path)


if __name__ == "__main__":
    main()
