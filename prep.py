import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import os
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(True)
from ttkthemes import ThemedTk
import easyocr
import pandas as pd
reader = easyocr.Reader(['en'], gpu=True)
import spacy
import re


phone_pattern = r'\b(?:Phone:|Cell:|Cellular:|Tel:|Fax:|fFtT)?\s*([0-9+-]{6,12})\b'
name_pattern = r"^(?:Mr\.|Mrs\.|Dr\.|[a-zA-Z'\-,.][^0-9_!¡?÷?¿/\\+=@#$%^&*(){}|~<>;:[\]]{2,})$"
website_pattern = r"^(?:www\.[^\s.]+\.[a-zA-Z]{2,}|[^\s]+\.(?:com))$"
address_pattern = r"^[0-9A-Za-z\s,.-]+$"
designation_pattern = re.compile(r'(?i)\b(manager|director|engineer|analyst|supervisor|specialist|coordinator|administrator|consultant|executive)\b')


def checkName(val):
    if re.match(name_pattern, val):
        return True
    return False
def checkPhone(val):
    if re.match(phone_pattern, val):
        return True
    return False
def checkPhoneTwo(val):
    phone_pattern = re.compile(r'\b(?:Phone|Cell|Tel|P|T)?\s*(?:\+?\d{1,2}\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
    if re.findall(phone_pattern,val):
        return True 
    return False
def checkEmail(val):
    return '@' in val
def checkWebsite(val):
    if re.search(website_pattern, val):
        return True
    return False
def checkAddress(val):
    if re.search(address_pattern, val):
        return True
    return False
def checkDesignation(val):
    return bool(designation_pattern.search(val))

def getInfo(e):
    company_names = []
    person_names = []
    phone_numbers = []
    emails = []
    addresses = []
    designation = []
    txt=""
    for val in e:
        txt += val
        if checkEmail(val):
            split_result = val.split(" : ", 1)
            if len(split_result) > 1:
                result = split_result[1]
            else:
                result = val
                emails.append(result)
        if checkDesignation(val):
            designation.append(val)  
        if(checkName(val) and val.isupper()):
            person_names.append(val) 
        if(checkPhoneTwo(val) and phone_numbers.count(val)==0):
                    phone_numbers.append(val)

    return company_names, person_names, phone_numbers,emails,addresses,designation


def process_ocr(filename):
    img=filename
    dfs = []
    result = reader.readtext(img)
    img_id = img.split('/')[-1].split('.')[0]
    img_df = pd.DataFrame(result, columns=['bbox','text','conf'])
    img_df['img_id'] = img_id
    dfs.append(img_df)
    easyocr_df = pd.concat(dfs)
    company,person_name,phone,email,address,designation=getInfo(easyocr_df['text'])
    return (filename,company,person_name,phone,email,address,designation)



folder_path = "./upload"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def upload_image():
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg;*.png")])

    if file_path:
        # Save image in "upload" folder
        with open(f"./upload/{file_path.split('/')[-1]}", "wb") as f:
            f.write(open(file_path, "rb").read())

        # Show confirmation message
        tk.Label(root, text="Image uploaded successfully!").pack()
        filename, company, person_name, phone, email, address, designation = process_ocr(f"./upload/{file_path.split('/')[-1]}")

        # Join elements within each variable if it's a list
        filename = ' '.join(filename) if isinstance(filename, list) else filename
        company = ' '.join(company) if isinstance(company, list) else company
        person_name = ' '.join(person_name) if isinstance(person_name, list) else person_name
        phone = ' '.join(phone) if isinstance(phone, list) else phone
        email = ' '.join(email) if isinstance(email, list) else email
        address = ' '.join(address) if isinstance(address, list) else address
        designation = ' '.join(designation) if isinstance(designation, list) else designation

        tree.insert("", "end", values=(filename, company, person_name, phone, email, address, designation), tags=('entry',))

def edit_entry(event):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item)['values']

    # Check if values is not None and has the expected number of elements
    if values and len(values) == 7:
        open_canvas_window(*values)
    else:
        print("Error: Unexpected number of elements in values tuple.")

def print_entry(image_path, text_values):
    # Create a PDF file
    pdf_filename = "output.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Add image to the PDF
    c.drawImage(image_path, 100, 500, width=400, height=200)

    # Add text to the PDF
    text = "\n".join(text_values)
    c.setFont("Helvetica", 12)
    c.drawString(100, 400, text)

    # Save the PDF
    c.save()

    print(f"PDF created: {pdf_filename}")

def open_canvas_window(filename, company, person_name, phone, email, address, designation):
    # Create a new themed window named "Canvas"
    canvas_window = ThemedTk(theme="equilux")
    canvas_window.title("Canvas")

    # Input boxes for editing OCR output
    filename_var = tk.StringVar(value=filename)
    company_var = tk.StringVar(value=company)
    person_name_var = tk.StringVar(value=person_name)
    phone_var = tk.StringVar(value=phone)
    email_var = tk.StringVar(value=email)
    address_var = tk.StringVar(value=address)
    designation_var = tk.StringVar(value=designation)

    tk.Label(canvas_window, text="Filename:").grid(row=1, column=0)
    tk.Entry(canvas_window, textvariable=filename_var).grid(row=1, column=1, columnspan=5)
    tk.Label(canvas_window, text="Company:").grid(row=2, column=0)
    tk.Entry(canvas_window, textvariable=company_var).grid(row=2, column=1, columnspan=5)
    tk.Label(canvas_window, text="Person Name:").grid(row=3, column=0)
    tk.Entry(canvas_window, textvariable=person_name_var).grid(row=3, column=1, columnspan=5)
    tk.Label(canvas_window, text="Phone:").grid(row=4, column=0)
    tk.Entry(canvas_window, textvariable=phone_var).grid(row=4, column=1, columnspan=5)
    tk.Label(canvas_window, text="Email:").grid(row=5, column=0)
    tk.Entry(canvas_window, textvariable=email_var).grid(row=5, column=1, columnspan=5)
    tk.Label(canvas_window, text="Address:").grid(row=6, column=0)
    tk.Entry(canvas_window, textvariable=address_var).grid(row=6, column=1, columnspan=5)
    tk.Label(canvas_window, text="Designation:").grid(row=7, column=0)
    tk.Entry(canvas_window, textvariable=designation_var).grid(row=7, column=1, columnspan=5)

    # Submit button to save changes
    submit_button = tk.Button(canvas_window, text="Submit", command=lambda: save_changes(canvas_window, filename_var, company_var, person_name_var, phone_var, email_var, address_var, designation_var))
    submit_button.grid(row=8, column=0, columnspan=6, pady=10)

    # Print button to print image and text
    print_button = tk.Button(canvas_window, text="Print", command=lambda: print_entry(image_path, get_text_values(filename_var, company_var, person_name_var, phone_var, email_var, address_var, designation_var)))
    print_button.grid(row=9, column=0, columnspan=6, pady=10)

def get_text_values(*args):
    return [arg.get() for arg in args]

def save_changes(window, filename_var, company_var, person_name_var, phone_var, email_var, address_var, designation_var):
    # Get the updated values from the Entry widgets
    updated_filename = filename_var.get()
    updated_company = company_var.get()
    updated_person_name = person_name_var.get()
    updated_phone = phone_var.get()
    updated_email = email_var.get()
    updated_address = address_var.get()
    updated_designation = designation_var.get()

    # Get the selected item in the Treeview
    selected_item = tree.selection()[0]

    # Update the values in the Treeview
    tree.item(selected_item, values=(updated_filename, updated_company, updated_person_name, updated_phone, updated_email, updated_address, updated_designation))

    # Close the Canvas window
    window.destroy()

# Use ThemedTk for a modern theme
root = ThemedTk(theme="equilux")
root.title("High-Tech Tkinter App")

file_list_frame = tk.Frame(root)
file_list_frame.pack_forget()

# Create "Upload Image" button
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Filename", "Company", "Person Name", "Phone", "Email", "Address", "Designation"))
tree.pack(fill="both", expand=True)

# Style the Treeview
style = ttk.Style(root)
style.theme_use("equilux")
style.configure("Treeview", background="#2E2E2E", foreground="#FFFFFF", font=("Helvetica", 12))
style.map("Treeview", background=[("selected", "#004080")])

# Define column headings
tree.heading("Filename", text="Filename", anchor="center")
tree.heading("Company", text="Company", anchor="center")
tree.heading("Person Name", text="Person Name", anchor="center")
tree.heading("Phone", text="Phone", anchor="center")
tree.heading("Email", text="Email", anchor="center")
tree.heading("Address", text="Address", anchor="center")
tree.heading("Designation", text="Designation", anchor="center")

# Set column widths
tree.column("Filename", width=150)
tree.column("Company", width=150)
tree.column("Person Name", width=150)
tree.column("Phone", width=100)
tree.column("Email", width=200)
tree.column("Address", width=250)
tree.column("Designation", width=150)

# Add "Edit" and "Print" buttons for each entry
tree.tag_configure('entry', background='#2E2E2E', foreground='#FFFFFF')
tree.tag_bind('entry', '<Button-1>', edit_entry)
tree.tag_bind('entry', '<Button-3>', print_entry)

root.mainloop()
