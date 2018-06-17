"""Allow tests to discover the modules."""

import sys
from pathlib import Path


_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent.joinpath("src", "pyhtml")))
