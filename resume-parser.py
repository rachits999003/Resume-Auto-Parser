import tkinter as tk
from tkinter import filedialog, messagebox
import json
from pdfminer.high_level import extract_text
import os
from docx import Document

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text(file_path)
    elif ext == '.docx':
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return None
    
def parse_resume():
    file_path = filedialog.askopenfilename(filetypes=["PDF/DOCX files", "*.pdf *.docx"])
    if not file_path:
        return
        
    text = extract_text_from_file(file_path)

    if not text:
        messagebox.showerror("Error", "Unsupported file format")
        return
    
#Extracting name and email from the resume - Basic parsing
    lines = text.split("\n")
    extracted_data = {"Name" : lines[0].strip() if lines else "Unknown", "Email" : "Not found" }

#save to json

    json_path = file_path + ".json"
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4)
        messagebox.showinfo("Success", f"Resume parsed successfully! Data saved to {json_path}")

#GUI setup
root = tk.Tk()
root.title("Resume Parser")
root.geometry("300x100")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(pady=20)

tk.Label(frame, text = "Resume Auto Parser", font=("Helvetica", 16,"bold")).pack()
tk.Button(frame, text="Select Resume", command=parse_resume, font=("Arial", 12 )).pack(pady=10)

root.mainloop()