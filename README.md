# data-toolkit

A personal collection of practical utilities for cleaning, transforming, and inspecting data.

## Features

- Read and write common tabular data formats
- Clean missing, duplicate, and inconsistent values
- Filter, sort, and transform datasets
- Generate quick dataset summaries
- Run repeatable operations from the command line

## Install

```bash
git clone https://github.com/<your-username>/data-toolkit.git
cd data-toolkit
python -m pip install -e .
```

## Usage

```bash
data-toolkit inspect data.csv
data-toolkit clean data.csv --output cleaned.csv
data-toolkit convert data.csv --output data.json
```

Run `data-toolkit --help` to see all commands and options.