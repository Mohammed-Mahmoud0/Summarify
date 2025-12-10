import PyPDF2


def extract_text_from_pdf(file_obj):
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    cleaned_text = clean_text(text)
    return cleaned_text


def clean_text(text):
    cleaned = " ".join(text.split())
    return cleaned


# test code for extracting and summarizing text from a PDF
# with open(
#     "D:\\Programming\\Projects\\Work\\Summarify\\Backend\\summarizer\\utils\\Idioms+Set+2+Definitions.pdf",
#     "rb",
# ) as f:
#     ex_text = extract_text_from_pdf(f)
#     text = summarize_text(ex_text)
#     print("**********************************************")
#     print(text)
#     print("**********************************************")
