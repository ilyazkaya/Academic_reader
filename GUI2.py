import tkinter as tk
from tkinter import Frame, Label, Button, Canvas, Scrollbar
from PIL import Image, ImageTk

# Placeholder function for image change
def change_image(direction):
    print(f"Change image: {direction}")

# Main window
root = tk.Tk()
root.title("Image Viewer")

# Left panel with a scrollable image
left_panel = Frame(root)
left_panel.pack(side="left", fill="both", expand=True)

canvas = Canvas(left_panel)
scroll_y = Scrollbar(left_panel, orient="vertical", command=canvas.yview)

# Placeholder image for the scrollable area
img = Image.open("stacked_image.png")
img = ImageTk.PhotoImage(img)
canvas.create_image(0, 0, anchor="nw", image=img)

canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Right panel with image navigation
right_panel = Frame(root)
right_panel.pack(side="right", fill="both", expand=True)

# Placeholder image for the navigable area
# Replace 'placeholder.png' with your image file
img_label = Label(right_panel, image=img)
img_label.pack()

prev_button = Button(right_panel, text="Previous", command=lambda: change_image("previous"))
prev_button.pack(side="left")

next_button = Button(right_panel, text="Next", command=lambda: change_image("next"))
next_button.pack(side="right")

root.mainloop()
