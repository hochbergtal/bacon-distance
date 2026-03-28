import csv
from dataclasses import dataclass
from typing import Generator


@dataclass
class TitleActor:
    """Entry for actor who played in a title"""

    title_id: str
    actor_id: str


@dataclass
class IdName:
    """Entry for actor/title name and its ID"""

    id: str
    name: str


def iter_title_actors(
    title_principals_filename: str,
) -> Generator[TitleActor, None, None]:
    """Iterates over all title-actor entries in a dataset file.

    :param title_principals_filename: a tsv file of titles and their principals as presented in imdb
    :yields: an entry for an actor who played in a title
    """
    with open(title_principals_filename, "r") as tsvfile:
        principals_reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in principals_reader:
            if row["category"] == "actor":
                yield TitleActor(row["tconst"], row["nconst"])


def iter_title_names(title_basics_filename: str) -> Generator[IdName, None, None]:
    """Iterates over all title-name entries in a dataset file.

    :param title_basics_filename: a tsv file of titles and their basic info as presented in imdb
    :yields: an entry for a title ID and name
    """
    with open(title_basics_filename, "r") as tsvfile:
        basics_reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in basics_reader:
            yield IdName(row["tconst"], row["primaryTitle"])


def iter_actor_names(name_basics_filename: str) -> Generator[IdName, None, None]:
    """Iterates over all actor-name entries in a dataset file.

    :param name_basics_filename: a tsv file of people's names and their basic info as presented in imdb
    :yields: an entry for an actor ID and name
    """
    with open(name_basics_filename, "r") as tsvfile:
        basics_reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in basics_reader:
            yield IdName(row["nconst"], row["primaryName"])
