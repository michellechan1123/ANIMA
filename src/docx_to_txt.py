import docx2pdf
from pdf_to_txt import PdfToStrings
import os

class DocxToStrings():
    """
    Converts .docx file text and table to strings without symbols/punctuations. 
    """
    def docx_to_str(self, file_path: str, file_page_line=None):
        """
        Converts text in .docx file into strings without symbols and punctuations.

        Args:
            file_path (str): pdf filepath in path/filename.pdf format
            file_page_line (dict["page": int, "lines": list[int]]): page and lines of the file
        """
        self.__check_file_path(file_path)

        pdf_file_path = self.__docx_to_pdf(file_path)

        pdf_to_str = PdfToStrings()
        text = pdf_to_str.txt_to_str(pdf_file_path, file_page_line)
        
        os.remove(pdf_file_path)

        return text
    
    
    def __docx_to_pdf(self, file_path :str):
        """
        Converts .docx file to a .pdf file. 

        Args:
            filename (str): filename in path/filename.docx format
        """
        docx2pdf.convert(file_path)
        pdf_file_path = file_path.replace(".docx", ".pdf")

        return pdf_file_path


    def __check_file_path(self, file_path):
        """
        Check if filename ends with .docx.

        Args: 
            file_path (str): docx filepath in path/filename.docx format
        """
        file_path_len = len(file_path) 

        if file_path_len < 5 or file_path[(file_path_len - 5): file_path_len] != ".docx":
            raise self.InvalidFilename()


    class InvalidFilename(Exception):
        def __init__(self) -> None:
            super().__init__(f"Invlid filename: the filename must end with \".docx\"")



  