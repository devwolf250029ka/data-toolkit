# data-toolkit

A small collection of practical utilities I use to inspect, clean, and convert everyday datasets.

## Features

- Read and write CSV, JSON, and JSON Lines
- Summarize columns, types, null values, and unique values
- Filter, rename, and select fields from the command line
- Convert between supported formats
- Stream large files without loading everything into memory

## Install

Requires Python 3.10 or newer.

```bash
git clone https://github.com/your-username/data-toolkit.git
cd data-toolkit
python -m pip install -e .
```

## Usage

Inspect a dataset:

```bash
data-toolkit inspect data/customers.csv
```

Convert CSV to JSON Lines:

```bash
data-toolkit convert data/customers.csv output/customers.jsonl
```

Use it from Python:

```python
from data_toolkit import Dataset

data = Dataset.read("data/customers.csv")
print(data.summary())
```