import sys
import subprocess
import importlib

Required_Modules = ["psutil"]

def Install_If_Missing(Modules):
    Failed = []
    for Mod in Modules:
        try:
            importlib.import_module(Mod)
        except ImportError:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", Mod, "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                importlib.import_module(Mod)
            except Exception as E:
                Failed.append((Mod, str(E)))
    return Failed

Failed_Modules = Install_If_Missing(Required_Modules)

if Failed_Modules:
    import tkinter as tk
    from tkinter import messagebox
    Root = tk.Tk()
    Root.withdraw()
    Msg = "[ ERROR ] Failed To Install Required Modules:\n\n"
    for Mod, Err in Failed_Modules:
        Msg += f"  >> {Mod}: {Err}\n"
    Msg += "\n[ FIX ] Run Manually:\n  pip install " + " ".join(m for m, _ in Failed_Modules)
    messagebox.showerror("MODULE INSTALL FAILED", Msg)
    Root.destroy()
    sys.exit(1)

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Files.PY.App import Main_App

if __name__ == "__main__":
    App = Main_App()
    App.mainloop()
