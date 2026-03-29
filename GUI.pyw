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
import math
import getpass
import platform
import psutil
import tkinter as tk
import random
import time
from datetime import datetime

BG_Black     = "#000000"
BG_Matrix    = "#010b01"
BG_Panel     = "#030f03"
BG_Card      = "#050f05"
BG_Card2     = "#071207"
Green_Bright = "#00ff41"
Green_Mid    = "#00cc33"
Green_Dim    = "#008f11"
Green_Faint  = "#004d0a"
Green_Ghost  = "#001a03"
Amber        = "#ffb300"
Cyan         = "#00ffcc"
Red_Hack     = "#ff2222"
Text_Green   = "#00ff41"
Text_Dim     = "#008f11"
Text_Ghost   = "#004d0a"
Border_Green = "#003508"
Border_Bright= "#00ff41"

Font_Mono_Big   = ("Cascadia Code", 26, "bold")
Font_Mono_Med   = ("Cascadia Code", 13, "bold")
Font_Mono_Sm    = ("Cascadia Code", 10)
Font_Mono_Xs    = ("Cascadia Code", 9)
Font_Mono_Xxs   = ("Cascadia Code", 8)
Font_Mono_Num   = ("Cascadia Code", 32, "bold")
Font_Mono_Label = ("Cascadia Code", 9)

Total_Threads = os.cpu_count() or 1

if Total_Threads <= 8:
    Mine_Threads = 1
elif Total_Threads <= 14:
    Mine_Threads = 2
elif Total_Threads <= 20:
    Mine_Threads = 3
else:
    Mine_Threads = math.floor(Total_Threads * 0.20)

Thread_Percent = min(100, math.ceil((Mine_Threads / Total_Threads) * 100))


def Get_System_Info():
    Mem   = psutil.virtual_memory()
    Disk  = psutil.disk_usage("C:\\")
    Freq  = psutil.cpu_freq()
    Freq_Max = round(Freq.max / 1000, 2) if Freq else "N/A"
    Freq_Cur = round(Freq.current / 1000, 2) if Freq else "N/A"
    Cpu_Pct  = psutil.cpu_percent(interval=0.3)
    return {
        "cpu_name":     platform.processor() or "Unknown CPU",
        "cpu_cores":    psutil.cpu_count(logical=False) or "N/A",
        "cpu_threads":  Total_Threads,
        "cpu_freq_max": Freq_Max,
        "cpu_freq_cur": Freq_Cur,
        "cpu_pct":      Cpu_Pct,
        "mine_threads": Mine_Threads,
        "thread_pct":   Thread_Percent,
        "ram_total":    round(Mem.total   / (1024 ** 3), 1),
        "ram_used":     round(Mem.used    / (1024 ** 3), 1),
        "ram_free":     round(Mem.available / (1024 ** 3), 1),
        "ram_pct":      Mem.percent,
        "disk_total":   round(Disk.total  / (1024 ** 3), 1),
        "disk_used":    round(Disk.used   / (1024 ** 3), 1),
        "disk_free":    round(Disk.free   / (1024 ** 3), 1),
        "disk_pct":     round(Disk.percent, 1),
        "os_name":      platform.system() + " " + platform.release(),
        "os_build":     platform.version()[:50] + "..." if len(platform.version()) > 50 else platform.version(),
        "arch":         platform.architecture()[0],
        "username":     getpass.getuser(),
        "hostname":     platform.node(),
        "python_ver":   platform.python_version(),
    }


class Matrix_Rain(tk.Canvas):
    Chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ#@$%&"

    def __init__(self, Parent, **Kw):
        super().__init__(Parent, highlightthickness=0, bd=0, **Kw)
        self.Cols     = []
        self.Drops    = []
        self.Col_W    = 16
        self.Running  = True
        self.after(100, self._Init_Rain)

    def _Init_Rain(self):
        W = self.winfo_width()
        H = self.winfo_height()
        if W < 2 or H < 2:
            self.after(100, self._Init_Rain)
            return
        Num_Cols = max(1, W // self.Col_W)
        self.Cols  = list(range(Num_Cols))
        self.Drops = [random.randint(-40, 0) for _ in range(Num_Cols)]
        self._Draw()

    def _Draw(self):
        if not self.Running:
            return
        W = self.winfo_width()
        H = self.winfo_height()
        if W < 2 or H < 2:
            self.after(80, self._Draw)
            return
        self.delete("all")
        self.create_rectangle(0, 0, W, H, fill=BG_Black, outline="")
        Row_H = 16
        Num_Rows = H // Row_H + 1
        Num_Cols = max(1, W // self.Col_W)
        while len(self.Drops) < Num_Cols:
            self.Drops.append(random.randint(-40, 0))
        for C in range(min(Num_Cols, len(self.Drops))):
            Drop = self.Drops[C]
            for R in range(max(0, Drop - 12), min(Drop + 1, Num_Rows)):
                Char = random.choice(self.Chars)
                X    = C * self.Col_W + 4
                Y    = R * Row_H
                if R == Drop:
                    Color = Green_Bright
                    Font  = ("Cascadia Code", 9, "bold")
                elif R >= Drop - 2:
                    Color = Green_Mid
                    Font  = ("Cascadia Code", 8)
                elif R >= Drop - 6:
                    Color = Green_Dim
                    Font  = ("Cascadia Code", 8)
                else:
                    Color = Green_Ghost
                    Font  = ("Cascadia Code", 7)
                self.create_text(X, Y, text=Char, fill=Color,
                                 font=Font, anchor="nw")
            self.Drops[C] += 1
            if self.Drops[C] > Num_Rows + 15:
                self.Drops[C] = random.randint(-30, 0)
        self.after(70, self._Draw)

    def Stop(self):
        self.Running = False


class Hack_Progress(tk.Canvas):
    def __init__(self, Parent, Width=400, Height=14,
                 Value=0, Color=Green_Bright, **Kw):
        super().__init__(Parent, width=Width, height=Height,
                         bg=BG_Card, highlightthickness=0, bd=0, **Kw)
        self.W       = Width
        self.H       = Height
        self.Color   = Color
        self.Current = 0.0
        self.Target  = Value / 100
        self._Draw()
        self.after(30, self._Step)

    def _Draw(self):
        self.delete("all")
        Seg_W  = 6
        Gap    = 2
        Total  = self.W
        Fill_W = int(self.Current * Total)
        X = 0
        while X < Total:
            End_X = min(X + Seg_W, Total)
            if X < Fill_W:
                Bright = X < Fill_W - (Seg_W * 2)
                Clr    = self.Color if Bright else Green_Mid
                self.create_rectangle(X, 0, End_X, self.H,
                                      fill=Clr, outline="")
            else:
                self.create_rectangle(X, 0, End_X, self.H,
                                      fill=Green_Ghost, outline="")
            X += Seg_W + Gap
        self.create_rectangle(0, self.H - 1, Fill_W, self.H,
                              fill=Green_Bright, outline="")

    def _Step(self):
        if self.Current < self.Target:
            self.Current = min(self.Target, self.Current + 0.016)
            self._Draw()
            self.after(12, self._Step)
        else:
            self._Draw()


class Hack_Card(tk.Frame):
    def __init__(self, Parent, Title, **Kw):
        super().__init__(Parent, bg=BG_Card,
                         highlightbackground=Green_Faint,
                         highlightthickness=1, **Kw)
        Top = tk.Frame(self, bg=BG_Card2,
                       highlightbackground=Green_Faint,
                       highlightthickness=0)
        Top.pack(fill="x")
        Hdr = tk.Frame(Top, bg=BG_Card2, padx=16, pady=8)
        Hdr.pack(fill="x")
        tk.Label(Hdr, text="[ " + Title.upper() + " ]",
                 fg=Green_Bright, bg=BG_Card2,
                 font=Font_Mono_Med).pack(side="left")
        tk.Frame(self, bg=Green_Faint, height=1).pack(fill="x")
        self.Body = tk.Frame(self, bg=BG_Card, padx=18, pady=14)
        self.Body.pack(fill="both", expand=True)


class Big_Metric(tk.Frame):
    def __init__(self, Parent, Label, Value, Unit="",
                 Sub="", Color=Green_Bright, **Kw):
        super().__init__(Parent, bg=BG_Card2,
                         highlightbackground=Green_Faint,
                         highlightthickness=1,
                         padx=0, pady=0, **Kw)
        Top_Strip = tk.Frame(self, bg=Green_Faint, height=2)
        Top_Strip.pack(fill="x")
        Content = tk.Frame(self, bg=BG_Card2, padx=16, pady=14)
        Content.pack(fill="both", expand=True)
        tk.Label(Content, text=">_ " + Label.upper(),
                 fg=Text_Dim, bg=BG_Card2,
                 font=Font_Mono_Xxs).pack(anchor="w")
        Val_Row = tk.Frame(Content, bg=BG_Card2)
        Val_Row.pack(anchor="w", pady=(4, 0))
        tk.Label(Val_Row, text=str(Value), fg=Color,
                 bg=BG_Card2, font=Font_Mono_Num).pack(side="left")
        if Unit:
            tk.Label(Val_Row, text=f" {Unit}", fg=Green_Dim,
                     bg=BG_Card2, font=Font_Mono_Sm).pack(side="left",
                                                            anchor="s", pady=(0, 6))
        if Sub:
            tk.Label(Content, text=Sub, fg=Text_Ghost,
                     bg=BG_Card2, font=Font_Mono_Xxs).pack(anchor="w", pady=(4, 0))
        Bot_Strip = tk.Frame(self, bg=Color, height=2)
        Bot_Strip.pack(fill="x", side="bottom")


class Info_Line(tk.Frame):
    def __init__(self, Parent, Key, Val, Val_Color=Green_Mid, **Kw):
        super().__init__(Parent, bg=BG_Card, **Kw)
        tk.Label(self, text=f"  {Key:<22}",
                 fg=Text_Dim, bg=BG_Card,
                 font=Font_Mono_Xs).pack(side="left")
        tk.Label(self, text="::  ",
                 fg=Green_Faint, bg=BG_Card,
                 font=Font_Mono_Xs).pack(side="left")
        tk.Label(self, text=str(Val),
                 fg=Val_Color, bg=BG_Card,
                 font=Font_Mono_Xs).pack(side="left")


class Bar_Stat(tk.Frame):
    def __init__(self, Parent, Label, Used, Total_V,
                 Pct, Color=Green_Bright, **Kw):
        super().__init__(Parent, bg=BG_Card, **Kw)

        Header = tk.Frame(self, bg=BG_Card)
        Header.pack(fill="x", pady=(0, 6))
        tk.Label(Header, text=f"  >_ {Label.upper()}",
                 fg=Text_Dim, bg=BG_Card,
                 font=Font_Mono_Xs).pack(side="left")
        tk.Label(Header, text=f"  {Used}  /  {Total_V}",
                 fg=Green_Dim, bg=BG_Card,
                 font=Font_Mono_Xs).pack(side="left")
        Pct_Label = tk.Label(Header, text=f"  [{Pct}%]",
                              fg=Color, bg=BG_Card,
                              font=Font_Mono_Xs)
        Pct_Label.pack(side="right", padx=(0, 4))

        Bar_Frame = tk.Frame(self, bg=BG_Card, padx=4)
        Bar_Frame.pack(fill="x")
        Hack_Progress(Bar_Frame, Width=0, Height=12,
                      Value=Pct, Color=Color).pack(fill="x")


class Main_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FERROFY_EARN :: SYSTEM_SCAN v1.0")
        self.configure(bg=BG_Black)

        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda E: self.destroy())
        self.bind("<F11>", self._Toggle_Fullscreen)
        self._Is_Fullscreen = True

        self.Info = Get_System_Info()
        self._Build_UI()
        self._Pulse()
        self._Tick_Clock()

    def _Toggle_Fullscreen(self, Event=None):
        self._Is_Fullscreen = not self._Is_Fullscreen
        self.attributes("-fullscreen", self._Is_Fullscreen)

    def _Build_UI(self):
        self.Rain_Canvas = Matrix_Rain(self, bg=BG_Black)
        self.Rain_Canvas.place(x=0, y=0, relwidth=1, relheight=1)

        Main = tk.Frame(self, bg=BG_Panel,
                        highlightbackground=Green_Faint,
                        highlightthickness=1)
        Main.place(relx=0.5, rely=0.5, anchor="center",
                   relwidth=0.92, relheight=0.92)

        self._Build_Titlebar(Main)
        self._Build_Body(Main)
        self._Build_Statusbar(Main)

    def _Build_Titlebar(self, P):
        Bar = tk.Frame(P, bg=BG_Card2,
                       highlightbackground=Green_Faint,
                       highlightthickness=0,
                       padx=20, pady=10)
        Bar.pack(fill="x")
        tk.Frame(Bar, bg=Green_Bright, width=4, height=28).pack(side="left", padx=(0, 14))
        Left = tk.Frame(Bar, bg=BG_Card2)
        Left.pack(side="left")
        tk.Label(Left,
                 text="FERROFY_EARN :: SYSTEM_DIAGNOSTICS_PANEL",
                 fg=Green_Bright, bg=BG_Card2,
                 font=Font_Mono_Big).pack(anchor="w")
        tk.Label(Left,
                 text=f"USER :: {self.Info['username'].upper()}  |  HOST :: {self.Info['hostname'].upper()}  |  OS :: {self.Info['os_name'].upper()}",
                 fg=Green_Dim, bg=BG_Card2,
                 font=Font_Mono_Xxs).pack(anchor="w", pady=(3, 0))
        Right = tk.Frame(Bar, bg=BG_Card2)
        Right.pack(side="right")
        self.Clock_Label = tk.Label(Right, text="", fg=Green_Mid,
                                     bg=BG_Card2, font=Font_Mono_Sm)
        self.Clock_Label.pack(anchor="e")
        self.Pulse_Label = tk.Label(Right, text="● SCANNING",
                                    fg=Green_Bright, bg=BG_Card2,
                                    font=Font_Mono_Xs)
        self.Pulse_Label.pack(anchor="e", pady=(4, 0))
        Hint = tk.Label(Right, text="[ESC] EXIT   [F11] WINDOWED",
                        fg=Text_Ghost, bg=BG_Card2,
                        font=Font_Mono_Xxs)
        Hint.pack(anchor="e", pady=(4, 0))
        tk.Frame(P, bg=Green_Mid, height=2).pack(fill="x")

    def _Build_Body(self, P):
        Body = tk.Frame(P, bg=BG_Panel)
        Body.pack(fill="both", expand=True, padx=16, pady=12)

        Left_Col = tk.Frame(Body, bg=BG_Panel)
        Left_Col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        Right_Col = tk.Frame(Body, bg=BG_Panel)
        Right_Col.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self._Build_Stats_Row(Left_Col)
        self._Build_CPU_Card(Left_Col)
        self._Build_Memory_Card(Left_Col)

        self._Build_Mining_Card(Right_Col)
        self._Build_OS_Card(Right_Col)

    def _Build_Stats_Row(self, P):
        Row = tk.Frame(P, bg=BG_Panel)
        Row.pack(fill="x", pady=(0, 10))
        Items = [
            ("CPU Threads",       self.Info["cpu_threads"],  "TOTAL",   Green_Bright),
            ("Used For Mining",   self.Info["mine_threads"], "THREADS", Cyan),
            ("% Using For Mining",f"{self.Info['thread_pct']}%", "CPU",  Amber),
            ("RAM Free",          self.Info["ram_free"],     "GB",      Green_Mid),
        ]
        for I, (Lbl, Val, Unit, Clr) in enumerate(Items):
            Box = Big_Metric(Row, Lbl, Val, Unit, Color=Clr)
            Box.grid(row=0, column=I,
                     padx=(0, 8) if I < len(Items) - 1 else 0,
                     sticky="nsew")
            Row.columnconfigure(I, weight=1)

    def _Build_CPU_Card(self, P):
        Card = Hack_Card(P, "Processor_Unit")
        Card.pack(fill="x", pady=(0, 10))
        B = Card.Body
        tk.Label(B, text=self.Info["cpu_name"].upper(),
                 fg=Green_Bright, bg=BG_Card,
                 font=Font_Mono_Sm).pack(anchor="w", pady=(0, 10))
        Grid = tk.Frame(B, bg=BG_Card)
        Grid.pack(fill="x", pady=(0, 10))
        CPU_Details = [
            ("Physical Cores",    self.Info["cpu_cores"],    Green_Mid),
            ("Logical Threads",   self.Info["cpu_threads"],  Green_Mid),
            ("Architecture",      self.Info["arch"],         Green_Dim),
            ("Max Frequency",     f"{self.Info['cpu_freq_max']} GHZ", Cyan),
            ("Current Frequency", f"{self.Info['cpu_freq_cur']} GHZ", Cyan),
            ("CPU Load",          f"{self.Info['cpu_pct']}%", Amber),
        ]
        for I, (K, V, C) in enumerate(CPU_Details):
            R, Col = divmod(I, 2)
            Cell = tk.Frame(Grid, bg=BG_Card)
            Cell.grid(row=R, column=Col, sticky="w", padx=(0, 30), pady=2)
            Grid.columnconfigure(Col, weight=1)
            tk.Label(Cell, text=f">_ {K:<22}", fg=Text_Dim,
                     bg=BG_Card, font=Font_Mono_Xs).pack(side="left")
            tk.Label(Cell, text=f"::  {V}", fg=C,
                     bg=BG_Card, font=Font_Mono_Xs).pack(side="left")
        tk.Frame(B, bg=Green_Faint, height=1).pack(fill="x", pady=(4, 8))
        Bar_Stat(B, "CPU Load",
                 f"{self.Info['cpu_pct']}%", "100%",
                 int(self.Info["cpu_pct"]),
                 Color=Amber).pack(fill="x")

    def _Build_Memory_Card(self, P):
        Card = Hack_Card(P, "Memory_Storage")
        Card.pack(fill="x", pady=(0, 10))
        B = Card.Body
        Bar_Stat(B, "RAM",
                 f"{self.Info['ram_used']} GB",
                 f"{self.Info['ram_total']} GB",
                 int(self.Info["ram_pct"]),
                 Color=Green_Bright).pack(fill="x")
        tk.Frame(B, bg=Green_Faint, height=1).pack(fill="x", pady=10)
        Bar_Stat(B, "DISK  [C:\\]",
                 f"{self.Info['disk_used']} GB",
                 f"{self.Info['disk_total']} GB",
                 int(self.Info["disk_pct"]),
                 Color=Cyan).pack(fill="x")

    def _Build_Mining_Card(self, P):
        Card = Hack_Card(P, "Mining_Config")
        Card.pack(fill="x", pady=(0, 10))
        B = Card.Body

        Rows = [
            ("Total CPU Threads",    self.Info["cpu_threads"],  Green_Bright),
            ("Used For Mining",      self.Info["mine_threads"], Cyan),
            ("% Using For Mining",   f"{self.Info['thread_pct']}%", Amber),
            ("Remaining Threads",    self.Info["cpu_threads"] - self.Info["mine_threads"], Green_Dim),
        ]
        for K, V, C in Rows:
            Row_Frame = tk.Frame(B, bg=BG_Card2,
                                 highlightbackground=Green_Faint,
                                 highlightthickness=1,
                                 padx=14, pady=10)
            Row_Frame.pack(fill="x", pady=4)
            tk.Label(Row_Frame, text=f">_ {K.upper()}",
                     fg=Text_Dim, bg=BG_Card2,
                     font=Font_Mono_Xxs).pack(anchor="w")
            tk.Label(Row_Frame, text=str(V),
                     fg=C, bg=BG_Card2,
                     font=("Cascadia Code", 22, "bold")).pack(anchor="w", pady=(2, 0))

        tk.Frame(B, bg=Green_Faint, height=1).pack(fill="x", pady=8)
        tk.Label(B, text=">_ THREAD_ALLOCATION_BAR",
                 fg=Text_Dim, bg=BG_Card,
                 font=Font_Mono_Xxs).pack(anchor="w", pady=(0, 6))
        Hack_Progress(B, Width=0, Height=14,
                      Value=Thread_Percent, Color=Cyan).pack(fill="x")
        tk.Label(B,
                 text=f"  [ {Mine_Threads} OF {Total_Threads} THREADS ALLOCATED TO MINER ]",
                 fg=Cyan, bg=BG_Card,
                 font=Font_Mono_Xxs).pack(anchor="w", pady=(6, 0))

    def _Build_OS_Card(self, P):
        Card = Hack_Card(P, "System_Identity")
        Card.pack(fill="x", pady=(0, 10))
        B = Card.Body

        OS_Details = [
            ("Operating System",  self.Info["os_name"],    Green_Bright),
            ("OS Build",          self.Info["os_build"],   Green_Dim),
            ("Architecture",      self.Info["arch"],       Green_Mid),
            ("Hostname",          self.Info["hostname"],   Cyan),
            ("Username",          self.Info["username"],   Cyan),
            ("Python Version",    self.Info["python_ver"], Amber),
        ]
        for K, V, C in OS_Details:
            Row_Frame = tk.Frame(B, bg=BG_Card)
            Row_Frame.pack(fill="x", pady=3)
            tk.Label(Row_Frame, text=f">_ {K:<22}", fg=Text_Dim,
                     bg=BG_Card, font=Font_Mono_Xs).pack(side="left")
            tk.Label(Row_Frame, text=f"::  {V}", fg=C,
                     bg=BG_Card, font=Font_Mono_Xs).pack(side="left")
            tk.Frame(B, bg=Green_Ghost, height=1).pack(fill="x", pady=1)

    def _Build_Statusbar(self, P):
        tk.Frame(P, bg=Green_Mid, height=1).pack(fill="x")
        Bar = tk.Frame(P, bg=BG_Card2, padx=20, pady=7)
        Bar.pack(fill="x")
        tk.Label(Bar,
                 text=f"  FERROFY_EARN :: SYSTEM_SCAN v1.0  |  PYTHON {self.Info['python_ver']}  |  {self.Info['os_name'].upper()}",
                 fg=Text_Ghost, bg=BG_Card2,
                 font=Font_Mono_Xxs).pack(side="left")
        Btn = tk.Label(Bar, text="  [ CLOSE ]  ", fg=BG_Black,
                       bg=Green_Bright, font=Font_Mono_Xs,
                       padx=8, pady=4, cursor="hand2")
        Btn.pack(side="right")
        Btn.bind("<Button-1>", lambda E: self.destroy())
        Btn.bind("<Enter>",    lambda E: Btn.configure(bg=Cyan, fg=BG_Black))
        Btn.bind("<Leave>",    lambda E: Btn.configure(bg=Green_Bright, fg=BG_Black))

    def _Pulse(self):
        C = self.Pulse_Label.cget("fg")
        N = Green_Bright if C == BG_Card2 else BG_Card2
        self.Pulse_Label.configure(fg=N)
        self.after(700, self._Pulse)

    def _Tick_Clock(self):
        Now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self.Clock_Label.configure(text=f"SYS_TIME :: {Now}")
        self.after(1000, self._Tick_Clock)


if __name__ == "__main__":
    App = Main_App()
    App.mainloop()
