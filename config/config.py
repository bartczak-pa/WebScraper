"""Module including configuration settings for the application."""

import os
from pathlib import Path

BASE_PATH = Path(os.environ.get("BASE_PATH", "/app")).resolve()
if not BASE_PATH.is_absolute():
    msg = "BASE_PATH must be an absolute path"
    raise ValueError(msg)
