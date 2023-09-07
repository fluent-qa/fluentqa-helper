from typing import Any, Dict

from generators.api.models import StructureModel
from generators.enums import *
from generators.target import TargetStructureModel


class Dataclass(TargetStructureModel):
    template_file = "dataclass.jinja2"
    type = TargetType.dataclass
    language = Language.python

    def _parse_model(self, imports: set[str], models: Dict[str, Any], model: StructureModel):
        fields = []
        for field in model.fields:
            name = field.name
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
            field_str = f"{name}: {type_}"
            fields.append(field_str)
        return fields

    def render(self):
        model = self.model
        imports = set()
        models = {}
        models[self.model_name] = self._parse_model(imports, models, model)
        return self.template.render(models=models, imports=sorted(imports))
