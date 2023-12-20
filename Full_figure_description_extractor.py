from Figure_description_extractor import extract_figure_descriptions
from Text_processor import get_text_from_matching_font
import os

folder_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC'
papers = {}
for filename in os.listdir(folder_path):
    # Check if the file is a PDF
    if filename.endswith('.pdf'):
        # Full path to the file
        file_path = os.path.join(folder_path, filename)
        figure_descriptions, page_texts = extract_figure_descriptions(file_path)
        if len(figure_descriptions) >=1:
            sample_text = figure_descriptions[0][13:43]
            if sample_text is not None and sample_text != '':
                all_figure_texts = get_text_from_matching_font(file_path, sample_text)
                papers[filename] = all_figure_texts
            else:
                papers[filename] = []
        else:
            papers[filename] = []