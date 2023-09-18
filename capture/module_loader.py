import importlib
from importlib.machinery import SourceFileLoader


def load_module(module_path):
    module = importlib.import_module(module_path)
    return module


def load_module_from_file(module_name, module_path):
    module_spec = importlib.util.spec_from_file_location(module_name, module_path)
    loaded_module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(loaded_module)
    return loaded_module


def load_module_from_source(module_name: str, module_file_path: str):
    m = SourceFileLoader(module_name, module_file_path).load_module()
    return m
