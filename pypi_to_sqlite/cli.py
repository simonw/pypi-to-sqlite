import click
import httpx
import json
import sqlite_utils
import time


@click.command()
@click.version_option()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("package", nargs=-1)
@click.option(
    "-f",
    "--file",
    multiple=True,
    type=click.File("rb"),
    help="Import JSON from this file",
)
@click.option(
    "-d",
    "--delay",
    type=float,
    help="Wait this many seconds between requests",
    default=1.0,
)
def cli(db_path, package, file, delay):
    """
    Load data about Python packages from PyPI into SQLite

    Usage example:

        pypi-to-sqlite pypy.db datasette sqlite-utils

    Use -f to load data from a JSON file instead:

        pypi-to-sqlite pypy.db -f datasette.json
    """
    db = sqlite_utils.Database(db_path)
    with click.progressbar(package) as bar:
        for name in bar:
            save_to_db(db, fetch_package(name))
            time.sleep(delay)
    for file_obj in file:
        save_to_db(db, json.load(file_obj))


def fetch_package(name):
    url = "https://pypi.org/pypi/{}/json".format(name)
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()


def save_to_db(db, data):
    info = data["info"]
    for key in ("bugtrack_url", "docs_url", "download_url", "downloads"):
        # Obsolete PyPI fields
        info.pop(key)
    releases = data["releases"]
    db["packages"].insert(
        info, pk="name", column_order=("name", "summary", "classifiers", "description")
    )
    # Releases are: {"version_number": [list-of-downloads]}
    for version_number, downloads in releases.items():
        version_id = "{}:{}".format(info["name"], version_number)
        db["versions"].insert(
            {
                "id": version_id,
                "package": info["name"],
                "name": version_number,
            },
            pk="id",
            foreign_keys=("package",),
            replace=True,
        )
        for download in downloads:
            download.pop("downloads")
            db["releases"].insert(
                dict(download, version=version_id, package=info["name"]),
                column_order=("package", "version", "packagetype", "filename"),
                foreign_keys=("package", "version"),
                pk="md5_digest",
            )
