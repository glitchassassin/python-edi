""" Parsing test cases for PythonEDI """

import unittest
import pprint
import pythonedi

class TestParse810(unittest.TestCase):
    """ Tests the Parser module """
    def setUp(self):
        self.parser = pythonedi.EDIParser(edi_format="810") #, segment_delimiter="~")

    def test_parse(self):
        with open("test/test_edi.txt", "r") as test_edi_file:
            test_edi = test_edi_file.read()
            found_segments, edi_data = self.parser.parse(test_edi)
            print("\n\n{}".format(found_segments))
            print("\n\n")
            pprint.pprint(edi_data)
