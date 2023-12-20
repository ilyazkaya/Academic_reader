import fitz  # PyMuPDF
from collections import defaultdict
import numpy as np

def analyze_pdf_fonts(file_path):
    # Open the PDF file
    doc = fitz.open(file_path)

    # Dictionary to hold text grouped by font characteristics
    font_data = defaultdict(str)

    # Total character count
    total_chars = 0

    # Function to round to the nearest half
    def round_half(n):
        return round(n * 2) / 2

    # Iterate through each page
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:  # iterate through the text blocks
            if "lines" in b:  # block contains text
                for line in b["lines"]:
                    for span in line["spans"]:  # iterate through text spans
                        if "size" in span and "font" in span:
                            # Font identifier includes font name, size (rounded to nearest half), and boldness
                            font_id = (span["font"], round_half(span["size"]), "bold" in span["font"].lower())
                            # Append text to the corresponding font category
                            font_data[font_id] += span["text"]
                            # Update total character count
                            total_chars += len(span["text"])

    # Close the document
    doc.close()

    # Calculate the percentage of text in each font category
    font_percentages = {font: len(text) / total_chars * 100 for font, text in font_data.items()}

    return font_percentages

def get_line_prevalent_font(line):
    # Dictionary to hold text grouped by font characteristics
    font_data = defaultdict(str)

    # Total character count
    total_chars = 0

    for span in line["spans"]:  # iterate through text spans
        if "size" in span and "font" in span:
            # Font identifier includes font name, size (rounded to nearest half), and boldness
            font_id = (span["font"], (span["size"]), "bold" in span["font"].lower())
            # Append text to the corresponding font category
            font_data[font_id] += span["text"]
            # Update total character count
            total_chars += len(span["text"])

    # Calculate the percentage of text in each font category
    font_percentages = {font: len(text) / total_chars * 100 for font, text in font_data.items()}

    # Determine the highest percentage
    percentages = list(font_percentages.values())
    max_percent = np.max(percentages)
    max_percent_index = percentages.index(max_percent)
    prevalent_font = list(font_percentages.keys())[max_percent_index]

    return prevalent_font

def find_body_font(file_path):
    font_percentages = analyze_pdf_fonts(file_path)

    # Determine the highest percentage - likely to be main text body
    percentages = list(font_percentages.values())
    max_percent = np.max(percentages)
    max_percent_index = percentages.index(max_percent)
    most_common_font = list(font_percentages.keys())[max_percent_index]

    return most_common_font



def get_text_font(file_path, search_text):
    """
    Finds the font information of the given text in the PDF.

    :param file_path: Path to the PDF file
    :param search_text: Text string to search for
    :return: Dictionary with font information or None if text is not found
    """
    doc = fitz.open(file_path)
    font_info = None

    for page in doc:
        text_instances = page.search_for(search_text)

        # If the text is found in the page
        if text_instances:
            # Extract text information from the first instance of the text
            text_info = page.get_text("dict", clip=text_instances[0])

            for block in text_info["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        font_info = get_line_prevalent_font(line)
                        break
                    if font_info:
                        break
                if font_info:
                    break
        if font_info:
            break

    doc.close()
    return font_info


def find_text_by_font(file_path, font_info):
    """
    Finds all text in the PDF that matches the given font information.

    :param file_path: Path to the PDF file
    :param font_info: Dictionary with font information (font, size, color, flags)
    :return: List of text strings that match the font information
    """
    if font_info == None:
        return 'sample text not found'
    doc = fitz.open(file_path)
    matching_texts = []

    for page in doc:
        text_info = page.get_text("dict")

        for block in text_info["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    line_acc = ''
                    for span in line["spans"]:
                        if ((span["font"] == font_info["font"] or span["font"] == f'{font_info["font"]}+fb') and
                                span["size"] == font_info["size"] and
                                span["color"] == font_info["color"] and
                                span["flags"] == font_info["flags"]):
                            line_acc = line_acc + span["text"]
                    if line_acc != '':
                        matching_texts.append(line_acc)

    doc.close()
    return matching_texts

def get_text_from_matching_font(filepath, sample_text):
    sample_text_font = get_text_font(filepath, sample_text)
    fetched_text = find_text_by_font(filepath, sample_text_font)
    return fetched_text

