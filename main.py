from __init__ import * # Import everything needed into file(using this way as it also installs required packages as well)

# Custom Widget - Label with a delete button on the right
class List_Item(cTk.CTkLabel): 
    def __init__(self, *args, text, **kwargs): # Init with self, text and *args as well as **kwargs(both required for custom tkinter stuff, just followed instructions)

        super().__init__(*args, text=text, **kwargs) # Intialize custom tkitner Label with *args, text and **kwargs

        self.button_delete = cTk.CTkButton(self, width=1, height=1, text="X", command=self.__remove_self, anchor="e") # Create the delete button with a X, small width, height and function to delete button(anchor is to align to east or right)
        self.button_delete.grid(row=0, padx=(425,0)) # Grid the button onto master widget and add padding to the left to align to right(works with east anchor)
    
    # Private function
    def __remove_self(self): # Deletes Label and Button
        self.destroy() # Destroy self

# Custom Widget - Scrollable frame with scaled images inside
class Image_Preview(cTk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs): # Init with self, *args and **kwargs(both required for custom tkinter stuff, just followed instructions)

        super().__init__(*args, **kwargs) # Intialize custom tkitner Label with *args, text and **kwargs

        self.width = self.master.winfo_reqwidth()

        self.master.bind("<Configure>", self.__refresh) # Bind window resize to refresh
        self.images = [] # intialize list of images
    
    def create_image(self, img): # Function to create image
        '''Adds image into preview
        
        @params:
            img - PIL image to add to preview'''
        # Create button with no text and apply image to it (best way that i have tried to display and image) and make the command show the image expanded
        # Also Convert the image to cTkImage with proper height and width(to make the approximate aspect ration of A4 paper - 1.41)
        button_image = cTk.CTkButton(self, image=cTk.CTkImage(img, size=(self.width,self.width*1.41)), text="", command=img.show)
        button_image.grid(sticky="ew", padx=(button_image.cget("width")/10, 0)) # Grid image onto master widget and add padding to left(10th of the image's width, seems to put the image around the center-ish)

        self.images.append(button_image) # Append image onto images array

    def get_images(self): # Gets all images in preview
        '''Get all loaded images
        
        @returns:
            Array with loaded PIL images'''
        return [imgButton.cget("image").cget("light_image") for imgButton in self.images] # Return the light_image attribute of the image attribute of every button in images array
    
    def __refresh(self, event): # Resizes images - Private Function
        # If statements to make sure that the imae is not too too big
        img_w = event.width/1.5 if event.width*1.41 < event.height else event.width/1.5
        img_h = img_w*1.41 # Make height a little more than width to maintain A4 aspect ratio

        for img in self.images: # Do this for every image previewd
            img.cget("image").configure(size=(img_w, img_h)) # Set size of images
            img.grid_configure(padx=(img_w/10, 0)) # Set padding of images

# Merges PDFs
def merge_Pdfs(filenames: list, save: bool = True, outputFilename: str = ""):
    '''Merges provided PDFs
    
    @params:
        filenames - list of PDF filenames to merge
        save - whether to save the merged file or not (returns PDF file in bytes if False)
        outputFilename - filename of output PDF(leave blank if save is False)
    @returns:
        PDF file in bytes if save is False'''
    merger = PdfMerger(outputFilename) # Create PDF merger(from PyPDF2) on output path

    [merger.append(p) for p in filenames] # Add all filenames to merged file
    
    if not save: # If the user doesn't want to save to file
        t = tempfile.NamedTemporaryFile(mode="w+b", delete=False) # Make temporary file that writes and reads bytes(w+b) and has to be closed manually
        
        merger.write(t.name) # Write merged data to temp file(only way to get data out of PdfMerger)
        merger.close() # Close merger
        
        t.flush() # Flush file stream as if you don't, file appears blank

        res = t.read() # Read bytes into res variable
        t.close() # Delete temp file

        return res # Return bytes

    # Open output file and write to it
    with open(outputFilename, 'wb') as out:
        merger.write(out)

# Converts images to PDF
def images_to_pdf(filenames: list, save: bool = True, outputFilename: str = ""):
    '''Converts input images into a single PDF
    
    @params:
        filenames - List of image filenames
        save - whether to save the converted file or not (returns PDF file in bytes if False)
        outputFilename - filename of output PDF(leave blank if save is False)
    @returns:
        PDF file in bytes if save is False'''
    
    i = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297)) # Convert input to A4 size and aspect ration - COPIED FROM INTERNET
    layout_fun = img2pdf.get_layout_fun(i) # ALSO COPIED FROM INTERNET

    if not save: return img2pdf.convert(filenames) # if user wants data, return just the data

    # Open and write data to output file
    with open(outputFilename, "wb") as file:
        file.write(img2pdf.convert(filenames, layout_fun = layout_fun))

# Merges all files - NOT FOR MODULE USE so private
def __merge_all(save:bool = True):
    '''Merges all loaded files
    
    @params:
        save - Whether to save merged file
    @returns:
        PDF file int bytes if save is False'''
    names = get_pdf_names() # Get jsut PDF names in case there are no image names

    t = tempfile.NamedTemporaryFile(mode="w+b", delete=False) # Create temp file to be able to use filenames for images
    try: 
        t.write(images_to_pdf(get_image_names(), save=False)) # Write images PDF to temp file
        names = names + [t.name] # Add images PDF to names if an error doesnt occur
    except ValueError: # If error occurs, pass
        pass
    t.flush() # Flush so that the temp file doesn't read as empty

    if not save: # If save false
        t.close() # Delete Temp file
        return merge_Pdfs(names, save=False) # Return merged PDF bytes
    
    print(names)
    merge_Pdfs(names, True, set_output(ask_pdf_save())) # Save to prompted location
    t.close() # delete temp file

# Handler for merge segmented button no docstring needed as private
def __handler(val):
    try: # Try Except in case merge fails(usually because there are no files loaded)
        if val=="Merge PDFs": merge_pdfs() # Merge just the PDFs
        elif val=="Convert Images to PDF": convert_images() # Convert Images
        elif val=="Merge All": __merge_all() # Merge everything
    except Exception: # If merge fails, just pass
        pass
    segment_button_merges.set("EMPTY") # Unselect option on segmented button

# Previews loaded files no dosctring needed as private
def __preview():
    global cached_names # Acess global cache to improve load times
    if(tabs.get() != "Preview" or get_filenames() == cached_names): return # Prevent re-loading on changing to main tab or if there have been no changes

    merged = __merge_all(save=False) # get merged byte data

    for canvas in tabs.tab("Preview").winfo_children(): # Go through previous preview's children widgets
        canvas.pack_forget() # Delete old preview

    images = pdf2image.convert_from_bytes(merged, poppler_path="poppler-0.68.0_x86\\poppler-0.68.0\\bin") # Set up pdf2image with poppler_path and convert bytes to PIL images
    prFrame = Image_Preview(tabs.tab("Preview")) # Create preview widget on preview tab
    prFrame.pack(fill="both", expand=True) # Pack the preview so that it fills available space

    for img in images: # Go through pages of PDF
        prFrame.create_image(img) # Add page to preview
    
    cached_names = get_filenames() # Cache current pages

cTk.set_appearance_mode("dark") # Set colour scheme to dark

root = cTk.CTk() # Create root window
root.title("PDF conversion utilities") # Set title

root.geometry("500x500") # Set default window size
root.iconbitmap("./icon.ico") # Set icon

height = root.winfo_height() # Get height
width = root.winfo_width() # Get width

cached_names = [""] # Initialize preview cache

tabs = cTk.CTkTabview(root, height=height, width=width-50, command = __preview) # Create tabview and set height, width as well as handler
tabs.add("Merge and Convert") # Add Merge and Convert Section
tabs.add("Preview") # Add preview section

tab_main = tabs.tab("Merge and Convert") # Get main tab as it is mentioned a lot
tab_main.configure(width=width/2) # Set appropriate width

tabs.tab("Preview").configure(width=width) # Set preview width

tabs.pack(fill="both", expand=True) # Pack tabs to fill available space

# Load custom font so that it can be used in theme
font_manager = cTk.FontManager() # Make Font Manager
font_manager.init_font_manager() # Initialize Manager
font_manager.load_font("Quicksand-VariableFont_wght.ttf") # Load custom font

cTk.ThemeManager.theme["CTkFont"] = {'family': 'Quicksand', 'size': 15, 'weight': 'normal'} # Set font for all text by setting font in font theme to custom loaded font

pdf_file_type = [("PDF Document", "*.pdf")] # File type for PDF file ( variable as it is used often )
image_file_types = [("JFIF Image", "*.jfif"), ("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("TIFF Image", ".tiff .tif")] # Image file types
all_supported_file_types = [("Supported Files", [x[1] for x in pdf_file_type + image_file_types])] # PDF and image files combined

get_filenames = lambda: [item.cget("text") for item in frame_file_list.winfo_children()] # Gets filenames of all files loaded

get_image_names = lambda: [x for x in get_filenames() if not x.endswith(".pdf")] # Gets all loaded image filenames
get_pdf_names = lambda: [x for x in get_filenames() if x.endswith(".pdf")] # Gets all loaded PDF filenames
ask_pdf_save = lambda: filedialog.asksaveasfilename(filetypes = pdf_file_type) # Show prompt for saving PDF
set_output = lambda msg, clr = "green": [label_output.configure(text = f"Saved to: {msg}", text_color=clr), msg][1] # Sets output text and returns the input

# Lambda function that loops over all files chosen by the user and adds each of them as List Item
load_files = lambda: [List_Item(frame_file_list, text=os.path.basename(fname)).pack() for fname in filedialog.askopenfilenames(filetypes = all_supported_file_types)] # User can load any supported file type
merge_pdfs = lambda: merge_Pdfs(get_pdf_names(), True, set_output(ask_pdf_save())) # Lambda function to merge loaded PDFs and save to specified location
convert_images = lambda: images_to_pdf(get_image_names(), True, set_output(ask_pdf_save())) # Lambda function to convert loaded images to PDF and save to specified location


label_file_list = cTk.CTkLabel(tab_main, text="Loaded files: ") # Label the Files list
label_file_list.pack(pady=(10, 0)) # Pack Label

frame_file_list = cTk.CTkFrame(tab_main, height=100) # Create a Frame to show loaded files
frame_file_list.pack() # Pack Frame

button_load_files = cTk.CTkButton(tab_main, text="Load File(s)", command = load_files) # Create button for user to load files
button_load_files.pack(pady=(30, 20)) # Pack load file button

# Create button for all merge options and set handler as command
segment_button_merges = cTk.CTkSegmentedButton(tab_main, values=["Merge PDFs", "Convert Images to PDF", "Merge All"],
                                               command= __handler)
segment_button_merges.pack() # Pack merge buttons

label_output = cTk.CTkLabel(tab_main, text="", text_color="green") # Output text label
label_output.pack() # Pack output


if (__name__ == "__main__"): # Only show UI if file is not being used as module
    root.mainloop() # Run mainloop
