from dataclasses import dataclass, field
import sys
from types import ModuleType

def create_patched_module():
    # Create a new module to avoid import issues
    mod = ModuleType('mitmproxy.contentviews.grpc')
    sys.modules['mitmproxy.contentviews.grpc'] = mod

    # Create the patched classes
    @dataclass
    class ParserOptions:
        def __init__(self):
            pass

    class ProtoParser:
        ParserOptions = ParserOptions

    # Add classes to module
    mod.ProtoParser = ProtoParser
    return mod

def apply_patch():
    try:
        # Create and inject the patched module before any mitmproxy imports
        patched_module = create_patched_module()
        sys.modules['mitmproxy.contentviews.grpc'] = patched_module
        
        # Force reload of dependent modules
        modules_to_reload = [
            'mitmproxy.contentviews',
            'mitmproxy.tools.web.app',
            'mitmproxy.tools.web.master'
        ]
        
        for module_name in modules_to_reload:
            if module_name in sys.modules:
                del sys.modules[module_name]
                
    except Exception as e:
        print(f"Failed to apply mitmproxy patch: {e}") 