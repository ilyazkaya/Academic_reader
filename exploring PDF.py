import fitz  # PyMuPDF

file_path = fr'C:\Users\il_ka\PycharmProjects\Academic_reader\papers\Knop 2013 Morphological and physiological properties of enhanced green fluorescent protein (EGFP)-expressing wide-field amacrine cells in the ChAT-EGFP mouse line.pdf'
doc = fitz.open(file_path)
acc = []
page = doc[0]
blocks = page.get_text("dict")["blocks"]
for block in blocks:
   acc.append(block)
