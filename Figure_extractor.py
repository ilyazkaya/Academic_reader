from PyPDF2 import PdfFileReader
import fitz  # PyMuPDF
import os

# File path for the uploaded PDF
# pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC\Gollisch and Meister 2019 Eye Smarter than Scientists Believed Neural Computations in Circuits of the Retina.pdf'
pdf_path = r'C:\Users\il_ka\Main\Documents\Learning\BIOL\Awatramani\Papers\WAC\Bruggen 2014. Type 2 wide-field amacrine cells in TH-GFP mice show a homogenous synapse distribution and contact small ganglion cells.pdf'
paper_name = pdf_path.split('\\')[-1].replace('.pdf', '')
images_folder = os.path.join(r'C:\Users\il_ka\PycharmProjects\Academic_reader\images', paper_name)

# Create a directory for extracted images if it doesn't exist
if not os.path.exists(images_folder):
    os.makedirs(images_folder)


# Function to extract images from a PDF file
def extract_images_from_pdf(pdf_path, images_folder):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    image_count = 0

    # Iterate through each page
    for i in range(len(doc)):
        # Get the page
        page = doc.load_page(i)

        # Get the images in the page
        for img in page.get_images(full=True):
            # Get the XREF of the image
            xref = img[0]
            # Extract the image
            base_image = doc.extract_image(xref)
            image = base_image["image"]
            # Generate an image file name
            image_filename = f'image_page_{i + 1}_img_{xref}.png'
            image_path = os.path.join(images_folder, image_filename)
            # Save the image
            with open(image_path, "wb") as img_file:
                img_file.write(image)
            image_count += 1

    return image_count


# Extract images from the PDF
extracted_images_count = extract_images_from_pdf(pdf_path, images_folder)
extracted_images_count, images_folder
