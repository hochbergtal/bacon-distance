import sqlite3
import sys
from typing import Union, Set, List
from math import inf

DEFAULT_DB_PATH = "bacon.db"
TARGET_NAME = "Kevin Bacon"

TITLE_ACTOR_TABLE = "title_actor"
TITLE_ID_COL = "title_id"
ACTOR_ID_COL = "actor_id"

TITLES_TABLE = "titles"
ACTORS_TABLE = "actors"
ID_COL = "id"
NAME_COL = "name"


def get_distance(
    root_id: str,
    target_id: str,
    db_cursor: sqlite3.Cursor,
    passed_ids: Set[str] = set(),
) -> Union[int, float]:
    if root_id == target_id:
        return 0

    adjacent_distances: List[Union[int, float]] = []

    titles_played_in = db_cursor.execute(
        f"SELECT {TITLE_ID_COL} FROM {TITLE_ACTOR_TABLE} WHERE {ACTOR_ID_COL} = '{root_id}'"
    ).fetchall()
    for (title,) in titles_played_in:
        if title in passed_ids:
            continue

        passed_ids.add(title)
        cast = db_cursor.execute(
            f"SELECT {ACTOR_ID_COL} FROM {TITLE_ACTOR_TABLE} WHERE {TITLE_ID_COL} = '{title}'"
        ).fetchall()
        for (actor,) in cast:
            if actor == root_id or actor in passed_ids:
                continue

            passed_ids.add(actor)
            adjacent_distances.append(
                get_distance(actor, target_id, db_cursor, passed_ids)
            )
            passed_ids.remove(actor)
        passed_ids.remove(title)

    if len(adjacent_distances) > 0:
        return min(adjacent_distances) + 1
    return inf


def main() -> None:
    root_actor_name = sys.argv[1]

    db_connection = sqlite3.connect(DEFAULT_DB_PATH)
    db_cursor = db_connection.cursor()

    (root_id,) = db_cursor.execute(
        f"SELECT {ID_COL} FROM {ACTORS_TABLE} WHERE {NAME_COL} = '{root_actor_name}'"
    ).fetchone()
    (target_id,) = db_cursor.execute(
        f"SELECT {ID_COL} FROM {ACTORS_TABLE} WHERE {NAME_COL} = '{TARGET_NAME}'"
    ).fetchone()

    print(f"root: {root_id}\ntarget: {target_id}")
    distance = get_distance(root_id, target_id, db_cursor)
    print(f"{root_actor_name}'s distance from {TARGET_NAME} is {distance}")

    db_cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
