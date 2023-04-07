# import customtkinter as cTk
# from customtkinter import filedialog

# import img2pdf
# from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from __init__ import *

def merge_Pdfs(filenames: list, outputFilename: str = "", data = [], save: bool = True):
    merger = PdfMerger(outputFilename)

    [merger.append(p) for p in filenames]
    
    if data:
        merger.merge(data)

    with open(outputFilename, 'wb') as out:
        merger.write(out)

def images_to_pdf(filenames: list, outputFilename: str = "", save: bool = True):
    if not save: return img2pdf.convert(filenames)
    with open(outputFilename, "wb") as file:
        file.write(img2pdf.convert(filenames))

root = cTk.CTk()
root.title("Custom Tkinter Works!")

root.geometry("500x500")

pdf_file_type = [("PDF Document", "*.pdf")]
image_file_types = [("JFIF Image", "*.jfif"), ("PNG Image", "*.png"), ("JPEG Image", "*.jpg")]
all_supported_file_types = pdf_file_type + image_file_types

print(all_supported_file_types)

get_image_names = lambda: [x for x in file_list.get(0, 'end') if not x.endswith(".pdf")]
get_pdf_names = lambda: [x for x in file_list.get(0, 'end') if x.endswith(".pdf")]

load_files = lambda: [file_list.insert(i, fname) for i, fname in enumerate(filedialog.askopenfilenames(filetypes = all_supported_file_types))]
merge_pdfs = lambda: merge_Pdfs(file_list.get(0, 'end'), filedialog.asksaveasfilename(filetypes = pdf_file_type))
convert_images = lambda: images_to_pdf(get_image_names(), filedialog.asksaveasfilename(filetypes = pdf_file_type))
merge_all = lambda: merge_Pdfs(get_pdf_names(), data=images_to_pdf(get_image_names(), save=False))

file_list = Listbox(root, width = 100)
file_list.pack()

button_load_files = cTk.CTkButton(root, text="Load File(s)", command = load_files)
button_load_files.pack()

button_merge = cTk.CTkButton(root, text="Merge Pdfs", command = merge_pdfs)
button_merge.pack()

button_merge_all = cTk.CTkButton(root, text = "Merge All Images and PDFs", command = merge_all)
button_merge_all.pack()

button_image_convert = cTk.CTkButton(root, text="Convert images to pdf", command = convert_images)
button_image_convert.pack()

if (__name__ == "__main__"):
    root.mainloop()
