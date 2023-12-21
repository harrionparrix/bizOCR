# OCR Image Processing Application

This application utilizes Optical Character Recognition (OCR) to extract information from images containing text. The extracted data is displayed in a Tkinter GUI, where users can edit the information, print it, and upload a profile picture.

## Prerequisites

Make sure you have the necessary libraries installed:

```bash
pip install tkinter pillow easyocr pandas spacy reportlab ttkthemes
```

## Usage

1. Run the application by executing the script in a Python environment.
   
```bash
python your_script_name.py
```

2. Click the "Upload Image" button to select an image file containing text.

3. The uploaded image and its extracted information will be displayed in the Treeview widget.

4. To edit the information, right-click on an entry in the Treeview and choose "Edit."

5. To print the information, right-click on an entry in the Treeview and choose "Print." This will create a PDF document with the extracted details.

6. Optionally, you can upload a profile picture for a specific entry by right-clicking and choosing "Profile Picture Upload."

## Features

- Image Upload: Select an image file for OCR processing.
- OCR Processing: Extract text information from the uploaded image using the EasyOCR library.
- Information Display: Display extracted information in a Treeview widget with columns for Filename, Company, Person Name, Phone, Email, Address, and Designation.
- Editing: Right-click on an entry to edit the information.
- Printing: Right-click on an entry to print the information as a PDF document.
- Profile Picture Upload: Upload a profile picture for a specific entry.

## Note

- The application uses the Tkinter library for the graphical user interface.
- OCR processing is done using the EasyOCR library.
- Editing and printing options are available through the right-click context menu in the Treeview.
- Ensure that all required dependencies are installed before running the application.

Feel free to customize and extend the application based on your specific needs!