from typing import Any, Dict

from generators.api.models import StructureModel
from generators.enums import *
from generators.target import TargetStructureModel
from generators.type_loader import camel_to_snake


class Pydantic(TargetStructureModel):
    template_file = "pydantic.jinja2"
    type = TargetType.pydantic
    language = Language.python

    def __init__(
        self,
        model: StructureModel,
        source_type: SourceType,
        optional: bool = False,
        snake_case: bool = False,
    ):
        super().__init__(model, source_type)
        self.snake_case = snake_case
        self.optional = optional

    def _parse_model(self, imports: set[str], models: Dict[str, Any], model: StructureModel):
        fields = []
        for field in model.fields:
            name = field.name
            snake_case_name = name
            if self.snake_case:
                snake_case_name = camel_to_snake(name)
            if isinstance(field.type, StructureModel):
                type_ = f"'{name.title()}'"
                models[name.title()] = self._parse_model(imports, models, field.type)
            elif isinstance(field.type, list):
                imports.add("from typing import List")
                if isinstance(field.type[0], StructureModel):
                    type_ = f"List['{name.title()}']"
                    models[name.title()] = self._parse_model(imports, models, field.type[0])
                else:
                    type_ = f"List[{field.type[0].__name__}]"
            elif field.type is type(Any):
                imports.add("from typing import Any")
                type_ = "Any"
            else:
                type_ = field.type.__name__
            if self.optional:
                type_ = f"Optional[{type_}]"
                imports.add("from typing import Optional")
            if name != snake_case_name:
                imports.add("from pydantic import Field")
                field_str = f"{snake_case_name}: {type_} = Field(..., alias='{name}')"
            else:
                field_str = f"{snake_case_name}: {type_}"
            fields.append(field_str)
        return fields

    def render(self):
        model = self.model
        imports = set()
        models = {}
        models[self.model_name] = self._parse_model(imports, models, model)
        return self.template.render(models=models, imports=sorted(imports))
