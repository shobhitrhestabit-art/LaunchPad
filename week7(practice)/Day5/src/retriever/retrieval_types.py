from enum import Enum


class RetrievalMode(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    SQL = "sql"
