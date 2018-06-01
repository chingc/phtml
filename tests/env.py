"""The annoying part of Python."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent.joinpath("src")))
