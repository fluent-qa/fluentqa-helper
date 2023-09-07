import json

from gema.enums import SourceType
from gema.source import Source


class Json(Source):
    type = SourceType.json

    def decode(self):
        return json.loads(self.content)
