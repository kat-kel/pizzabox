import re
from collections import namedtuple

# Remove any ANSI code from a line of text.
ansi_escape_regex = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')

class LogLine():
    def __init__(self, log, line, count):
        self.log = log
        self.text = ansi_escape_regex.sub('', line)
        self.i = count

    def analyse_empty(self, elements_needing_verification, levels_up):
        """
        param:
            elements_needing_verification (list): 
            levels_up (int): the number of lines above the current one to search 
                            for relevant ALTO XML document's path; the number will be
                            1 line up for zones, and 2 lines up for a text line.
        """

        # Set up named tuple for empty zone data, containing the ALTO XML document's path and the zone's ID.
        EmptyElementsInDocument = namedtuple("EmptyElementsInDocument", ["file", "elements"])

        # Extract a list of zones named in the cleaned log line.
        empty_elements = [z[1:] for z in re.split(r"[,\s+]", self.text) if z!='' and z[0]=="#"]

        # Get the relative path of the ALTO XML document cited in the log.
        # If analysing a log line for an *Empty* tag, look one line farther up the log for the document name. 
        # But if the phrase "Segmonto test" is not found on that line, look two lines farther up.
        if "*Empty* tag" in self.text and "Segmonto test" not in self.log[self.i-levels_up]:
            doc_path_in_log = [d for d in re.split(r"\s|\:", self.log[self.i-2]) if d!='' and d[:7]=="./data/"][0]
        # Look the given number of lines higher up on the log to find the document name; 
        # either 1 line above a log line talking about empty zones, 
        # or 2 lines above when the log line talks about empty lines.
        else:
            doc_path_in_log = [d for d in re.split(r"\s|\:", self.log[self.i-levels_up]) if d!='' and d[:7]=="./data/"][0]

        # Add the empty zones and the ALTO XML document's relative path to the list of empty zones.
        elements_needing_verification.append(EmptyElementsInDocument(doc_path_in_log, empty_elements))
        return elements_needing_verification