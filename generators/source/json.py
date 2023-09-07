import json

from generators.enums import SourceType
from generators.source import SourceStructureModel


class Json(SourceStructureModel):
    type = SourceType.json

    def decode(self):
        return json.loads(self.content)
