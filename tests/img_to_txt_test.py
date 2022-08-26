import unittest
from src.img_to_txt import ImgToStrings

class ImgToTxtTest(unittest.TestCase):
    def setUp(self):
        self.img_to_strings = ImgToStrings()

    def test_img_to_str_invalid_img_path(self):
        with self.assertRaises(self.img_to_strings.InvalidImgPath):
            self.img_to_strings.img_to_str("tests/test_files/any_jpg.jpg", "eng")

    def test_img_to_str_invalid_lang(self):
        with self.assertRaises(self.img_to_strings.InvalidFilename):
            self.img_to_strings.img_to_str("tests/test_files/any_file.pdf", "en")

    def test_img_to_str(self):
        text = self.img_to_strings.img_to_str("tests/test_files/sample_jpg.jpg", "eng")
        self.assertEqual(text, "This is a sample document and this is the first sentence\n\nThis is line two and this is the second sentence\n\x0c")