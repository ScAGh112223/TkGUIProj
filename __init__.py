import subprocess, sys, importlib

dependencies = ["customtkinter", "PyPDF2", "img2pdf", "tkinter"]
sub_packages = [("cTk", "filedialog"), ("tkinter", "Listbox"), ("PyPDF2", "PdfWriter"), ("PyPDF2", "PdfMerger")]
custom_names = [("customtkinter", "cTk")]

__all__ = []

for dep in dependencies:
    dep_name = dep

    c_name = [t[1] for t in custom_names if t[0] == dep]
    if c_name: dep_name = c_name[0]
    
    try:
        exec(f"{dep_name} = importlib.import_module('{dep}')")
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep],
                        stdout = subprocess.DEVNULL,
                        stderr = subprocess.STDOUT)

        exec(f"{dep_name} = importlib.import_module('{dep}')")
    __all__.append(dep_name)


for dep, sub in sub_packages:
    exec(f"{sub} = {__all__[__all__.index(dep)]}.{sub}")
    __all__.append(sub)

print(__all__)
