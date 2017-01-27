"""
PythonEDI

Generates EDI messages from Python data objects (dicts/lists/etc).
Validates against a provided EDI standard definition (in JSON format).
Provides hints if the validation fails.
"""

import os

from .EDIGenerator import EDIGenerator, Debug, supported_formats
from .hint import explain
