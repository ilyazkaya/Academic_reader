import re
from PyPDF2 import PdfReader
import string
import os


# Open the PDF file
pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC\Kim and Kerchensteiner 2017 W3 OMS.pdf'

# Function to extract text from PDF and search for figure descriptions
def extract_figure_descriptions(pdf_path):
    pdf = PdfReader(open(pdf_path, 'rb'))
    descriptions = []

    # Regular expression to match figure descriptions (e.g., Figure 1, Figure 2, etc.)
    # figure_regex = re.compile(r'\n\n(?:Figure|Fig\.|FIG\.|Fig|FIG)\s*\d+[\s\W_](?=[A-Z])')
    pattern = r'^(?:Figure|Fig)\.?\s\d+\.\s'
    figure_regex = re.compile(pattern, re.MULTILINE)
    # figure_regex = re.compile(rf'\n\n(?:Figure|Fig|FIG)[{re.escape(punctuation)}]\s*\d+[\s\W_](?=[A-Z])')

    # Iterate through each page
    page_texts = []
    for page_num in range(len(pdf.pages)):
        # Extract text from page
        page_text = pdf.pages[page_num].extract_text()
        page_texts.append(page_text)
        if page_text:
            # Find all figure descriptions in the text
            for match in figure_regex.finditer(page_text):
                figure_title = match.group()
                # Extract the description following the figure title
                # Assuming description is in the next few lines
                start_idx = match.start()
                end_idx = start_idx + 500  # Arbitrary length for description
                figure_description = page_text[start_idx:end_idx]
                # Clean and cut the description at the next figure or end of paragraph
                figure_description = re.split(r'\n\n', figure_description)[0].strip()
                descriptions.append(figure_description)

    return descriptions, page_texts

# Extract figure descriptions
# Loop through each file in the directory
folder_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC'
papers = {}
for filename in os.listdir(folder_path):
    # Check if the file is a PDF
    if filename.endswith('.pdf'):
        # Full path to the file
        file_path = os.path.join(folder_path, filename)
        figure_descriptions, page_texts = extract_figure_descriptions(file_path)
        papers[filename] = figure_descriptions