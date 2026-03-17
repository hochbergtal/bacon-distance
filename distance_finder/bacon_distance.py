import sqlite3
import sys
from typing import Union, Set, List, Tuple
from math import inf
from functools import lru_cache
from queue import Queue

DEFAULT_DB_PATH = "bacon.db"
TARGET_NAME = "Kevin Bacon"

TITLE_ACTOR_TABLE = "title_actor"
TITLE_ID_COL = "title_id"
ACTOR_ID_COL = "actor_id"

TITLES_TABLE = "titles"
ACTORS_TABLE = "actors"
ID_COL = "id"
NAME_COL = "name"


class DistanceFinder:
    def __init__(self, db_path: str) -> None:
        self.db_connection = sqlite3.connect(db_path)
        self.db_cursor = self.db_connection.cursor()

        try:
            self.db_cursor.execute(
                f"CREATE INDEX actor_index ON {TITLE_ACTOR_TABLE} ({ACTOR_ID_COL})"
            )
        except sqlite3.OperationalError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.db_connection.close()

    def get_bacon_distance(self, actor_name: str) -> Union[int, float]:
        (root_id,) = self.db_cursor.execute(
            f"SELECT {ID_COL} FROM {ACTORS_TABLE} WHERE {NAME_COL} = '{actor_name}'"
        ).fetchone()

        (target_id,) = self.db_cursor.execute(
            f"SELECT {ID_COL} FROM {ACTORS_TABLE} WHERE {NAME_COL} = '{TARGET_NAME}'"
        ).fetchone()

        return self.get_distance_dfs(root_id, target_id)

    def get_distance_dfs(self, root_id: str, target_id: str) -> Union[int, float]:
        actors_queue: Queue[Tuple[str, int]] = Queue()
        checked_actors: Set[str] = set()

        actors_queue.put((root_id, 0))
        while not actors_queue.empty():
            curr_actor, curr_distance = actors_queue.get()
            if curr_actor == target_id:
                return curr_distance

            checked_actors.add(curr_actor)

            adjacent_actors: List[Tuple[str]] = self.db_cursor.execute(
                f"""
                SELECT {ACTOR_ID_COL} FROM {TITLE_ACTOR_TABLE}
                WHERE {TITLE_ID_COL} IN (
                    SELECT {TITLE_ID_COL} FROM {TITLE_ACTOR_TABLE}
                    WHERE {ACTOR_ID_COL} = '{curr_actor}'
                )
                """
            ).fetchall()
            for (actor,) in adjacent_actors:
                if actor not in checked_actors:
                    actors_queue.put((actor, curr_distance + 1))

        return inf


def main() -> None:
    actor_name = sys.argv[1]
    with DistanceFinder(DEFAULT_DB_PATH) as distance_finder:
        distance = distance_finder.get_bacon_distance(actor_name)
        print(f"{actor_name}'s Bacon distance is {distance}")


if __name__ == "__main__":
    main()
