# pypi-to-sqlite

[![PyPI](https://img.shields.io/pypi/v/pypi-to-sqlite.svg)](https://pypi.org/project/pypi-to-sqlite/)
[![Changelog](https://img.shields.io/github/v/release/simonw/pypi-to-sqlite?include_prereleases&label=changelog)](https://github.com/simonw/pypi-to-sqlite/releases)
[![Tests](https://github.com/simonw/pypi-to-sqlite/workflows/Test/badge.svg)](https://github.com/simonw/pypi-to-sqlite/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/pypi-to-sqlite/blob/master/LICENSE)

Load data about Python packages from PyPI into SQLite

## Installation

Install this tool using `pip`:

    $ pip install pypi-to-sqlite

## Usage

To create a SQLite database with details of one or more packages, run:

    pypi-to-sqlite pypi.db datasette sqlite-utils

You can also process JSON that you have previously saved to disk like so:

    curl -o datasette.json https://pypi.org/pypi/datasette/json
    pypi-to-sqlite pypi.db -f datasette.json

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd pypi-to-sqlite
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
