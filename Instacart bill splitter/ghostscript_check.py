import numpy as np

import ctypes
from ctypes.util import find_library
string = find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))
print(string)
print(len(string))
import camelot
pdf_path = 'https://camelot-py.readthedocs.io/en/master/_static/pdf/foo.pdf'
# Use the `ghostscript` parameter to provide the path to Ghostscript
tables = camelot.read_pdf(pdf_path)

# Process the extracted tables as needed
for table in tables:
    print(table.df)