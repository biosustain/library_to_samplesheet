# -*- coding: utf-8 -*-

"""Console script for library_to_samplesheet."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for library_to_samplesheet."""
    click.echo("Replace this message by putting your code into "
               "library_to_samplesheet.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
