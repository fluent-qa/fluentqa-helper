import yaml
from generators.enums import SourceType
from generators.source import SourceStructureModel


class Yaml(SourceStructureModel):
    type = SourceType.yaml

    def decode(self):
        return yaml.load(self.content, Loader=yaml.FullLoader)
