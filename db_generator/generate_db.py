import sys
from data_parser import DataParser

TITLE_PRINCIPALS_NAME = "title.principals.tsv"
TITLE_BASICS_NAME = "title.basics.tsv"
NAME_BASICS_NAME = "name.basics.tsv"
DEFAULT_RESULT_NAME = "bacon.db"


def main() -> None:
    """Read the TVS dataset files and create an sqlite DB file from it.
    Assumes CWD has files with the global file names. If a command-line arg is given it's the result file path, otherwise it's "bacon.db".
    """
    if len(sys.argv) == 1:
        result_file_path = DEFAULT_RESULT_NAME
    elif len(sys.argv) == 2:
        result_file_path = sys.argv[1]
    else:
        print(f"Usage:\npython {sys.argv[0]} [result file path]")
        return

    with DataParser(
        result_file_path, TITLE_PRINCIPALS_NAME, TITLE_BASICS_NAME, NAME_BASICS_NAME
    ) as parser:
        print("DB generation started.")
        print("filling titles and actors ID...")
        parser.fill_ids()
        print("filling title names...")
        parser.fill_title_names()
        print("filling actor names...")
        parser.fill_actor_names()


if __name__ == "__main__":
    main()
