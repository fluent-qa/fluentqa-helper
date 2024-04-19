import inspect
import sys

from toolkits.capture.module_loader import load_module_from_file


def test_module_loader():
    print("this is test")
    sys.path.append("../plugins/mitmutils")
    m = load_module_from_file("plugins", "../plugins/mitm/mitm-replace.py")
    print(inspect.ismodule(m))
    print(dir(m))