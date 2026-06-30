import fitz
from pathlib import Path


def load_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


if __name__ == "__main__":

    pdf_folder = Path("data/raw")

    for pdf in pdf_folder.glob("*.pdf"):
        content = load_pdf(pdf)

        print(pdf.name)
        print(len(content))