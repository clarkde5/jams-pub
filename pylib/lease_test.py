import unittest
import json
from lease import *

class TestLeaseFunctions(unittest.TestCase):

    def setUp(self):
        pages = json.loads('{"pages":[]}')
        page = json.loads('{"page_idx":0,"dimensions":[0,0],"orientation":{},"language":{},"blocks":[]}')
        block = json.loads('{"geometry":[[0,0],[0,0]],"artefacts":[],"lines":[]}')
        line = json.loads('{"geometry":[[0,0],[0,0]],"words":[]}')
        word = json.loads('{"geometry":[[0,0],[0,0]],"value":"","confidence":0}')

        pages["pages"].append(page)
        page["blocks"].append(block)
        block["lines"].append(line)
        line["words"].append(word)

        self.test_pages = pages
        self.test_page = page
        self.test_block = block
        self.test_line = line
        self.test_word = word
    
    def __getWord(self, value):
        return json.loads('{"geometry":[[0,0],[0,0]],"value":"'+value+'","confidence":0}')

    def test_GetInvoiceNumber_Invalid(self):
        self.assertEqual(getInvoiceNumber(0,self.test_pages["pages"][0]),"")

    def test_GetInvoiceNumber_Valid(self):
        self.test_line["words"].clear()
        self.test_line["words"].append(self.__getWord("INVOICE"))
        self.test_line["words"].append(self.__getWord("NUMBERI"))
        self.test_line["words"].append(self.__getWord("InvoiceNumber"))

        self.test_page["blocks"].append(self.test_block)
        self.test_block["lines"].append(self.test_line)

        self.assertEqual(getInvoiceNumber(0,self.test_pages["pages"][0]),"InvoiceNumber")
    
    def test_GetContractsForPage_Invalid(self):
        self.assertEqual(getContractsForPage(0,self.test_pages["pages"][0]),[])
        

if __name__ == '__main__':
    unittest.main()