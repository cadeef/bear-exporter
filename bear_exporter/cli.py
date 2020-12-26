from pathlib import Path
from typing import Any, Optional, Sequence, Tuple

import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup
from tablib import Dataset

from bear_exporter.bear import Bear

# import tabulate


BEAR = Bear()


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def main(verbose: bool = False) -> None:
    """
    Export Bear.app notes and files with ease.

    """
    # TODO: Pass ctx around for verbose
    pass


@main.command()
@click.option(
    "--list",
    "-l",
    "action",
    flag_value="list",
    help="List notes (default)",
    default=True,
)
@click.option("--export", "-e", "action", flag_value="export", help="Export notes")
@optgroup.group(
    "Filters",
    cls=MutuallyExclusiveOptionGroup,
    help="available for --list and --export",
)
@optgroup.option(
    "--tag", "-t", multiple=True, help="filter by tag, may be invoked multiple times"
)
@optgroup.option(
    "--id",
    "-i",
    "note_id",
    multiple=True,
    type=int,
    help="filter by ID, may be invoked multiple times",
)
@optgroup.option("--title", "-T", help="filter by title")
# @optgroup.group('Export')
# @optgroup.option("--slugify/--no-slugify", default=True, help="slugify note title for file name")
def notes(
    action: str,
    tag: Optional[Tuple[str]] = None,
    note_id: Optional[Tuple[int]] = None,
    title: Optional[str] = None,
):
    """
    Notes interface
    """
    # TODO: Add help for notes
    display_title("Notes:")
    if action == "list":
        notes = BEAR.notes(tag=tag, note_id=note_id, title=title)
        display_table(notes, ["ID", "Title"], ["id", "title"])
    elif action == "export":
        pass


@main.command()
def tags():
    """ """
    # TODO: Add help for tags
    display_title("Tags:")
    display_table(BEAR.tags(), ["ID", "Tag"], ["id", "title"])


@main.command()
@click.option(
    "--list",
    "-l",
    "action",
    flag_value="list",
    help="List files (default)",
    default=True,
)
@click.option("--export", "-e", "action", flag_value="export", help="Export files")
@optgroup.group("Filters", cls=MutuallyExclusiveOptionGroup)
@optgroup.option(
    "--id",
    "-i",
    "file_id",
    multiple=True,
    type=int,
    help="filter by ID, may be invoked multiple times",
)
@optgroup.option("--title", "-T", help="filter by title")
@optgroup.option(
    "--extension",
    "-e",
    "extension",
    type=str,
    help="filter by extension",
)
@optgroup.group("Output")
@optgroup.option(
    "--output-dir",
    "-o",
    "output_dir",
    type=click.Path(exists=True),
    default=Path.cwd(),
    help="output directory",
)
def files(
    action: str,
    file_id: Optional[Tuple[int]] = None,
    title: Optional[str] = None,
    extension: Optional[str] = None,
    output_dir: Path = Path.cwd(),
):
    """
    Files interface
    """
    files = BEAR.files(file_id=file_id, title=title, extension=extension)

    display_title("Files:")
    if action == "list":
        display_table(files, ["ID", "Name"], ["id", "name"])
    elif action == "export":
        for file in files:
            file.export(output_dir)


def display_table(
    records: Sequence[Any],
    headers: Sequence[str],
    attrs: Sequence[str],
    tablefmt: str = "fancy_grid",
) -> None:
    """

    Args:
      records: Sequence[Any]:
      headers: Sequence[str]:
      attrs: Sequence[str]:
      tablefmt: str:  (Default value = "fancy_grid")

    Returns:

    """
    if len(records) == 0:
        display_error("No results found")
    else:
        data = Dataset()
        data.headers = headers
        for record in records:
            data.append([getattr(record, a) for a in attrs])

        click.echo(data.export("cli", tablefmt=tablefmt))


def display_title(text: str) -> None:
    """

    Args:
      text: str:

    Returns:

    """
    click.secho(text, fg="green", bold=True)


def display_error(message: str) -> None:
    """

    Args:
      message: str:

    Returns:

    """
    click.secho("ERROR: {}".format(message), fg="red")
