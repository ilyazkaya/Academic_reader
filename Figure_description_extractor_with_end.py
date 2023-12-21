import re
import fitz  # PyMuPDF
import Text_processor as tp
import os

def get_line_text(line):
    _span_texts = [span['text'] for span in line['spans']]
    _line_text = ''.join(_span_texts)
    return _line_text

def find_figure_label(line):
    # Regular expression to match figure descriptions (e.g., Figure 1, Figure 2, etc.)
    # pattern = r'^(?:Figure|Fig)\.?\s\d+\.?'
    pattern = r'^(?:Figure|Fig)\.?\s\d+\.?(?:\s|$)'
    figure_regex = re.compile(pattern, re.MULTILINE)

    try:
        line_text = get_line_text(line)
        matches = figure_regex.finditer(line_text)
        figure_title = next(matches).group()
    except StopIteration:
        figure_title = None

    if figure_title == '':
        figure_title = None

    if figure_title != None:
        ind = len(figure_title)
        try:
            if line[ind+1].islower():
                figure_title = None
        except KeyError:
            pass

    return figure_title

def extract_figure_descriptions(pdf_path):
    pdf = fitz.open(pdf_path)
    descriptions = {}

    lines = []
    for page in pdf:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:  # block contains text
                for line in block['lines']:
                    lines.append(line)


    for l_count, line in enumerate(lines):
        figure_title = find_figure_label(line)
        if figure_title == None:
            continue

        # get figure description font
        figure_font = tp.get_line_prevalent_font(lines[l_count + 3])
        # print(f'figure label: {figure_title}')
        # TODO: remove this hack. The figure desc might be shorter than 3 lines.
        figure_desc_line_texts = []
        i = 0
        while i < 3:
            line_text = get_line_text(lines[l_count])
            figure_desc_line_texts.append(line_text)
            i += 1
            l_count += 1

        line_font = figure_font
        while figure_font == line_font:
            line_text = get_line_text(lines[l_count])
            # print(f'line: {line_text}')
            figure_desc_line_texts.append(line_text)
            l_count += 1
            line_font = tp.get_line_prevalent_font(lines[l_count])
            next_figure_label = find_figure_label(lines[l_count])
            if next_figure_label != None:
                break

        # concatenating lines
        figure_desc_text = ''
        for text in figure_desc_line_texts:
            if text[-1] == '-':
                text = text[:-1]
                figure_desc_text += text
            else:
                figure_desc_text += ' ' + text
        # TODO: remove the space that is inserted instead of the hyphen. No idea why it works this way...

        descriptions[figure_title] = figure_desc_text

    line_texts = [get_line_text(line) for line in lines]

    return descriptions, line_texts

# Extract figure descriptions
# pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC\Bruggen 2014. Type 2 wide-field amacrine cells in TH-GFP mice show a homogenous synapse distribution and contact small ganglion cells.pdf'
# pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC\Gollisch 2009 Eyes Smarter than Scientists Believed Neural Computations in Circuits of the Retina.pdf'
# pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC\Davenport 2007 Functional polarity of dendrites and axons of primate A1 amacrine cells.pdf'

# figure_descriptions = extract_figure_descriptions(pdf_path)

folder_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC'
paper_fig_descs = {}
paper_lines = {}
for filename in os.listdir(folder_path):
    # Check if the file is a PDF
    if filename.endswith('.pdf'):
        # Full path to the file
        file_path = os.path.join(folder_path, filename)
        figure_descriptions, lines = extract_figure_descriptions(file_path)
        paper_fig_descs[filename] = figure_descriptions
        paper_lines[filename] = lines

# TODO. Some papers failed all or some figures

#%%
filepath = 'delete.txt'
with open(filepath, 'w') as file:
    for line in paper_lines['Knop 2011 Inputs Underlying the ON–OFF Light Responses of Type 2 Wide-Field Amacrine Cells in TH-GFP Mice.pdf']:
        if 'Figure' in line:
            print(line)
            file.write(line + '\n')