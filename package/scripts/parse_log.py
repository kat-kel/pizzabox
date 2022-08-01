import re
import os

from .analyse_log import LogLine

def parse_log(log_path, github_directory, OutputDataFormat):
    
    # Empty lists to stock input data.
    zones_needing_verification = []
    lines_needing_verification = []
    zones_needing_analysis = []
    lines_needing_analysis = []

    # Open the log file given as an argument in the command line.
    with open(log_path.name, "r", encoding='utf-8') as f:
        log = f.readlines()

        # Iterate over every line in the log.
        for i, log_line in enumerate(log):

            # Instantiate the class Line for this line of the log.
            parsed_line = LogLine(log, log_line, i)

            # Look for lines in the log that contain the phrase "empty zone(s)".
            if "empty zone(s)" in parsed_line.text:
                zones_needing_verification = parsed_line.analyse_empty(zones_needing_verification, 1)

            # Compile a regular expression that checks what integer comes before the phrase "empty line".
            number_before_empty_line = re.compile(r'[1-9](?=(?:\sempty\sline))|[0-9]0(?=(?:\sempty\sline))')
            # Look for lines in the log that contain the phrase "empty line(s)" and that count 1 or more empty lines.
            if "empty line(s)" in log_line and number_before_empty_line.search(parsed_line.text):
                lines_needing_verification = parsed_line.analyse_empty(lines_needing_verification, 2)

            # Look for lines in the log that forbid zones with empty tags.
            if "*Empty* tag for zones" in parsed_line.text:
                zones_needing_analysis = parsed_line.analyse_empty(zones_needing_analysis, 1)

            # Look for lines in the log that forbid lines with empty tags.
            if "*Empty* tag for lines" in parsed_line.text:
                lines_needing_analysis = parsed_line.analyse_empty(lines_needing_analysis, 1)
    
    # Format the parsed data for the output log.
    problematic_empty_lines = format_output_data(lines_needing_verification, github_directory, OutputDataFormat, "Line should have text.")
    zones_missing_tags = format_output_data(zones_needing_analysis, github_directory, OutputDataFormat, "Zone missing a tag.")
    lines_missing_tags = format_output_data(lines_needing_analysis, github_directory, OutputDataFormat, "Line missing a tag.")
    
    # Return the lists of named tuples for empty zones and problematic lines.
    return zones_needing_verification, problematic_empty_lines, zones_missing_tags, lines_missing_tags


def format_output_data(list, github_directory, OutputDataFormat, issue):
    for EmptyElementsInDocument in list:
        formatted_output_data = [
            OutputDataFormat(issue, "NA", element, os.path.join(github_directory, EmptyElementsInDocument.file[2:]))
            for element in EmptyElementsInDocument.elements
        ]
    return formatted_output_data