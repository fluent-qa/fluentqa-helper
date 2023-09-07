from typing import Any, Union

from generators.api.models import StructureModel, FieldModel
from generators.enums import Base, SourceType


class SourceStructureModel(Base):
    type: SourceType

    def __init__(self, content: str):
        self.content = content

    def decode(self):
        raise NotImplementedError

    def get_model(self, content: Union[list, dict]) -> StructureModel:
        model = StructureModel(fields=[])
        if isinstance(content, list):
            item = content[0]
        else:
            item = content
        for k, v in item.items():
            if isinstance(v, dict):
                field = FieldModel(name=k, type=self.get_model(v))
            elif isinstance(v, list):
                if isinstance(v[0], dict):
                    field = FieldModel(name=k, type=[self.get_model(v)])
                else:
                    field = FieldModel(name=k, type=[type(v[0])])
            elif v is None:
                field = FieldModel(name=k, type=type(Any))
            else:
                field = FieldModel(name=k, type=type(v))
            model.fields.append(field)
        return model
