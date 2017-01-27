"""
Parses a provided dictionary set and tries to build an EDI message from the data.
Provides hints if data is missing, incomplete, or incorrect.
"""

import os
import json
from .hint import explain

class EDIGenerator(object):
    def __init__(self):
        # Map format definitions
        self.supported_formats = {}
        self.formats_path = os.path.join(os.path.dirname(__file__), "formats")
        for filename in os.listdir(self.formats_path):
            if filename.endswith(".json"):
                format_name = filename[:-5]
                with open(os.path.join(self.formats_path, filename)) as format_file:
                    format_def = json.load(format_file)
                if type(format_def) is not list:
                    raise TypeError("Imported definition {} is not a list of segments".format(format_name))
                self.supported_formats[format_name] = format_def

    def build(self, data):
        """
        Compiles a transaction set (as a dict) into an EDI message
        """
        # Check for transaction set ID in data

        if "ST" not in data:
            explain(self.supported_formats["ST"])
            raise ValueError("No transaction set header found in data.")
        ts_id = data["ST"][0]
        if ts_id not in self.supported_formats:
            raise ValueError("Transaction set type '{}' is not supported. Valid types include: {}".format(
                ts_id,
                "".join(["\n - " + f for f in self.supported_formats])
            ))
        edi_format = self.supported_formats[ts_id]

        # Walk through the format definition to compile the output message
        for segment in edi_format:
            if segment["id"] not in data:
                if segment["req"] == "O":
                    # Optional segment is missing - that's fine, keep going
                    continue
                elif segment["req"] == "M":
                    # Mandatory segment is missing - explain it and then fail
                    explain(segment)
                    raise ValueError("EDI data is missing mandatory segment '{}'.".format(segment["id"]))
                else:

            
            # Segment exists, so let's process it.


        return None