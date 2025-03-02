import PyPDF2

from .base_loader import BaseDocumentLoader


class PdfDocumentLoader(BaseDocumentLoader):
    def load(self, file_path: str) -> dict:
        """
        Load a PDF document from a given file path and return a dictionary with keys
        like 'title', 'text_content', and any additional metadata.

        :param file_path: The file path of the PDF document to load.
        :return: A dictionary with the following keys:

            - title: The title of the PDF document, which is the file path here.
            - text_content: The main text content of the PDF document.
            - metadata: A dictionary containing the following keys:

                - file_type: The type of the document, always "pdf".
        """
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        return {
            "title": file_path,
            "text_content": text,
            "metadata": {"file_type": "pdf"},
        }
