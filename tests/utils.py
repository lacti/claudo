"""Test utilities for Claudo test suite."""
import importlib.util
from pathlib import Path


def import_hook(hook_path: Path):
    """Import a hook file as a module."""
    spec = importlib.util.spec_from_file_location(hook_path.stem, hook_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
