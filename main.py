from Figure_description_extractor_with_end import extract_figure_descriptions
from Text_processor import find_body_font, find_text_by_font
import os
from collections import defaultdict

folder_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC'
papers = defaultdict(dict)
for filename in os.listdir(folder_path):
    # Check if the file is a PDF
    if filename.endswith('.pdf'):
        # Full path to the file
        file_path = os.path.join(folder_path, filename)
        figure_descriptions, lines = extract_figure_descriptions(file_path)

        body_font = find_body_font(file_path)
        body_text = find_text_by_font(file_path, body_font)

        papers[filename]['figures'] = figure_descriptions
        papers[filename]['line'] = lines
        papers['filename'] = body_text