import csv
from dataclasses import dataclass
from typing import Generator


@dataclass
class TitleActor:
    title_id: str
    actor_id: str


@dataclass
class IdName:
    id: str
    name: str


def iter_title_actors(
    title_principals_filename: str,
) -> Generator[TitleActor, None, None]:
    with open(title_principals_filename, "r") as tsvfile:
        principals_reader = csv.reader(tsvfile, delimiter="\t")
        next(principals_reader)
        for row in principals_reader:
            if row[3] == "actor":
                yield TitleActor(row[0], row[2])


def iter_title_names(title_basics_filename: str) -> Generator[IdName, None, None]:
    with open(title_basics_filename, "r") as tsvfile:
        basics_reader = csv.reader(tsvfile, delimiter="\t")
        next(basics_reader)
        for row in basics_reader:
            yield IdName(row[0], row[2])


def iter_actor_names(name_basics_filename: str) -> Generator[IdName, None, None]:
    with open(name_basics_filename, "r") as tsvfile:
        basics_reader = csv.reader(tsvfile, delimiter="\t")
        next(basics_reader)
        for row in basics_reader:
            yield IdName(row[0], row[1])
