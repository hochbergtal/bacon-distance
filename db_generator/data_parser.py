import json
from dataclasses import dataclass, asdict
from typing import Dict, List
from dataset_api import iter_title_actors, iter_title_names, iter_actor_names


@dataclass
class TitleData:
    actors: List[str]
    name: str = ""


@dataclass
class ActorData:
    titles: List[str]
    name: str = ""


@dataclass
class TitleActorsData:
    titles: Dict[str, TitleData]
    actors: Dict[str, ActorData]


class DataParser:
    def __init__(
        self, title_principals: str, title_basics: str, name_basics: str
    ) -> None:
        self.data = TitleActorsData({}, {})
        self.title_principals = title_principals
        self.title_basics = title_basics
        self.name_basics = name_basics

    def fill_ids(self) -> None:
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
        for title_name in iter_title_names(self.title_basics):
            self.data.titles[title_name.id].name = title_name.name

        for actor_name in iter_actor_names(self.name_basics):
            self.data.actors[actor_name.id].name = actor_name.name

    def dump_to_file(self, path: str) -> None:
        with open(path, "w") as dump_file:
            json.dump(asdict(self.data), dump_file)
