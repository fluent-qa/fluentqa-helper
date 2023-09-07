import xmltodict
from generators.enums import SourceType
from generators.source import SourceStructureModel

class Xml(SourceStructureModel):
    type = SourceType.xml

    def decode(self):
        return xmltodict.parse(self.content)
