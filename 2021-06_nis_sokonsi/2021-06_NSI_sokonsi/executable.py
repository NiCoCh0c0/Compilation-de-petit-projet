import sys
from cx_Freeze import setup, Executable

includefiles = ['AffichageCarte.py', 'InitalisationNiveau.py', 'Personnage.py', 'SauvegardeCarte.txt', 'Sprite']
includes = ["tkinter"]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Sokonsi",
    version="1.0",
    description="Sokonsi",
    options={"build_exe": {'include_files':includefiles, 'includes': includes}},
    executables=[Executable("Principal.py", base=base)]
)

