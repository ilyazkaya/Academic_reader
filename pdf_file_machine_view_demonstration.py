import fitz  # PyMuPDF
import json


def extract_text_with_attributes_all_pages(pdf_path):
    doc = fitz.open(pdf_path)
    all_text_info = []

    # Iterate through all pages
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block["type"] == 0:  # Text block
                for line in block["lines"]:
                    for span in line["spans"]:
                        text_info = {
                            "page": page_num + 1,
                            "text": span["text"],
                            "bbox": span["bbox"],
                            "font": span["font"],  # Font name
                            "size": span["size"],  # Font size
                            "color": span["color"]  # Text color in RGB
                        }
                        all_text_info.append(text_info)

    doc.close()
    return all_text_info


# Path to the PDF file
pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\Kim and Kerchensteiner 2017 W3 OMS.pdf'
text_with_coordinates = extract_text_with_attributes_all_pages(pdf_path)
json_output = json.dumps(text_with_coordinates, indent=4)