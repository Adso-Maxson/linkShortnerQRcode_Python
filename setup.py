from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["tkinter", "PIL", "pyshorteners", "qrcode", "io"],
    "include_files": [],
    "excludes": ["test"],
}

# GUI applications require a different base on Windows (the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="EncurtadorURL_QRCode",
    version="1.0",
    description="Encurtador de URL com gerador de QR Code",
    options={"build_exe": build_exe_options},
    executables=[Executable("url_shortener_gui.py", base=base, icon=None)]
)