from itertools import cycle
from PIL import Image, ImageTk
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Image Slideshows Viewer")

# List of image file paths
image_paths = [
    r"C:\Users\HP\Pictures\IMG_20230803_172042_1-02.jpeg",
    r"C:\Users\HP\Documents\WhatsApp Image 2024-11-17 at 20.12.37_cb22929a.jpg",
    r"C:\Users\HP\Documents\WhatsApp Image 2024-11-17 at 20.12.36_037f798a.jpg",
    r"C:\Users\HP\Documents\WhatsApp Image 2024-11-12 at 05.50.37_0e1c3b85.jpg",
    r"C:\Users\HP\Downloads\ChatGPT Image Jun 17, 2025, 05_23_50 AM.png",
]

# Resize all images
image_size = (1080, 1080)
images = [Image.open(path).resize(image_size) for path in image_paths]
photo_images = [ImageTk.PhotoImage(img) for img in images]

# Create a label to display images
label = tk.Label(root)
label.pack()

# Create an iterator over the images
slideshow = cycle(photo_images)

def update_image():
    next_image = next(slideshow)
    label.config(image=next_image)
    root.after(3000, update_image)  # Call this function again after 3 seconds

# Button to start the slideshow
play_button = tk.Button(root, text="Play Slideshow", command=update_image)
play_button.pack()

# Start the Tkinter event loop
root.mainloop()
 