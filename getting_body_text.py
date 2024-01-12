import Text_processor as tp
import os


folder_path = r'C:\Users\il_ka\PycharmProjects\Academic_reader\papers'
paper_body_texts = {}
for filename in os.listdir(folder_path):
    # Check if the file is a PDF
    if filename.endswith('.pdf'):
        # Full path to the file
        file_path = os.path.join(folder_path, filename)
        body_font = tp.get_most_common_font(file_path)
        body_text = tp.find_text_by_font(file_path, body_font)
        paper_body_texts[filename] = body_text

filepath = 'delete.txt'
for paper_path, lines in paper_body_texts.items():
    _, filename = os.path.split(paper_path)
    txt_filename = filename.replace('.pdf', '.txt')
    paper_text_folder = fr'C:\Users\il_ka\PycharmProjects\Academic_reader\paper_texts'
    paper_text_file = os.path.join(paper_text_folder, txt_filename)
    with open(paper_text_file, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line)