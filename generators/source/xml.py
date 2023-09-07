import xmltodict

from gema.enums import SourceType
from gema.source import Source


class Xml(Source):
    type = SourceType.xml

    def decode(self):
        return xmltodict.parse(self.content)
