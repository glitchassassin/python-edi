"""
Test cases for pythonedi module
"""

import string
import random
import unittest
from datetime import datetime

import pythonedi

class TestGenerate810(unittest.TestCase):

    def setUp(self):
        self.g = pythonedi.EDIGenerator()

    def test_generate(self):
        invoice_number = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(22))
        po_number = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(22))
        #pythonedi.explain("810", "ITD")
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
                datetime(2006, 6, 24, 10, 00), # Interchange Date
                datetime(2006, 6, 24, 10, 00), # Interchange Time
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
                datetime(2006, 6, 24, 10, 00), # Date
                datetime(2006, 6, 24, 10, 00), # Time
                "1164", # Group Control Number
                "X", # Responsible Agency Code
                "004010", # Version/Release/Industry Identifier Code
            ],
            "ST": [
                "810", # Transaction Set Identifier Code: Invoice
                "11640002" # Transaction Set Control Number
            ],
            "BIG": [
                datetime(2006, 6, 24), # Invoice date
                "INV-00777", # Invoice number
                datetime(2006, 6, 22), # Purchase order date
                "PO-001063", # PO Number
                None,
                None,
                "DR"
            ],
            "L_N1": [
                {
                    "N1": [
                        "ST", # Entity Identifier Code: Ship To
                        "SANGA GENERAL HOSPITAL", # Name
                        "91", # ID Code Qualifier: Assigned by seller
                        "6877755" # ID number
                    ],
                    "N3": [
                        "1765 HOSPITAL STREET" # Additional address information
                    ],
                    "N4": [ # Geographic location
                        "WESTWOOD", # City Name
                        "ON", # State or Province Code
                        "M8Y 6H8" # Postal Code
                    ]
                },
                {
                    "N1": [
                        "BT", # Entity Identifier Code: Bill To
                        "SANGA GENERAL HOSPITAL", # Name
                        "91", # ID Code Qualifier: Assigned by seller
                        "6877700" # ID number
                    ],
                },
                {
                    "N1": [
                        "VN", # Entity Identifier Code: Vendor
                        "ALLSUPPLIES INC.", # Name
                        "91", # ID Code Qualifier: Assigned by seller
                        "306000000" # ID number
                    ],
                }
            ],
            "ITD": [
                "05", # Terms Type Code
                "3", # Terms Basis Date Code: Invoice Date
                None, # Terms Discount %
                None, # Terms Discount Due Date
                None, # Terms Discount Days Due
                datetime(2006, 6, 24), # Terms Net Due Date
                "30" # Terms Net Days
            ],
            "DTM": [
                "011", # Date/Time Qualifier: Shipped
                datetime(2006, 6, 20) # Date
            ],
            "L_IT1": [
                {
                    "IT1": [ # Baseline Item Data
                        "1", # Assigned Identification
                        1 # Quantity Invoiced
                    ]
                }
            ]
        }

        message = self.g.build(edi_data)
        print("\n\n" + message)

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
        old_level = pythonedi.Debug.level
        pythonedi.Debug.level = 0 # Turn off explaining for intentional exceptions

        with self.assertRaises(ValueError):
            message = self.g.build(edi_data)

        pythonedi.Debug.level = old_level
