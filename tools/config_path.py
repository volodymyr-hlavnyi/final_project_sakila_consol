# config.py
import pathlib
from typing import Final

ROOT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]
DATABASE_DIR: Final[pathlib.Path] = ROOT_DIR.joinpath("db")
DATABASE_NAME: Final[str] = "data_sakila_bot.db"
# TRANSLATOR_DIR: Final[pathlib.Path] = ROOT_DIR.joinpath("vocabulary")
