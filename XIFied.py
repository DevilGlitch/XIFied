import os
import tkinter as tk
from tkinter import filedialog, messagebox
from exif import Image
import datetime

# Function to generate a filename based on the current date and time
def generate_datetime_filename():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    return f"{timestamp}.jpg"

# Function to remove all EXIF and metadata from an image file using the exif package
def remove_all_metadata(image_path, output_folder):
    # Ensure the output folder exists in the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder_path = os.path.join(project_dir, output_folder)
    os.makedirs(output_folder_path, exist_ok=True)

    try:
        # Generate a filename based on the current date and time
        output_image_filename = generate_datetime_filename()

        # Open the image with EXIF metadata
        with open(image_path, 'rb') as image_file:
            my_image = Image(image_file)

        # Remove all EXIF data
        my_image.delete_all()

        # Create the path for the output file
        output_image_path = os.path.join(output_folder_path, output_image_filename)

        # Save the modified image with metadata removed
        with open(output_image_path, 'wb') as output_file:
            output_file.write(my_image.get_file())

        messagebox.showinfo("Success", f"Image saved in the '{output_folder}' folder with all metadata removed and a timestamp-based filename.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to handle the "Browse" button click
def browse_button():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if file_path:
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(0, file_path)

# Function to execute the image processing and display a message box
def process_image():
    input_file = entry_filepath.get()
    if not os.path.exists(input_file):
        messagebox.showerror("Error", "File not found.")
        return

    # Create a folder for images without any metadata in the project folder
    metadata_removed_folder = "MetadataRemoved"

    # Remove all EXIF and metadata using the exif package
    remove_all_metadata(input_file, metadata_removed_folder)

# Create the main application window
root = tk.Tk()
root.title("Remove All Image Metadata")

# Create and configure the user interface elements
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label_filepath = tk.Label(frame, text="Select an image file:")
label_filepath.grid(row=0, column=0, columnspan=2, pady=(0, 10))

entry_filepath = tk.Entry(frame, width=40)
entry_filepath.grid(row=1, column=0, padx=5)

button_browse = tk.Button(frame, text="Browse", command=browse_button)
button_browse.grid(row=1, column=1)

button_process = tk.Button(frame, text="Remove Metadata", command=process_image)
button_process.grid(row=2, column=0, columnspan=2, pady=(10, 0))

# Start the Tkinter main loop
root.mainloop()
