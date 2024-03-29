import xml.etree.ElementTree as ET

data = [
    {"image": rf"C:\Users\il_ka\PycharmProjects\Academic_reader\images\image_page_2_img_3.png", "text": "Description for image 1"},
    {"image": rf"C:\Users\il_ka\PycharmProjects\Academic_reader\images\image_page_4_img_11.png", "text": "Description for image 2"},
    # Add more images and descriptions as needed
]

root = ET.Element("images")
for item in data:
    image_element = ET.SubElement(root, "image")
    image_element.set("src", item["image"])
    text_element = ET.SubElement(image_element, "text")
    text_element.text = item["text"]

tree = ET.ElementTree(root)
tree.write("images.xml")