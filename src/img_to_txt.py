import pytesseract
import os
import sys
from PIL import Image
from unicodedata import category

class ImgToStrings():
    """
    Converts .docx file text and table to strings without symbols/punctuations. 
    """
    def __init__(self) -> None:
        self.lang = ["eng", "por", "fra", "deu_frak"]
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    def img_to_str(self, img_path: str, lang: str, crop_img_box=None):
        """
        """
        self.__check_file_path(img_path)
        self.__check_lang(lang)

        image = Image.open(img_path)

        if crop_img_box is not None:
            image = image.crop(crop_img_box)
        
        str = pytesseract.image_to_string(image, lang=lang)
        str_wo_symbols = self.__remove_symbols(str)

        return str_wo_symbols
    
    def __remove_symbols(self, text: str):
        """
        Removes symbols in text.

        Args:
            text (str): text from pdf file
        """
        str_only_list = []
        symbol_chars =  [chr(i) for i in range(sys.maxunicode) if category(chr(i)).startswith("P")]

        for char in text:
            if char not in symbol_chars:
                str_only_list.append(char)

        str_only_str = "".join(str_only_list)
        return str_only_str


    def __check_file_path(self, img_path):
        """
        """
        img_path_len = len(img_path) 

        if img_path_len < 4 or img_path[(img_path_len - 4): img_path_len] != ".pdf":
            raise self.InvalidFilename()

        valid_img_path = os.path.exists(img_path)

        if not valid_img_path:
            raise self.InvalidImgPath(img_path)

    
    def __check_lang(self, lang):
        """
        """
        if lang not in self.lang:
            raise self.InvalidLang(lang)

    
    class InvalidLang(Exception):
        def __init__(self, lang) -> None:
            super().__init__(f"Invalid lang: The lang \"{lang}\" does not exist")


    class InvalidImgPath(Exception):
        def __init__(self, img_path) -> None:
            super().__init__(f"Invalid image file path: The image {img_path} path does not exist")


    class InvalidFilename(Exception):
        def __init__(self) -> None:
            super().__init__(f"Invalid image file format: the filename must end with \".jpg\" or \".png\"")

