"""General-purpose helpers for data loading, transformation, and validation."""

import csv
import json
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")


def read_json(path: str | Path, *, encoding: str = "utf-8") -> Any:
    """Read and deserialize a JSON file.

    Args:
        path: Path to the JSON file.
        encoding: Text encoding used to read the file.

    Returns:
        The deserialized JSON value.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    with Path(path).open("r", encoding=encoding) as file:
        return json.load(file)


def read_csv(
    path: str | Path,
    *,
    encoding: str = "utf-8-sig",
    delimiter: str = ",",
) -> list[dict[str, str]]:
    """Read a CSV file into a list of row dictionaries.

    Args:
        path: Path to the CSV file.
        encoding: Text encoding used to read the file.
        delimiter: Single-character field delimiter.

    Returns:
        Rows keyed by the CSV header fields.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file has no header row or the delimiter is invalid.
    """
    if len(delimiter) != 1:
        raise ValueError("delimiter must be exactly one character")

    with Path(path).open("r", encoding=encoding, newline="") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        if reader.fieldnames is None:
            raise ValueError("CSV file must contain a header row")
        return [dict(row) for row in reader]


def flatten_mapping(
    data: Mapping[str, Any],
    *,
    separator: str = ".",
    parent_key: str = "",
) -> dict[str, Any]:
    """Flatten nested mappings into keys joined by a separator.

    Args:
        data: Mapping to flatten.
        separator: String inserted between nested key components.
        parent_key: Optional prefix applied to every generated key.

    Returns:
        A new flat dictionary. Non-mapping values, including lists, are
        preserved unchanged.

    Raises:
        ValueError: If the separator is empty.
    """
    if not separator:
        raise ValueError("separator must not be empty")

    flattened: dict[str, Any] = {}
    for key, value in data.items():
        full_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, Mapping):
            flattened.update(
                flatten_mapping(
                    value,
                    separator=separator,
                    parent_key=full_key,
                )
            )
        else:
            flattened[full_key] = value
    return flattened


def batched(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield items in lists containing at most the requested number of values.

    Args:
        items: Any finite iterable of values.
        size: Maximum number of values in each batch.

    Yields:
        Non-empty lists in input order.

    Raises:
        ValueError: If size is less than one.
    """
    if size < 1:
        raise ValueError("size must be greater than zero")

    batch: list[T] = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []

    if batch:
        yield batch