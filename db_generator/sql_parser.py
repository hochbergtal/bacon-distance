import sqlite3
from dataset_api import iter_title_actors, iter_title_names, iter_actor_names


class DataParser:
    """A class for creating, filling and dumping the database.

    :param title_principals: path to the file that connects actors and titles IDs
    :param title_basics: path to the file that titles' IDs and names
    :param name_basics: path to the file that actors' IDs and names
    """

    def __init__(
        self, db_name: str, title_principals: str, title_basics: str, name_basics: str
    ) -> None:
        self.title_principals = title_principals
        self.title_basics = title_basics
        self.name_basics = name_basics

        self.db_connection = sqlite3.connect(db_name)
        self.db_cursor = self.db_connection.cursor()

        self.db_cursor.execute(
            f"""
            CREATE TABLE title_actor (
                title_id varchar(255),
                actor_id varchar(255)
            )
            """
        )
        self.db_cursor.execute(
            """
            CREATE TABLE titles (
                id varchar(255) UNIQUE,
                name varchar(255)
            )
            """
        )
        self.db_cursor.execute(
            """
            CREATE TABLE actors (
                id varchar(255) UNIQUE,
                name varchar(255)
            )
            """
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.db_connection.commit()
        self.db_cursor.close()
        self.db_connection.close()

    def fill_ids(self) -> None:
        """Fill the titles' and actors' IDs from the given files to the data."""
        for title_actor in iter_title_actors(self.title_principals):
            self.db_cursor.execute(
                f"""
                INSERT INTO title_actor VALUES (
                    '{title_actor.title_id}', '{title_actor.actor_id}'               
                )
                """
            )

            try:
                self.db_cursor.execute(
                    f"""
                    INSERT INTO titles VALUES (
                        '{title_actor.title_id}', null                  
                    )
                    """
                )
            except sqlite3.IntegrityError:
                pass

            try:
                self.db_cursor.execute(
                    f"""
                    INSERT INTO actors VALUES (
                        '{title_actor.actor_id}', null                  
                    )
                    """
                )
            except sqlite3.IntegrityError:
                pass

    def fill_title_names(self) -> None:
        """Fill the titles' and actors' names from the given files to the data."""
        for title_name in iter_title_names(self.title_basics):
            self.db_cursor.execute(
                f"""
                UPDATE titles
                SET name = '{title_name.name}'
                WHERE id = '{title_name.id}'
                """
            )

    def fill_actor_names(self) -> None:
        """Fill the titles' and actors' names from the given files to the data."""
        for actor_name in iter_actor_names(self.name_basics):
            self.db_cursor.execute(
                f"""
                UPDATE actors
                SET name = '{actor_name.name}'
                WHERE id = '{actor_name.id}'
                """
            )
