"""General-purpose helpers for the data-toolkit project."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Iterable, Iterator, Mapping, Sequence
from itertools import islice
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")
_MISSING = object()


def load_json(path: str | os.PathLike[str], *, encoding: str = "utf-8") -> Any:
    """Load and decode JSON data from a file.

    Args:
        path: Path to the JSON file.
        encoding: Text encoding used to read the file.

    Returns:
        The decoded JSON value.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    with Path(path).open("r", encoding=encoding) as file:
        return json.load(file)


def save_json(
    data: Any,
    path: str | os.PathLike[str],
    *,
    encoding: str = "utf-8",
    indent: int | None = 2,
) -> None:
    """Serialize data to JSON and atomically replace the destination file.

    Parent directories are created automatically. If serialization or writing
    fails, the existing destination file remains unchanged.

    Args:
        data: JSON-serializable value to write.
        path: Destination file path.
        encoding: Text encoding used to write the file.
        indent: JSON indentation width, or ``None`` for compact output.

    Raises:
        TypeError: If data is not JSON serializable.
        OSError: If the destination cannot be written or replaced.
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding=encoding,
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temporary_path = Path(file.name)
            json.dump(data, file, ensure_ascii=False, indent=indent)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_path, destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield items in lists containing at most ``size`` elements.

    Args:
        items: Any finite or streaming iterable.
        size: Maximum number of elements in each chunk.

    Yields:
        Non-empty lists in the original iteration order.

    Raises:
        ValueError: If size is less than one.
    """
    if size < 1:
        raise ValueError("size must be greater than zero")

    iterator = iter(items)
    while chunk := list(islice(iterator, size)):
        yield chunk


def deep_get(
    data: Mapping[str, Any],
    path: str | Sequence[str],
    *,
    separator: str = ".",
    default: Any = _MISSING,
) -> Any:
    """Retrieve a value from nested mappings.

    Args:
        data: Root mapping to traverse.
        path: Key sequence or separator-delimited key string.
        separator: Delimiter used when path is a string.
        default: Value returned when a key is absent or traversal encounters
            a non-mapping value. If omitted, a ``KeyError`` is raised.

    Returns:
        The nested value, or ``default`` when supplied and traversal fails.

    Raises:
        KeyError: If traversal fails and no default was supplied.
        ValueError: If separator is empty for a string path.
    """
    if isinstance(path, str):
        if not separator:
            raise ValueError("separator must not be empty")
        keys = path.split(separator) if path else []
    else:
        keys = list(path)

    current: Any = data
    for key in keys:
        if not isinstance(current, Mapping) or key not in current:
            if default is _MISSING:
                raise KeyError(key)
            return default
        current = current[key]

    return current