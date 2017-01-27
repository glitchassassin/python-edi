"""
PythonEDI

Generates EDI messages from Python data objects (dicts/lists/etc).
Validates against a provided EDI standard definition (in JSON format).
Provides hints if the validation fails.
"""

from .EDIGenerator import EDIGenerator
