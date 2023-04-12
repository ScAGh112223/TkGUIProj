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
root.title("PDF conversion utilities")

root.geometry("500x500")
root.iconbitmap("./icon.ico")

# Load custom font so that it can be used in theme
font_manager = cTk.FontManager() # Make Font Manager
font_manager.init_font_manager() # Initialize Manager
font_manager.load_font("Quicksand-VariableFont_wght.ttf") # Load custom font

cTk.ThemeManager.theme["CTkFont"] = {'family': 'Quicksand', 'size': 15, 'weight': 'normal'} # Set font for all text by setting font in font theme to custom loaded font

pdf_file_type = [("PDF Document", "*.pdf")] # File type for PDF file ( variable as it is used often )
image_file_types = [("JFIF Image", "*.jfif"), ("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("TIFF Image", ".tiff .tif")] # Image file types
all_supported_file_types = [("Supported Files", [x[1] for x in pdf_file_type + image_file_types])] # PDF and image files combined


get_image_names = lambda: [x for x in file_list.get(0, 'end') if not x.endswith(".pdf")] # Gets all loaded image filenames
get_pdf_names = lambda: [x for x in file_list.get(0, 'end') if x.endswith(".pdf")] # Gets all loaded PDF filenames
ask_pdf_save = lambda: filedialog.asksaveasfilename(filetypes = pdf_file_type) # Show prompt for saving PDF

# Lambda function that loops over all files chosen by the user and adds each of them to the ListBox - Enumerate is needed as the insert() function requries and index
load_files = lambda: [file_list.insert(i, fname) for i, fname in enumerate(filedialog.askopenfilenames(filetypes = all_supported_file_types))] # User can load any supported file type
merge_pdfs = lambda: merge_Pdfs(file_list.get(0, 'end'), ask_pdf_save()) # Lambda function to merge loaded PDFs and save to specified location
convert_images = lambda: images_to_pdf(get_image_names(), ask_pdf_save()) # Lambda function to convert loaded images to PDF and save to specified location

label_file_list = cTk.CTkLabel(root, text="Loaded files: ") # Label the ListBox
label_file_list.pack() # Pack Label

file_list = Listbox(root, width = 100) # Create a ListBox to show loaded files
file_list.pack() # Pack ListBox
 
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
