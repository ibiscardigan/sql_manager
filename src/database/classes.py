# Standard Library Imports
from dataclasses import dataclass

# Third Party Library Imports

# Local Library Imports

# Configure Logging


@dataclass
class field():
    name: str
    type: str
    length: int = None
    default: str = None
    null: bool = True
    primary: bool = False
    increment: bool = None


@dataclass
class table():
    name: str
    fields: list = None


@dataclass
class database():
    name: str
    env: str = None
    tables: list = None
