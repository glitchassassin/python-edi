"""
Imports and manages EDI format definitions
"""

import os
import json


def load_supported_formats(formats_path):
    supported_formats = {}
    for filename in os.listdir(formats_path):
        if filename.endswith(".json"):
            format_name = filename[:-5]
            with open(os.path.join(formats_path, filename)) as format_file:
                try:
                    format_def = json.load(format_file)
                except json.decoder.JSONDecodeError as e:
                    raise SyntaxError(
                        f"Failed to parse format: {format_name}\r\nError: {e}"
                    )
            if type(format_def) is not list:
                raise TypeError("Imported definition {} is not a list of segments".format(format_name))
            supported_formats[format_name] = format_def
    return supported_formats

supported_formats = load_supported_formats(os.path.join(os.path.dirname(__file__), "formats"))
