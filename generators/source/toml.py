import toml

from generators.enums import SourceType
from generators.source import SourceStructureModel

class Toml(SourceStructureModel):
    type = SourceType.toml

    def decode(self):
        return toml.loads(self.content)
