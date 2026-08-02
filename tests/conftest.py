"""Load unit-testable modules without importing Home Assistant."""

from pathlib import Path
import sys
from types import ModuleType


PACKAGE_PATH = Path(__file__).parents[1] / "custom_components" / "glance_clock"

custom_components = ModuleType("custom_components")
custom_components.__path__ = [str(PACKAGE_PATH.parent)]
sys.modules.setdefault("custom_components", custom_components)

glance_clock = ModuleType("custom_components.glance_clock")
glance_clock.__path__ = [str(PACKAGE_PATH)]
sys.modules.setdefault("custom_components.glance_clock", glance_clock)
