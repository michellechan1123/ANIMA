import unittest
from src.pdf_to_txt import PdfToStrings

class PdfToTxtTest(unittest.TestCase):
    def setUp(self):
        self.pdf_to_strings = PdfToStrings()

    def test_pdf_to_str_invalid_file_type(self):
        with self.assertRaises(self.pdf_to_strings.InvalidFilename):
            self.pdf_to_strings.pdf_to_str("tests/test_files/sample.docx")

    def test_pdf_to_str_invalid_file_path(self):
        with self.assertRaises(Exception):
            self.pdf_to_strings.pdf_to_str("tests/test_files/any_pdf.pdf")
    
    def test_pdf_to_str_invalid_file_page_line_with_zero(self):
        with self.assertRaises(self.pdf_to_strings.InvalidPageLineNumber):
            self.pdf_to_strings.pdf_to_str("tests/test_files/sample_pdf.pdf", {"page": 0, "lines": [1, 2]})

    def test_pdf_to_str_invalid_file_page(self):
        with self.assertRaises(Exception):
            self.pdf_to_strings.pdf_to_str("tests/test_files/sample_pdf.pdf", {"page": 3, "lines": [20, 21]})

    def test_pdf_to_str_invalid_password(self):
        with self.assertRaises(Exception):
            self.pdf_to_strings.pdf_to_str("tests/test_files/sample_pdf_protected.pdf", {"page": 1, "lines": [1, 2]}, "password")
    
    def test_pdf_to_str(self):
        text = self.pdf_to_strings.pdf_to_str("tests/test_files/sample_pdf.pdf", {"page": 1, "lines": [1, 2]})
        self.assertEqual(text, " A Simple PDF File  This is a small demonstration .pdf file - ")

    def test_pdf_to_str_with_password(self):
        text = self.pdf_to_strings.pdf_to_str("tests/test_files/sample_pdf_protected.pdf", {"page": 1, "lines": [1, 2]}, "123456")
        self.assertEqual(text, " A Simple PDF File  This is a small demonstration .pdf file - ")
