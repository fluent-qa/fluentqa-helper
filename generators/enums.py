from enum import Enum

from enum import Enum


class Base:
    type: Enum


class SourceType(str, Enum):
    json = "json"
    xml = "xml"
    yaml = "yaml"
    toml = "toml"


class TargetType(str, Enum):
    pydantic = "pydantic"
    go = "go"
    rust = "rust"
    dataclass = "dataclass"
    typescript = "typescript"


class Language(str, Enum):
    python = "python"
    go = "go"
    rust = "rust"
    typescript = "typescript"


class DatabaseType(str, Enum):
    mysql = "mysql"
    postgresql = "postgresql"
