from lxml import etree
import os
from collections import defaultdict

from ..config import names_of_unproblematic_emtpy_zones

NS = {'a':"http://www.loc.gov/standards/alto/ns-v4#"}  # namespace for the Alto xml

def search_zones(zones_needing_verification, directory, OutputDataFormat):
    problematic_empty_zones = []
    for document in zones_needing_verification:
        # Compose a path to the ALTO XML document using the directory given in the command line 
        # and the path to the document given in the log file. 
        # Because the latter relative path was composed from GitHub, it begins with 
        # "./", which must be removed before joining with the local directory path.
        doc_path = os.path.join(directory, document.file[2:])
        # Parse the ALTO XML document with lxml and get the root
        root = etree.parse(doc_path).getroot()

        # Decode all the @TAGREFS for this ALTO XML document.
        all_tag_elements = [t.attrib for t in root.findall('.//a:OtherTag', namespaces=NS)]
        collect = defaultdict(dict)
        for d in all_tag_elements:
            collect[d["ID"]] = d["LABEL"]
        all_tag_labels = dict(collect)

        # Check if the empty zone is unproblematic by verifying if the label of its @TAGREF 
        # is one of the zone types listed in the variable name_of_unproblematic_emtpy_zone[].
        for empty_zone_id in document.elements:
            zone_tagref = root.find(f'.//a:TextBlock[@ID="{empty_zone_id}"]', namespaces=NS).get("TAGREFS")
            if zone_tagref in all_tag_labels.keys() and all_tag_labels[zone_tagref] not in names_of_unproblematic_emtpy_zones:
                # Format this element's data for the output log, which is
                # namedtuple("OutputDataFormat", ["issue", "tag", "element", "file"])
                problematic_empty_zones.append(OutputDataFormat("Zone should not be empty.", all_tag_labels[zone_tagref], empty_zone_id, doc_path))
            elif zone_tagref not in all_tag_labels.keys():
                # Format this element's data for the output log, which is
                # namedtuple("OutputDataFormat", ["issue", "tag", "element", "file"])
                problematic_empty_zones.append(OutputDataFormat("Zone has invlaid TAGREF.", all_tag_labels[zone_tagref], empty_zone_id, doc_path))
    return problematic_empty_zones