import json
from dataclasses import dataclass, asdict
from typing import Dict, List
from dataset_api import iter_title_actors, iter_title_names, iter_actor_names


@dataclass
class TitleData:
    """Entry for title's name and actors list"""

    actors: List[str]
    name: str = ""


@dataclass
class ActorData:
    """Entry for actor's name and movie they're featured in"""

    titles: List[str]
    name: str = ""


@dataclass
class TitleActorsData:
    """A json-like dataclass of all titles with their names and actors, and actors with their names and featured titles"""

    titles: Dict[str, TitleData]
    actors: Dict[str, ActorData]


class DataParser:
    """A class for creating, filling and dumping the database.

    :param title_principals: path to the file that connects actors and titles IDs
    :param title_basics: path to the file that titles' IDs and names
    :param name_basics: path to the file that actors' IDs and names
    """

    def __init__(
        self, title_principals: str, title_basics: str, name_basics: str
    ) -> None:
        self.data = TitleActorsData({}, {})
        self.title_principals = title_principals
        self.title_basics = title_basics
        self.name_basics = name_basics

    def fill_ids(self) -> None:
        """Fill the titles' and actors' IDs from the given files to the data."""
        for title_actor in iter_title_actors(self.title_principals):
            if title_actor.title_id in self.data.titles:
                self.data.titles[title_actor.title_id].actors.append(
                    title_actor.actor_id
                )
            else:
                self.data.titles[title_actor.title_id] = TitleData(
                    [title_actor.actor_id]
                )

            if title_actor.actor_id in self.data.actors:
                self.data.actors[title_actor.actor_id].titles.append(
                    title_actor.title_id
                )
            else:
                self.data.actors[title_actor.actor_id] = ActorData(
                    [title_actor.title_id]
                )

    def fill_names(self) -> None:
        """Fill the titles' and actors' names from the given files to the data."""
        for title_name in iter_title_names(self.title_basics):
            if title_name.id in self.data.titles:
                self.data.titles[title_name.id].name = title_name.name

        for actor_name in iter_actor_names(self.name_basics):
            if actor_name.id in self.data.actors:
                self.data.actors[actor_name.id].name = actor_name.name

    def dump_to_file(self, path: str) -> None:
        """Dump the saved data to the given file in a JSON format.

        :param path: the path of the file
        """
        with open(path, "w") as dump_file:
            json.dump(asdict(self.data), dump_file)
