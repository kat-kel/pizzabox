import click
from collections import namedtuple

from .scripts.parse_log import parse_log
from .scripts.parse_xml import search_zones
from .scripts.output import write_output_log

@click.command()
@click.argument('log_path', type=click.File())
@click.argument('github_directory', type=click.Path())
def main(log_path, github_directory):

    OutputDataFormat = namedtuple("OutputDataFormat", ["issue", "tag", "element", "file"])

    # Parse the HTRVX log to find problematic emtpy zones and problematic lines.
    zones_needing_verification, problematic_empty_lines, zones_missing_tags, lines_missing_tags = parse_log(log_path, github_directory, OutputDataFormat)

    # Update the output log with formatted data about the problematic empty zones.
    problematic_empty_zones = search_zones(zones_needing_verification, github_directory, OutputDataFormat)

    # Update the output log with formatted data about the problematic lines.
    #output_log = fix_lines(lines_needing_verification)

    output = zones_missing_tags + lines_missing_tags + problematic_empty_lines + problematic_empty_zones

    # Write the output to a CSV file.
    write_output_log(output, log_path)

if __name__ == '__main__':
    main()