from typing import Any, Dict, Type

from generators.enums import *
from generators.source import SourceStructureModel
from generators.target import TargetStructureModel


class Typescript(TargetStructureModel):
    template_file = "typescript.jinja2"
    type = TargetType.typescript
    language = Language.typescript

    @classmethod
    def _type_convert(cls, type_: Type):
        if type_ is int:
            return "number"
        if type_ is str or type_ is Any:
            return "string"
        if type_ is bool:
            return "boolean"
        if type_ is float:
            return "number"

    def _parse_model(self, models: Dict[str, Any], model: SourceStructureModel):
        fields = []
        for field in model.fields:
            name = field.name
            if isinstance(field.type, SourceStructureModel):
                type_ = f"{name.title()}"
                models[name.title()] = self._parse_model(models, field.type)
            elif isinstance(field.type, list):
                if isinstance(field.type[0], SourceStructureModel):
                    type_ = f"Array<{name.title()}>"
                    models[name.title()] = self._parse_model(models, field.type[0])
                else:
                    type_ = f"Array<{self._type_convert(field.type[0])}>"
            elif field.type is type(Any):
                type_ = "any"
            else:
                type_ = self._type_convert(field.type)

            field_str = f"{name}: {type_};"
            fields.append(field_str)
        return fields

    def render(self):
        model = self.model
        models = {}
        models[self.model_name] = self._parse_model(models, model)
        return self.template.render(models=models)
