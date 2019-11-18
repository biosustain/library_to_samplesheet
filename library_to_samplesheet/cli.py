# -*- coding: utf-8 -*-

"""Console script for library_to_samplesheet."""
import os
import sys

import click

from library_to_samplesheet.library_to_samplesheet \
    import parse_run_parameters, parse_library_sheet, write_sample_sheet


@click.command()
@click.option('--run_parameters', '-r',
              help='Path to "RunParamters.xml" file.')
@click.option('--library_sheet', '-l',
              help='Path to library sheet file.')
@click.option('--output', '-o',
              help='Path for sample sheet output.')
def main(run_parameters, library_sheet, output):
    """Console script for library_to_samplesheet."""
    # Check given paths
    if not os.path.exists(run_parameters):
        click.echo("Given RunParamters path doesn't exist:\n"
                   f"\"{run_parameters}\"")
        sys.exit(-1)
    run_parameters = os.path.abspath(run_parameters)

    if not os.path.exists(library_sheet):
        click.echo("Given library sheet path doesn't exist:\n"
                   f"\"{library_sheet}\"")
        sys.exit(-1)
    library_sheet = os.path.abspath(library_sheet)

    # Do not overwrite existing files.
    if os.path.exists(output):
        click.echo("Given sample sheet path already exist:\n"
                   f"\"{output}\"")
        sys.exit(-1)

    # Parse run parameters
    run_parameters = parse_run_parameters(run_parameters)

    # Parse library sheet
    library = parse_library_sheet(library_sheet)

    # Write sample sheet
    write_sample_sheet(output, run_parameters, library)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
