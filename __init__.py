import subprocess, sys, importlib # Packages needed to install and import dependencies

dependencies = ["customtkinter", "PyPDF2", "img2pdf", "pdf2image", "tempfile", "pdf2image", "os"] # List of deps to install
sub_packages = [("cTk", "filedialog"), ("PyPDF2", "PdfWriter"), ("PyPDF2", "PdfMerger")] # Sub-packages to import
custom_names = [("customtkinter", "cTk")] # Proxy names to set
 
__all__ = [] # Initialize __all__ so that imported deps can be acessed

for dep in dependencies: # Loop over deps
    dep_name = dep # Make variable for name in case proxy needs to be used

    # Find proxy name and if one is found, set name variable to proxy name
    c_name = [t[1] for t in custom_names if t[0] == dep]
    if c_name: dep_name = c_name[0]
    
    try: # Try except in case dep is not installed
        exec(f"{dep_name} = importlib.import_module('{dep}')") # Import dep
    except ImportError: # In case dep is not installed
        # Install dep
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep],
                        stdout = subprocess.DEVNULL,
                        stderr = subprocess.STDOUT)

        exec(f"{dep_name} = importlib.import_module('{dep}')") # Import dep
    __all__.append(dep_name) # Append imported dep to __all__


for dep, sub in sub_packages: # Loop over sub packages
    exec(f"{sub} = {__all__[__all__.index(dep)]}.{sub}") # Import sub package
    __all__.append(sub) # Append sub package to __all__
    
