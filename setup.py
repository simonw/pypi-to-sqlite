from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="pypi-to-sqlite",
    description="Load data about Python packages from PyPI into SQLite",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/pypi-to-sqlite",
    project_urls={
        "Issues": "https://github.com/simonw/pypi-to-sqlite/issues",
        "CI": "https://github.com/simonw/pypi-to-sqlite/actions",
        "Changelog": "https://github.com/simonw/pypi-to-sqlite/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["pypi_to_sqlite"],
    entry_points="""
        [console_scripts]
        pypi-to-sqlite=pypi_to_sqlite.cli:cli
    """,
    install_requires=["click", "sqlite-utils", "httpx"],
    extras_require={"test": ["pytest", "pytest-httpx", "cogapp"]},
    python_requires=">=3.7",
)
