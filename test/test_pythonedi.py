"""
Test cases for pythonedi module
"""

import string
import random
import unittest
import pythonedi
from datetime import date

class TestGenerate810(unittest.TestCase):

    def setUp(self):
        self.g = pythonedi.EDIGenerator()

    def test_generate(self):
        invoice_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(22))
        po_number = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(22))

        edi_data = {
            "ST": [
                "810",
                "123456"
            ],
            "BIG": [
                date.today(), # Invoice date
                invoice_number, # Invoice number
                date.today(), # Purchase order date
                po_number,
                "CN"
            ]
        }

        message = self.g.build(edi_data)
        print(message)