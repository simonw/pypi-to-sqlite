from click.testing import CliRunner
import json
import pathlib
from pypi_to_sqlite.cli import cli
import pytest
import sqlite_utils

fixture = json.loads(
    (pathlib.Path(__file__).parent / "datasette-block.json").read_text()
)


@pytest.mark.parametrize("use_file", (True, False))
def test_import_package(httpx_mock, use_file):
    args = []
    runner = CliRunner()
    with runner.isolated_filesystem():
        if use_file:
            open("package.json", "w").write(json.dumps(fixture))
            args = ["-f", "package.json"]
        else:
            args = ["datasette-block"]
            httpx_mock.add_response(json=fixture)
        result = runner.invoke(cli, ["pypi.db"] + args, catch_exceptions=False)
        assert result.exit_code == 0
        db = sqlite_utils.Database("pypi.db")
        schema = db.schema
    assert schema == (
        "CREATE TABLE [packages] (\n"
        "   [name] TEXT PRIMARY KEY,\n"
        "   [summary] TEXT,\n"
        "   [classifiers] TEXT,\n"
        "   [description] TEXT,\n"
        "   [author] TEXT,\n"
        "   [author_email] TEXT,\n"
        "   [description_content_type] TEXT,\n"
        "   [home_page] TEXT,\n"
        "   [keywords] TEXT,\n"
        "   [license] TEXT,\n"
        "   [maintainer] TEXT,\n"
        "   [maintainer_email] TEXT,\n"
        "   [package_url] TEXT,\n"
        "   [platform] TEXT,\n"
        "   [project_url] TEXT,\n"
        "   [project_urls] TEXT,\n"
        "   [release_url] TEXT,\n"
        "   [requires_dist] TEXT,\n"
        "   [requires_python] TEXT,\n"
        "   [version] TEXT,\n"
        "   [yanked] INTEGER,\n"
        "   [yanked_reason] TEXT\n"
        ");\n"
        "CREATE TABLE [releases] (\n"
        "   [package] TEXT REFERENCES [packages]([name]),\n"
        "   [version] TEXT,\n"
        "   [packagetype] TEXT,\n"
        "   [filename] TEXT,\n"
        "   [comment_text] TEXT,\n"
        "   [digests] TEXT,\n"
        "   [downloads] INTEGER,\n"
        "   [has_sig] INTEGER,\n"
        "   [md5_digest] TEXT PRIMARY KEY,\n"
        "   [python_version] TEXT,\n"
        "   [requires_python] TEXT,\n"
        "   [size] INTEGER,\n"
        "   [upload_time] TEXT,\n"
        "   [upload_time_iso_8601] TEXT,\n"
        "   [url] TEXT,\n"
        "   [yanked] INTEGER,\n"
        "   [yanked_reason] TEXT\n"
        ");"
    )
