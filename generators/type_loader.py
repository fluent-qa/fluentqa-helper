import importlib
import inspect
import pkgutil
import re

from generators import source, target
from generators.enums import Language
from generators.source import SourceStructureModel
from generators.target import TargetStructureModel


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def _discover_source_type():
    ret = {}
    for m in pkgutil.iter_modules(source.__path__):
        mod = importlib.import_module(f"{source.__name__}.{m.name}")
        for name, member in inspect.getmembers(mod, inspect.isclass):
            if issubclass(member, SourceStructureModel) and member is not SourceStructureModel:
                ret[member.type] = member
    return ret


def _discover_target_type():
    ret = {}
    for m in pkgutil.iter_modules(target.__path__):
        mod = importlib.import_module(f"{target.__name__}.{m.name}")
        for name, member in inspect.getmembers(mod, inspect.isclass):
            if issubclass(member, TargetStructureModel) and member is not TargetStructureModel:
                ret.setdefault(member.language, {})[member.type] = member
    return ret


source_cls_map = _discover_source_type()
target_cls_map = _discover_target_type()


def get_source_cls(type_: SourceStructureModel):
    return source_cls_map[type_]


def get_target_cls(language: Language, type_: TargetStructureModel):
    return target_cls_map[language][type_]
