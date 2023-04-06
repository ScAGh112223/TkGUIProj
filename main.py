import customtkinter as cTk
from customtkinter import filedialog

import img2pdf
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

def merge_Pdfs(filenames: list, outputFilename: str):
    merger = PdfMerger(outputFilename)

    [merger.append(p) for p in filenames]
    
    with open(outputFilename, 'wb') as out:
        merger.write(out)

def images_to_pdf(filenames: list, outputFilename: str):
    with open(outputFilename, "wb") as file:
        file.write(img2pdf.convert(filenames))

root = cTk.CTk()
root.title("Custom Tkinter Works!")

root.geometry("500x500")

list_merge = cTk.CTkLabel(root, text="Label 1")
list_merge.pack()

pdf_file_type = [("PDF Document", "*.pdf")]
image_file_types = [("PDF Document", "*.pdf")]

button_merge = cTk.CTkButton(root, text="Merge Pdfs", command=lambda: merge_Pdfs(filedialog.askopenfilenames(filetypes=pdf_file_type), filedialog.asksaveasfilename(defaultextension=".pdf", filetypes = pdf_file_type)))
button_merge.pack()

button_image_convert = cTk.CTkButton(root, text="Convert images to pdf", command=lambda: images_to_pdf(filedialog.askopenfilenames(filetypes=image_file_types), filedialog.asksaveasfilename(defaultextension=".pdf", filetypes = pdf_file_type)))
button_image_convert.pack()

if (__name__ == "__main__"):
    root.mainloop()