# import customtkinter as cTk
# from customtkinter import filedialog

# import img2pdf
# from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from tkinter.constants import ANCHOR
from customtkinter.windows.ctk_tk import CTk
from __init__ import *
import tempfile
import img2pdf
import customtkinter as cTk
import pdf2image
from PyPDF2 import PdfMerger
from PIL import ImageTk
from tkinter import Canvas
from PIL import Image

################################### MAKE THIS DRAGGABLE IF POSSIBLE
class List_Item(cTk.CTkLabel):
    def __init__(self, *args, text, **kwargs):

        super().__init__(*args, text=text, **kwargs)

        self.button_delete = cTk.CTkButton(self, width=1, height=1, text="X", command=self.remove_self, anchor="e")
        self.button_delete.grid(row=0, padx=(425,0), sticky="e")
    
    def remove_self(self):
        self.destroy()

class Image_Preview(cTk.CTkScrollableFrame):
    def __init__(self, *args, images, **kwargs):
        super().__init__(*args, height=args[0].winfo_height(), **kwargs)

        for img in images:
            self.create_image(img)
    
    def create_image(self, img):
        cTk.CTkButton(self, image=cTk.CTkImage(img, size=(400,400*1.41)), text="",).grid()

def merge_Pdfs(filenames: list, outputFilename: str = "", data = [], save: bool = True):
    merger = PdfMerger(outputFilename)

    [merger.append(p) for p in filenames]
    
    if not save:
        t = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
        merger.write(t.name)
        merger.close()
        t.flush()

        res = t.read()
        t.close()
        return res

    with open(outputFilename, 'wb') as out:
        merger.write(out)

def images_to_pdf(filenames: list, outputFilename: str = "", save: bool = True):
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)
    if not save: return img2pdf.convert(filenames)
    with open(outputFilename, "wb") as file:
        file.write(img2pdf.convert(filenames, layout_fun = layout_fun))

def merge_all(save:bool = True):
    t = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
    t.write(images_to_pdf(get_image_names(), save=False))
    t.flush()

    if not save: return merge_Pdfs(get_pdf_names() + [t.name], save=False)
    merge_Pdfs(get_pdf_names() + [t.name], set_output(ask_pdf_save()))
    
    t.close()

def handler(val):
    try: 
        if val=="Merge PDFs": merge_pdfs() 
        elif val=="Convert Images to PDF": convert_images()
        elif val=="Merge All": merge_all()
    except Exception:
        pass
    segment_button_merges.set("EMPTY")

def preview():
    merged = merge_all(save=False)

    for canvas in tabs.tab("Preview").winfo_children():
        canvas.pack_forget()

    images = pdf2image.convert_from_bytes(merged, poppler_path="poppler-0.68.0_x86\\poppler-0.68.0\\bin")
    canvases = [] 
    prFrame = Image_Preview(tabs.tab("Preview"), images=[])
    prFrame.pack(fill="both", expand=True)
    for img in images:
        prFrame.create_image(img)
        # w, h = img.size
        # cImg = cTk.CTkImage(light_image=img, dark_image=img, size=img.size)
        # canvas = cTk.CTkButton(tabs.tab("Preview"), image=cImg, text="")

        # # canvas.create_image(10, 10, image=cImg)
        # canvases.append(canvas)
        # canvas.pack()
    
    print(canvases)

cTk.set_appearance_mode("dark")

root = cTk.CTk()
root.title("PDF conversion utilities")

root.geometry("500x500")
root.iconbitmap("./icon.ico")

tabs = cTk.CTkTabview(root, height=500, width=450, command = preview)
tabs.add("Merge and Convert")
tabs.add("Preview")

tab_main = tabs.tab("Merge and Convert")
tab_main.configure(height=250)

tabs.tab("Preview").configure(width=250)

tabs.pack()

# Load custom font so that it can be used in theme
font_manager = cTk.FontManager() # Make Font Manager
font_manager.init_font_manager() # Initialize Manager
font_manager.load_font("Quicksand-VariableFont_wght.ttf") # Load custom font

cTk.ThemeManager.theme["CTkFont"] = {'family': 'Quicksand', 'size': 15, 'weight': 'normal'} # Set font for all text by setting font in font theme to custom loaded font

pdf_file_type = [("PDF Document", "*.pdf")] # File type for PDF file ( variable as it is used often )
image_file_types = [("JFIF Image", "*.jfif"), ("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("TIFF Image", ".tiff .tif")] # Image file types
all_supported_file_types = [("Supported Files", [x[1] for x in pdf_file_type + image_file_types])] # PDF and image files combined

get_filenames = lambda: [item.cget("text") for item in frame_file_list.winfo_children()]

get_image_names = lambda: [x for x in get_filenames() if not x.endswith(".pdf")] # Gets all loaded image filenames
get_pdf_names = lambda: [x for x in get_filenames() if x.endswith(".pdf")] # Gets all loaded PDF filenames
ask_pdf_save = lambda: filedialog.asksaveasfilename(filetypes = pdf_file_type) # Show prompt for saving PDF
set_output = lambda msg, clr = "green": [label_output.configure(text = f"Saved to: {msg}", text_color=clr), msg][1]

# Lambda function that loops over all files chosen by the user and adds each of them to the ListBox - Enumerate is needed as the insert() function requries and index
load_files = lambda: [List_Item(frame_file_list, text=fname).pack() for fname in filedialog.askopenfilenames(filetypes = all_supported_file_types)] # User can load any supported file type
merge_pdfs = lambda: merge_Pdfs(get_pdf_names(), set_output(ask_pdf_save())) # Lambda function to merge loaded PDFs and save to specified location
convert_images = lambda: images_to_pdf(get_image_names(), set_output(ask_pdf_save())) # Lambda function to convert loaded images to PDF and save to specified location

Image_Preview(tabs.tab("Preview"), images=[Image.open("icon.jpg")]).pack(fill="both", expand=True)

label_file_list = cTk.CTkLabel(tab_main, text="Loaded files: ") # Label the ListBox
label_file_list.pack(pady=(10, 0)) # Pack Label

frame_file_list = cTk.CTkFrame(tab_main, height=100) # Create a ListBox to show loaded files
frame_file_list.pack() # Pack ListBox

button_load_files = cTk.CTkButton(tab_main, text="Load File(s)", command = load_files)
button_load_files.pack(pady=(30, 20))

segment_button_merges = cTk.CTkSegmentedButton(tab_main, values=["Merge PDFs", "Convert Images to PDF", "Merge All"],
                                               command= handler)
segment_button_merges.pack()

label_output = cTk.CTkLabel(tab_main, text="", text_color="green")
label_output.pack()


if (__name__ == "__main__"):
    root.mainloop()
