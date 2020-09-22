from typing import Optional

import click

from bear_exporter.bear import Bear

BEAR = Bear()


@click.group()
def main() -> None:
    pass


@main.command()
@click.option(
    "--notes", "-n", "what", flag_value="notes", help="List notes", default=True
)
@click.option("--files", "-f", "what", flag_value="files", help="List files")
@click.option("--tags", "-t", "what", flag_value="tags", help="List tags")
@click.option("--filter", help="filter output")
def list(what: str, filter: Optional[str] = None) -> None:
    """
    List Bear items
    """
    click.secho("{}:".format(what.capitalize()), fg="green", bold=True)

    # TODO: Actually parse list output
    if what == "notes":
        for note in BEAR.notes():
            click.echo("{:4d} {:.100}".format(note.key, note.title))
    elif what == "tags":
        for tag in BEAR.tags():
            click.echo(tag)
