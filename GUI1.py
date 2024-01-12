import fitz  # PyMuPDF
import matplotlib.pyplot as plt
import numpy as np

def display_pdf(pdf_path, page_number):
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Select a page
    page = doc.load_page(page_number)

    # Render the page to an image
    pix = page.get_pixmap()

    # Convert the image to a numpy array
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

    # Display the image
    plt.imshow(img)
    plt.axis('off')  # Turn off axis numbers
    plt.savefig('delete_page.png')
    plt.show()

# Example usage
pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC\Knop 2011 Inputs Underlying the ON–OFF Light Responses of Type 2 Wide-Field Amacrine Cells in TH-GFP Mice.pdf'
display_pdf(pdf_path, 0)  # Display the first page
