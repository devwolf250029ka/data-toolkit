# data-toolkit

A personal collection of practical utilities for cleaning, transforming, and inspecting everyday datasets.

## Features

- Clean and normalize CSV and JSON data
- Filter, sort, and reshape records
- Summarize columns and detect missing values
- Convert between supported data formats
- Simple command-line interface
- Lightweight and easy to extend

## Install

Clone the repository and install it locally:

    git clone https://github.com/your-username/data-toolkit.git
    cd data-toolkit
    pip install -e .

## Usage

Inspect a dataset:

    data-toolkit inspect data.csv

Clean a file and save the result:

    data-toolkit clean data.csv --output cleaned.csv

View all commands and options:

    data-toolkit --help