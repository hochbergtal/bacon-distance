import sqlite3
from dataset_api import iter_title_actors, iter_title_names, iter_actor_names

TITLE_ACTOR_TABLE = "title_actor"
TITLE_ID_COL = "title_id"
ACTOR_ID_COL = "actor_id"

TITLES_TABLE = "titles"
ACTORS_TABLE = "actors"
ID_COL = "id"
NAME_COL = "name"


class DataParser:
    """A class for creating and filling the database, as an sqlite DB.
    Initiating this class creates a new DB (assuming there's no DB with the given path), and three empty tables:
    title_actor - IDs of titles and actors playing in them
    titles - IDs and names of titles
    actors - IDs and names of actors

    :param db_path: path to the DB file to create
    :param title_principals: path to the file that connects actors and titles IDs
    :param title_basics: path to the file that titles' IDs and names
    :param name_basics: path to the file that actors' IDs and names
    """

    def __init__(
        self, db_path: str, title_principals: str, title_basics: str, name_basics: str
    ) -> None:
        self.title_principals = title_principals
        self.title_basics = title_basics
        self.name_basics = name_basics

        self.db_connection = sqlite3.connect(db_path)
        self.db_cursor = self.db_connection.cursor()

        self.db_cursor.execute(
            f"""
            CREATE TABLE {TITLE_ACTOR_TABLE} (
                {TITLE_ID_COL} varchar(255),
                {ACTOR_ID_COL} varchar(255)
            )
            """
        )
        self.db_cursor.execute(
            f"""
            CREATE TABLE {TITLES_TABLE} (
                {ID_COL} varchar(255) UNIQUE,
                {NAME_COL} varchar(255)
            )
            """
        )
        self.db_cursor.execute(
            f"""
            CREATE TABLE {ACTORS_TABLE} (
                {ID_COL} varchar(255) UNIQUE,
                {NAME_COL} varchar(255)
            )
            """
        )

    def __enter__(self):
        """When entering the context manager, return itself."""
        return self

    def __exit__(self, exc_type, exc, tb):
        """When exiting the context manager, commit changes and close connection"""
        self.db_connection.commit()
        self.db_cursor.close()
        self.db_connection.close()

    def fill_ids(self) -> None:
        """Fill the titles' and actors' IDs from the given files to the DB."""
        for i, title_actor in enumerate(iter_title_actors(self.title_principals)):
            self.db_cursor.execute(
                f"""
                INSERT INTO {TITLE_ACTOR_TABLE} VALUES (
                    '{title_actor.title_id}', '{title_actor.actor_id}'               
                )
                """
            )

            self.db_cursor.execute(
                f"""
                INSERT OR IGNORE INTO {TITLES_TABLE} VALUES (
                    '{title_actor.title_id}', null                  
                )
                """
            )

            self.db_cursor.execute(
                f"""
                INSERT OR IGNORE INTO {ACTORS_TABLE} VALUES (
                    '{title_actor.actor_id}', null                  
                )
                """
            )

            if i == 2_000_000:
                return

    def fill_title_names(self) -> None:
        """Fill the titles' names from the given files to the DB."""
        for i, title_name in enumerate(iter_title_names(self.title_basics)):
            self.db_cursor.execute(
                f"""
                UPDATE {TITLES_TABLE}
                SET {NAME_COL} = '{title_name.name.replace("'", "\"")}'
                WHERE {ID_COL} = '{title_name.id}'
                """
            )

            if i == 4_000_000:
                return

    def fill_actor_names(self) -> None:
        """Fill the actors' names from the given files to the DB."""
        for i, actor_name in enumerate(iter_actor_names(self.name_basics)):
            self.db_cursor.execute(
                f"""
                UPDATE {ACTORS_TABLE}
                SET {NAME_COL} = '{actor_name.name.replace("'", "\"")}'
                WHERE {ID_COL} = '{actor_name.id}'
                """
            )

            if i == 4_000_000:
                return
