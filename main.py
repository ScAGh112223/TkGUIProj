# import customtkinter as cTk
# from customtkinter import filedialog

# import img2pdf
# from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from customtkinter.windows.ctk_tk import CTk
from __init__ import *
import tempfile
import img2pdf
import customtkinter as cTk

def merge_Pdfs(filenames: list, outputFilename: str = "", data = [], save: bool = True):
    merger = PdfMerger(outputFilename)

    [merger.append(p) for p in filenames]
    
    if data:
        merger.merge(data)

    with open(outputFilename, 'wb') as out:
        merger.write(out)

def images_to_pdf(filenames: list, outputFilename: str = "", save: bool = True):
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    if not save: return img2pdf.convert(filenames)
    with open(outputFilename, "wb") as file:
        file.write(img2pdf.convert(filenames, layout_fun = layout_fun))

def merge_all():
    t = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
    t.write(images_to_pdf(get_image_names(), save=False))
    t.flush()

    print(images_to_pdf(get_image_names(), save=False))
    print(t.read())
    
    merge_Pdfs(get_pdf_names() + [t.name], ask_pdf_save())
    
    t.close()

root = cTk.CTk()
root.title("Custom Tkinter Works!")

root.geometry("500x500")

tisa_font = cTk.CTkFont(family="Quicksand", size=15, weight="normal")
pdf_file_type = [("PDF Document", "*.pdf")]
image_file_types = [("JFIF Image", "*.jfif"), ("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("TIFF Image", ".tiff .tif")]
all_supported_file_types = [("Supported Files", [x[1] for x in pdf_file_type + image_file_types])]

print(all_supported_file_types)

get_image_names = lambda: [x for x in file_list.get(0, 'end') if not x.endswith(".pdf")]
get_pdf_names = lambda: [x for x in file_list.get(0, 'end') if x.endswith(".pdf")]
ask_pdf_save = lambda: filedialog.asksaveasfilename(filetypes = pdf_file_type)

load_files = lambda: [file_list.insert(i, fname) for i, fname in enumerate(filedialog.askopenfilenames(filetypes = all_supported_file_types))]
merge_pdfs = lambda: merge_Pdfs(file_list.get(0, 'end'), ask_pdf_save())
convert_images = lambda: images_to_pdf(get_image_names(), ask_pdf_save())

label_file_list = cTk.CTkLabel(root, textvariable="Loaded files: ", font=(tisa_font))
label_file_list1 = cTk.CTkLabel(root, text="Loaded files: ")
label_file_list.pack()
label_file_list1.pack()

file_list = Listbox(root, width = 100)
file_list.pack()

button_load_files = cTk.CTkButton(root, text="Load File(s)", command = load_files)
button_load_files.pack(pady=3)

button_merge = cTk.CTkButton(root, text="Merge Pdfs", command = merge_pdfs)
button_merge.pack(pady=3)

button_image_convert = cTk.CTkButton(root, text="Convert images to pdf", command = convert_images)
button_image_convert.pack(pady=3)

button_merge_all = cTk.CTkButton(root, text = "Merge All Images and PDFs", command = merge_all)
button_merge_all.pack(pady=20)

if (__name__ == "__main__"):
    root.mainloop()
