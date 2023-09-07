import yaml

from gema.enums import SourceType
from gema.source import Source


class Yaml(Source):
    type = SourceType.yaml

    def decode(self):
        return yaml.load(self.content, Loader=yaml.FullLoader)
