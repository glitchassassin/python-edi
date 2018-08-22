"""
PythonEDI

Generates EDI messages from Python data objects (dicts/lists/etc).
Validates against a provided EDI standard definition (in JSON format).
Provides hints if the validation fails.
"""

import os

from .EDIGenerator import EDIGenerator, Debug, supported_formats
from .EDIParser import EDIParser

def explain(edi_format, section_id=""):
    """ Explains the referenced section of the referenced EDI format.

    Try `pythonedi.explain("810", "ITD")`
    """
    if edi_format not in supported_formats:
        raise ValueError("'{}' is not a supported EDI format. Valid formats include: ({})".format(edi_format, ", ".join(supported_formats.keys())))
    section_id = section_id.upper()
    if section_id == "":
        Debug.explain(supported_formats[edi_format])
        return
    for section in supported_formats[edi_format]:
        if section["id"] == section_id:
            Debug.explain(section)
            return
        elif section["type"] == "loop":
            for segment in section["segments"]:
                if segment["id"] == section_id:
                    Debug.explain(section)
                    return

    print("Section '{}' was not found for EDI format '{}'.".format(section_id, edi_format))
        