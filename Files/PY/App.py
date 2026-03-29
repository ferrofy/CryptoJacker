import tkinter as tk
from datetime import datetime

from Files.PY.Colors import (
    BG_Black, BG_Panel, BG_Card, BG_Card2,
    Border_Color, Ghost_Color, Text_Muted, Text_Subdued,
    Neon_Green, Neon_Cyan, Neon_Pink, Neon_Purple,
    Neon_Orange, Neon_Yellow, Neon_Red, Neon_Blue,
    Neon_Lime, Neon_Magenta,
    Font_Big, Font_Xs, Font_Xxs, Font_Sm
)
from Files.PY.System_Info import (
    Get_System_Info, Mine_Threads, Total_Threads, Thread_Percent
)
from Files.PY.Widgets import (
    Chaos_Rain, Glow_Bar, Glow_Card, Big_Metric, Bar_Stat
)


class Main_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FERROFY_EARN :: SYSTEM_SCAN v2.0")
        self.configure(bg=BG_Black)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda E: self.destroy())
        self.bind("<F11>",    self._Toggle_Fullscreen)
        self._Is_Fullscreen = True
        self.Info           = Get_System_Info()
        self._Color_Idx     = 0
        self._Build_UI()
        self._Pulse()
        self._Tick_Clock()
        self._Cycle_Accent()

    def _Toggle_Fullscreen(self, Event=None):
        self._Is_Fullscreen = not self._Is_Fullscreen
        self.attributes("-fullscreen", self._Is_Fullscreen)

    def _Build_UI(self):
        self.Rain_Canvas = Chaos_Rain(self, bg=BG_Black)
        self.Rain_Canvas.place(x=0, y=0, relwidth=1, relheight=1)
        Main = tk.Frame(self, bg=BG_Panel,
                        highlightbackground=Border_Color,
                        highlightthickness=1)
        Main.place(relx=0.5, rely=0.5, anchor="center",
                   relwidth=0.93, relheight=0.93)
        self._Build_Titlebar(Main)
        self._Build_Body(Main)
        self._Build_Statusbar(Main)

    def _Build_Titlebar(self, P):
        Bar = tk.Frame(P, bg=BG_Card2, padx=20, pady=10)
        Bar.pack(fill="x")

        self.Title_Accent = tk.Frame(Bar, bg=Neon_Cyan, width=4, height=30)
        self.Title_Accent.pack(side="left", padx=(0, 14))

        Left = tk.Frame(Bar, bg=BG_Card2)
        Left.pack(side="left")

        self.Title_Label = tk.Label(
            Left,
            text="FERROFY_EARN :: SYSTEM_DIAGNOSTICS_PANEL",
            fg=Neon_Cyan, bg=BG_Card2,
            font=Font_Big
        )
        self.Title_Label.pack(anchor="w")

        Info_Str = (
            f"USER :: {self.Info['username'].upper()}"
            f"  |  HOST :: {self.Info['hostname'].upper()}"
            f"  |  OS :: {self.Info['os_name'].upper()}"
        )
        tk.Label(Left, text=Info_Str,
                 fg=Text_Subdued, bg=BG_Card2,
                 font=Font_Xxs).pack(anchor="w", pady=(3, 0))

        Right = tk.Frame(Bar, bg=BG_Card2)
        Right.pack(side="right")

        self.Clock_Label = tk.Label(Right, text="",
                                    fg=Neon_Yellow, bg=BG_Card2,
                                    font=Font_Sm)
        self.Clock_Label.pack(anchor="e")

        self.Pulse_Label = tk.Label(Right, text="● SCANNING",
                                    fg=Neon_Green, bg=BG_Card2,
                                    font=Font_Xs)
        self.Pulse_Label.pack(anchor="e", pady=(4, 0))

        tk.Label(Right, text="[ESC] EXIT   [F11] WINDOWED",
                 fg=Text_Muted, bg=BG_Card2,
                 font=Font_Xxs).pack(anchor="e", pady=(4, 0))

        self.Topbar_Line = tk.Frame(P, bg=Neon_Cyan, height=2)
        self.Topbar_Line.pack(fill="x")

    def _Build_Body(self, P):
        Body = tk.Frame(P, bg=BG_Panel)
        Body.pack(fill="both", expand=True, padx=14, pady=10)

        Left_Col = tk.Frame(Body, bg=BG_Panel)
        Left_Col.pack(side="left", fill="both", expand=True, padx=(0, 8))

        Right_Col = tk.Frame(Body, bg=BG_Panel)
        Right_Col.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self._Build_Stats_Row(Left_Col)
        self._Build_CPU_Card(Left_Col)
        self._Build_Memory_Card(Left_Col)
        self._Build_Mining_Card(Right_Col)
        self._Build_OS_Card(Right_Col)

    def _Build_Stats_Row(self, P):
        Row = tk.Frame(P, bg=BG_Panel)
        Row.pack(fill="x", pady=(0, 10))
        Items = [
            ("CPU Threads",  self.Info["cpu_threads"],          "TOTAL",   Neon_Cyan),
            ("Mine Threads", self.Info["mine_threads"],          "THREADS", Neon_Pink),
            ("Mine % CPU",   f"{self.Info['thread_pct']}%",     "CPU",     Neon_Orange),
            ("RAM Free",     self.Info["ram_free"],              "GB",      Neon_Lime),
        ]
        for I, (Lbl, Val, Unit, Clr) in enumerate(Items):
            Box = Big_Metric(Row, Lbl, Val, Unit, Color=Clr)
            Box.grid(row=0, column=I,
                     padx=(0, 7) if I < len(Items) - 1 else 0,
                     sticky="nsew")
            Row.columnconfigure(I, weight=1)

    def _Build_CPU_Card(self, P):
        Card = Glow_Card(P, "Processor_Unit", Accent=Neon_Green)
        Card.pack(fill="x", pady=(0, 10))
        B = Card.Body
        tk.Label(B, text=self.Info["cpu_name"].upper(),
                 fg=Neon_Green, bg=BG_Card,
                 font=Font_Sm).pack(anchor="w", pady=(0, 10))
        Grid = tk.Frame(B, bg=BG_Card)
        Grid.pack(fill="x", pady=(0, 10))
        CPU_Details = [
            ("Physical Cores", self.Info["cpu_cores"],               Neon_Lime),
            ("Logical Threads", self.Info["cpu_threads"],            Neon_Green),
            ("Architecture",    self.Info["arch"],                   Neon_Cyan),
            ("Max Frequency",   f"{self.Info['cpu_freq_max']} GHZ",  Neon_Blue),
            ("Current Freq",    f"{self.Info['cpu_freq_cur']} GHZ",  Neon_Cyan),
            ("CPU Load",        f"{self.Info['cpu_pct']}%",          Neon_Orange),
        ]
        for I, (K, V, C) in enumerate(CPU_Details):
            R, Col = divmod(I, 2)
            Cell = tk.Frame(Grid, bg=BG_Card)
            Cell.grid(row=R, column=Col, sticky="w", padx=(0, 28), pady=2)
            Grid.columnconfigure(Col, weight=1)
            tk.Label(Cell, text=f">_ {K:<22}", fg=Text_Subdued,
                     bg=BG_Card, font=Font_Xs).pack(side="left")
            tk.Label(Cell, text=f"::  {V}", fg=C,
                     bg=BG_Card, font=Font_Xs).pack(side="left")
        tk.Frame(B, bg=Border_Color, height=1).pack(fill="x", pady=(4, 8))
        Bar_Stat(B, "CPU Load",
                 f"{self.Info['cpu_pct']}%", "100%",
                 int(self.Info["cpu_pct"]),
                 Color=Neon_Orange).pack(fill="x")

    def _Build_Memory_Card(self, P):
        Card = Glow_Card(P, "Memory_Storage", Accent=Neon_Purple)
        Card.pack(fill="x", pady=(0, 10))
        B = Card.Body
        Bar_Stat(B, "RAM",
                 f"{self.Info['ram_used']} GB",
                 f"{self.Info['ram_total']} GB",
                 int(self.Info["ram_pct"]),
                 Color=Neon_Purple).pack(fill="x")
        tk.Frame(B, bg=Border_Color, height=1).pack(fill="x", pady=10)
        Bar_Stat(B, "Disk  [C:\\]",
                 f"{self.Info['disk_used']} GB",
                 f"{self.Info['disk_total']} GB",
                 int(self.Info["disk_pct"]),
                 Color=Neon_Blue).pack(fill="x")

    def _Build_Mining_Card(self, P):
        Card = Glow_Card(P, "Mining_Config", Accent=Neon_Pink)
        Card.pack(fill="x", pady=(0, 10))
        B = Card.Body
        Mine_Colors = [Neon_Cyan, Neon_Pink, Neon_Orange, Neon_Yellow]
        Rows = [
            ("Total CPU Threads",  self.Info["cpu_threads"],                              Mine_Colors[0]),
            ("Used For Mining",    self.Info["mine_threads"],                             Mine_Colors[1]),
            ("% Using For Mining", f"{self.Info['thread_pct']}%",                        Mine_Colors[2]),
            ("Remaining Threads",  self.Info["cpu_threads"] - self.Info["mine_threads"],  Mine_Colors[3]),
        ]
        for K, V, C in Rows:
            Row_Frame = tk.Frame(B, bg=BG_Card2,
                                 highlightbackground=C,
                                 highlightthickness=1,
                                 padx=12, pady=9)
            Row_Frame.pack(fill="x", pady=3)
            tk.Label(Row_Frame, text=f">_ {K.upper()}",
                     fg=Text_Subdued, bg=BG_Card2,
                     font=Font_Xxs).pack(anchor="w")
            tk.Label(Row_Frame, text=str(V),
                     fg=C, bg=BG_Card2,
                     font=("Cascadia Code", 20, "bold")).pack(anchor="w", pady=(2, 0))
        tk.Frame(B, bg=Border_Color, height=1).pack(fill="x", pady=8)
        tk.Label(B, text=">_ THREAD_ALLOCATION_BAR",
                 fg=Text_Subdued, bg=BG_Card,
                 font=Font_Xxs).pack(anchor="w", pady=(0, 5))
        Glow_Bar(B, Width=0, Height=13,
                 Value=Thread_Percent, Color=Neon_Pink).pack(fill="x")
        tk.Label(B,
                 text=f"  [ {Mine_Threads} OF {Total_Threads} THREADS ALLOCATED TO MINER ]",
                 fg=Neon_Pink, bg=BG_Card,
                 font=Font_Xxs).pack(anchor="w", pady=(5, 0))

    def _Build_OS_Card(self, P):
        Card = Glow_Card(P, "System_Identity", Accent=Neon_Yellow)
        Card.pack(fill="x", pady=(0, 10))
        B = Card.Body
        Row_Colors = [Neon_Lime, Neon_Cyan, Neon_Green, Neon_Blue, Neon_Magenta, Neon_Orange]
        OS_Details = [
            ("Operating System", self.Info["os_name"]),
            ("OS Build",         self.Info["os_build"]),
            ("Architecture",     self.Info["arch"]),
            ("Hostname",         self.Info["hostname"]),
            ("Username",         self.Info["username"]),
            ("Python Version",   self.Info["python_ver"]),
        ]
        for I, (K, V) in enumerate(OS_Details):
            C = Row_Colors[I % len(Row_Colors)]
            Row_Frame = tk.Frame(B, bg=BG_Card)
            Row_Frame.pack(fill="x", pady=3)
            tk.Label(Row_Frame, text=f">_ {K:<22}", fg=Text_Subdued,
                     bg=BG_Card, font=Font_Xs).pack(side="left")
            tk.Label(Row_Frame, text=f"::  {V}", fg=C,
                     bg=BG_Card, font=Font_Xs).pack(side="left")
            tk.Frame(B, bg=Ghost_Color, height=1).pack(fill="x", pady=1)

    def _Build_Statusbar(self, P):
        tk.Frame(P, bg=Neon_Purple, height=1).pack(fill="x")
        Bar = tk.Frame(P, bg=BG_Card2, padx=20, pady=7)
        Bar.pack(fill="x")
        tk.Label(Bar,
                 text=f"  FERROFY_EARN :: SYSTEM_SCAN v2.0  |  PYTHON {self.Info['python_ver']}  |  {self.Info['os_name'].upper()}",
                 fg=Text_Subdued, bg=BG_Card2,
                 font=Font_Xxs).pack(side="left")
        Btn = tk.Label(Bar, text="  [ CLOSE ]  ",
                       fg=BG_Black, bg=Neon_Red,
                       font=Font_Xs, padx=8, pady=4,
                       cursor="hand2")
        Btn.pack(side="right")
        Btn.bind("<Button-1>", lambda E: self.destroy())
        Btn.bind("<Enter>",    lambda E: Btn.configure(bg=Neon_Pink, fg=BG_Black))
        Btn.bind("<Leave>",    lambda E: Btn.configure(bg=Neon_Red,  fg=BG_Black))

    def _Pulse(self):
        C      = self.Pulse_Label.cget("fg")
        Colors = [Neon_Green, Neon_Cyan, Neon_Pink, Neon_Purple, Neon_Orange]
        Idx    = Colors.index(C) if C in Colors else 0
        N      = Colors[(Idx + 1) % len(Colors)]
        self.Pulse_Label.configure(fg=N)
        self.after(500, self._Pulse)

    def _Tick_Clock(self):
        Now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        self.Clock_Label.configure(text=f"SYS_TIME :: {Now}")
        self.after(1000, self._Tick_Clock)

    def _Cycle_Accent(self):
        Cycle = [
            Neon_Cyan, Neon_Pink, Neon_Purple, Neon_Green,
            Neon_Orange, Neon_Yellow, Neon_Blue, Neon_Magenta, Neon_Lime
        ]
        C = Cycle[self._Color_Idx % len(Cycle)]
        self._Color_Idx += 1
        self.Title_Label.configure(fg=C)
        self.Topbar_Line.configure(bg=C)
        self.Title_Accent.configure(bg=C)
        self.after(1800, self._Cycle_Accent)
