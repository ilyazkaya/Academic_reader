import re
import fitz  # PyMuPDF
import Text_processor as tp



# Function to extract text from PDF and search for figure descriptions
def extract_figure_descriptions(pdf_path):
    pdf = fitz.open(pdf_path)
    descriptions = {}

    # Regular expression to match figure descriptions (e.g., Figure 1, Figure 2, etc.)
    pattern = r'^(?:Figure|Fig)\.?\s\d+\.\s'
    figure_regex = re.compile(pattern, re.MULTILINE)

    # Combine text from all pages
    page_text_list = [page.get_text() for page in pdf]
    total_text = '\n'.join(page_text_list)
    if total_text:
        desc_font = None
        # Find all figure descriptions in the text
        for match in figure_regex.finditer(total_text):
            figure_title = match.group()
            # Extract the description following the figure title
            start_idx = match.end()
            end_idx = start_idx + 5000  # Arbitrary length for description
            if end_idx > len(total_text):
                end_idx = len(total_text)
            figure_description = total_text[start_idx:end_idx]
            # determining end of the figure description
            if desc_font is None:
                text_sample = figure_description[0:40]
                desc_font = tp.get_text_font(pdf_path, text_sample)
            fig_desc_lines = figure_description.split('\n')
            trunc_fig_desc = ''
            for line in fig_desc_lines:
                if tp.get_text_font(pdf_path, line) == desc_font:
                    trunc_fig_desc = fr'{trunc_fig_desc}{line}\n'
                else:
                    break
            descriptions[figure_title] = trunc_fig_desc

    pdf.close()
    return descriptions, total_text

def get_line_text(line):
    _span_texts = [span['text'] for span in line['spans']]
    _line_text = ''.join(_span_texts)
    return _line_text

def extract_figure_descriptions_(pdf_path):
    pdf = fitz.open(pdf_path)
    descriptions = {}

    # Regular expression to match figure descriptions (e.g., Figure 1, Figure 2, etc.)
    pattern = r'^(?:Figure|Fig)\.?\s\d+\.\s'
    figure_regex = re.compile(pattern, re.MULTILINE)

    lines = []
    for page in pdf:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:  # block contains text
                for line in block['lines']:
                    lines.append(line)


    for l_count, line in enumerate(lines):
        try:
            _line_text = get_line_text(line)
            matches = figure_regex.finditer(_line_text)
            figure_title = next(matches).group()
        except StopIteration:
            continue

        # get figure description font
        figure_font = tp.get_line_prevalent_font(lines[l_count + 3])

# TODO: remove this hack. The figure desc might be shorter than 3 lines.
        figure_desc_line_texts = []
        i = 0
        while i < 3:
            line_text = get_line_text(lines[l_count])
            figure_desc_line_texts.append(line_text)
            i += 1
            l_count += i

        line_font = figure_font
        while figure_font == line_font:
            line_text = get_line_text(lines[l_count])
            figure_desc_line_texts.append(line_text)
            l_count += 1
            line_font = tp.get_line_prevalent_font(lines[l_count])

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

    return descriptions, lines

# Extract figure descriptions
pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC\Gollisch 2009 Eyes Smarter than Scientists Believed Neural Computations in Circuits of the Retina.pdf'

figure_descriptions, lines = extract_figure_descriptions_(pdf_path)
