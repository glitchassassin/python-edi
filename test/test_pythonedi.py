"""
Test cases for pythonedi module
"""

import string
import random
import unittest
import pythonedi
from datetime import datetime

class TestGenerate810(unittest.TestCase):

    def setUp(self):
        self.g = pythonedi.EDIGenerator()

    def test_generate(self):
        invoice_number = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(22))
        po_number = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(22))

        edi_data = {
            "ISA": [
                "00", # Authorization Information Qualifier
                "", # Authorization Information
                "00", # Security Information Qualifier
                "", # Security Information
                "ZZ", # Interchange Sender ID Qualifier
                "306000000", # Interchange Sender ID
                "ZZ", # Interchange Receiver ID Qualifier
                "306009503", # Interchange Receiver ID
                datetime.now(), # Interchange Date
                datetime.now(), # Interchange Time
                "U", # Interchange Control Standards Identifier
                "00401", # Interchange Control Version Number
                "000010770", # Interchange Control Number
                "0", # Acknowledgment Requested
                "P", # Usage Indicator
                "/" # Component Element Separator
            ],
            "GS": [
                "IN", # Functional Identifier Code
                "306000000", # Application Sender's Code
                "306009503", # Application Receiver's Code
                datetime.now(), # Date
                datetime.now(), # Time
                "1164", # Group Control Number
                "X", # Responsible Agency Code
                "004010", # Version/Release/Industry Identifier Code
            ],
            "ST": [
                "810",
                "123456"
            ],
            "BIG": [
                datetime.now(), # Invoice date
                invoice_number, # Invoice number
                datetime.now(), # Purchase order date
                po_number,
                None,
                None,
                "CN"
            ],
            "REF": [
                "SA",
                "Joe Schmoe"
            ]
        }

        message = self.g.build(edi_data)
        print(message)

    def test_error_handling(self):
        invoice_number = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(22))
        po_number = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(22))

        edi_data = {
            "ISA": [
                "00", # Authorization Information Qualifier
                "", # Authorization Information
                "00", # Security Information Qualifier
                "", # Security Information
                "ZZ", # Interchange Sender ID Qualifier
                "306000000", # Interchange Sender ID
                "ZZ", # Interchange Receiver ID Qualifier
                "306009503", # Interchange Receiver ID
                datetime.now(), # Interchange Date
                datetime.now(), # Interchange Time
                "U", # Interchange Control Standards Identifier
                "00401", # Interchange Control Version Number
                "000010770", # Interchange Control Number
                "0", # Acknowledgment Requested
                "P", # Usage Indicator
                "/" # Component Element Separator
            ],
            "ST": [
                "810",
                "123456"
            ],
            "BIG": [
                datetime.now(), # Invoice date
                invoice_number, # Invoice number
                datetime.now(), # Purchase order date
                po_number,
                None,
                None,
                "CN"
            ],
            "REF": [
                "AP"
            ]
        }

        with self.assertRaises(ValueError):
            self.g.debug_level = 0 # Turn off explaining for intentional exceptions
            message = self.g.build(edi_data)
