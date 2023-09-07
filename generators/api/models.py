from typing import List, Optional, Type, Union

from pydantic import BaseModel
from pydantic import Field as PydanticField

from generators.enums import *


class ConversionRequest(BaseModel):
    source_type: SourceType = PydanticField(SourceType.json)
    content: str = PydanticField(..., example='{"a": 1}')
    language: Language = PydanticField(..., example=Language.python)
    target_type: TargetType = PydanticField(..., example=TargetType.pydantic)
    config: Optional[dict]


class ConversionResponse(BaseModel):
    content: str


class FieldModel(BaseModel):
    name: str
    type: Union[Type, "StructureModel", List["StructureModel"], List["Type"]]


class StructureModel(BaseModel):
    fields: List[FieldModel]


FieldModel.update_forward_refs()
