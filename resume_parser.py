import pdfplumber
import re
# import spacy

# nlp = spacy.load("en_core_web_sm")

def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    return text

def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):

    pattern = r"\b\d{10}\b"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"

def extract_name(text):

    doc = nlp(text)

    unwanted_words = [
        "mobile",
        "email",
        "phone",
        "contact"
    ]

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            name = ent.text.strip()

            for word in unwanted_words:
                name = name.replace(word.title(), "")
                name = name.replace(word.capitalize(), "")
                name = name.replace(word, "")

            return name.strip()

    return "Not Found"