from typing import Any, Dict, Type

from gema.dest import Dest
from gema.enums import DestType, Language
from gema.schema import Model


class Rust(Dest):
    template_file = "rust.jinja2"
    type = DestType.rust
    language = Language.rust

    @classmethod
    def _type_convert(cls, type_: Type):
        if type_ is int:
            return "i64"
        if type_ is str or type_ is Any:
            return "String"
        if type_ is bool:
            return "bool"
        if type_ is float:
            return "f64"

    def _parse_model(self, models: Dict[str, Any], model: Model):
        fields = []
        for field in model.fields:
            name = field.name
            if isinstance(field.type, Model):
                type_ = f"{name.title()}"
                models[name.title()] = self._parse_model(models, field.type)
            elif isinstance(field.type, list):
                if isinstance(field.type[0], Model):
                    type_ = f"Vec<{name.title()}>"
                    models[name.title()] = self._parse_model(models, field.type[0])
                else:
                    type_ = f"Vec<{self._type_convert(field.type[0])}>"
            else:
                type_ = self._type_convert(field.type)

            field_str = f"{name}: {type_},"
            fields.append(field_str)
        return fields

    def render(self):
        model = self.model
        models = {}
        models[self.model_name] = self._parse_model(models, model)
        return self.template.render(models=models)
