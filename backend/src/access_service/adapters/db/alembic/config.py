from collections.abc import Iterator
from importlib.resources import as_file, files
from pathlib import Path

import backend.src.adapters.db.alembic


def get_alembic_config_path() -> Iterator[Path]:
    source = files(backend.src.adapters.db.alembic).joinpath("alembic.ini")
    with as_file(source) as path:
        yield path
