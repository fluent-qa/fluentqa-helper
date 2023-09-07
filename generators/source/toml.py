import toml

from gema.enums import SourceType
from gema.source import Source


class Toml(Source):
    type = SourceType.toml

    def decode(self):
        return toml.loads(self.content)
