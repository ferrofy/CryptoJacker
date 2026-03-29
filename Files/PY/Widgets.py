import random
import tkinter as tk
from Files.PY.Colors import (
    BG_Black, BG_Card, BG_Card2,
    Neon_Green, Neon_Cyan, Ghost_Color,
    Dim_Green, Text_Subdued, Text_Muted,
    PALETTE, Font_Med, Font_Sm, Font_Xs, Font_Xxs, Font_Num
)


class Chaos_Rain(tk.Canvas):
    Chars = "01アイウエオカキクケコ#@$%&!?<>{}[]ΩΨΦ∑∂∇λ"

    def __init__(self, Parent, **Kw):
        super().__init__(Parent, highlightthickness=0, bd=0, **Kw)
        self.Drops      = []
        self.Col_W      = 18
        self.Running    = True
        self.Col_Colors = []
        self.after(100, self._Init_Rain)

    def _Init_Rain(self):
        W = self.winfo_width()
        H = self.winfo_height()
        if W < 2 or H < 2:
            self.after(100, self._Init_Rain)
            return
        Num_Cols        = max(1, W // self.Col_W)
        self.Drops      = [random.randint(-50, 0) for _ in range(Num_Cols)]
        self.Col_Colors = [random.choice(PALETTE)  for _ in range(Num_Cols)]
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
        Row_H    = 18
        Num_Rows = H // Row_H + 1
        Num_Cols = max(1, W // self.Col_W)
        while len(self.Drops) < Num_Cols:
            self.Drops.append(random.randint(-50, 0))
            self.Col_Colors.append(random.choice(PALETTE))
        for C in range(min(Num_Cols, len(self.Drops))):
            Drop  = self.Drops[C]
            Color = self.Col_Colors[C]
            for R in range(max(0, Drop - 14), min(Drop + 1, Num_Rows)):
                Char = random.choice(self.Chars)
                X    = C * self.Col_W + 4
                Y    = R * Row_H
                Fade = Drop - R
                if Fade == 0:
                    Clr  = "#ffffff"
                    Font = ("Cascadia Code", 9, "bold")
                elif Fade <= 2:
                    Clr  = Color
                    Font = ("Cascadia Code", 9, "bold")
                elif Fade <= 6:
                    Clr  = Dim_Green
                    Font = ("Cascadia Code", 8)
                else:
                    Clr  = Ghost_Color
                    Font = ("Cascadia Code", 7)
                self.create_text(X, Y, text=Char, fill=Clr,
                                 font=Font, anchor="nw")
            self.Drops[C] += 1
            if self.Drops[C] > Num_Rows + 20:
                self.Drops[C]      = random.randint(-40, 0)
                self.Col_Colors[C] = random.choice(PALETTE)
        self.after(65, self._Draw)

    def Stop(self):
        self.Running = False


class Glow_Bar(tk.Canvas):
    def __init__(self, Parent, Width=400, Height=12,
                 Value=0, Color=Neon_Green, **Kw):
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
        Seg_W  = 5
        Gap    = 2
        Total  = self.W
        Fill_W = int(self.Current * Total)
        X = 0
        while X < Total:
            End_X = min(X + Seg_W, Total)
            if X < Fill_W:
                self.create_rectangle(X, 0, End_X, self.H,
                                      fill=self.Color, outline="")
            else:
                self.create_rectangle(X, 0, End_X, self.H,
                                      fill=Ghost_Color, outline="")
            X += Seg_W + Gap
        self.create_rectangle(0, self.H - 1, Fill_W, self.H,
                              fill="#ffffff", outline="")

    def _Step(self):
        if self.Current < self.Target:
            self.Current = min(self.Target, self.Current + 0.018)
            self._Draw()
            self.after(12, self._Step)
        else:
            self._Draw()


class Glow_Card(tk.Frame):
    def __init__(self, Parent, Title, Accent=Neon_Cyan, **Kw):
        super().__init__(Parent, bg=BG_Card,
                         highlightbackground=Accent,
                         highlightthickness=1, **Kw)
        self.Accent = Accent
        Top = tk.Frame(self, bg=BG_Card2)
        Top.pack(fill="x")
        Hdr = tk.Frame(Top, bg=BG_Card2, padx=14, pady=8)
        Hdr.pack(fill="x")
        tk.Label(Hdr, text="[ " + Title.upper() + " ]",
                 fg=Accent, bg=BG_Card2,
                 font=Font_Med).pack(side="left")
        tk.Frame(self, bg=Accent, height=1).pack(fill="x")
        self.Body = tk.Frame(self, bg=BG_Card, padx=16, pady=12)
        self.Body.pack(fill="both", expand=True)


class Big_Metric(tk.Frame):
    def __init__(self, Parent, Label, Value, Unit="",
                 Sub="", Color=Neon_Green, **Kw):
        super().__init__(Parent, bg=BG_Card2,
                         highlightbackground=Color,
                         highlightthickness=1,
                         padx=0, pady=0, **Kw)
        tk.Frame(self, bg=Color, height=2).pack(fill="x")
        Content = tk.Frame(self, bg=BG_Card2, padx=14, pady=12)
        Content.pack(fill="both", expand=True)
        tk.Label(Content, text=">_ " + Label.upper(),
                 fg=Text_Subdued, bg=BG_Card2,
                 font=Font_Xxs).pack(anchor="w")
        Val_Row = tk.Frame(Content, bg=BG_Card2)
        Val_Row.pack(anchor="w", pady=(4, 0))
        tk.Label(Val_Row, text=str(Value), fg=Color,
                 bg=BG_Card2, font=Font_Num).pack(side="left")
        if Unit:
            tk.Label(Val_Row, text=f" {Unit}", fg=Text_Subdued,
                     bg=BG_Card2, font=Font_Sm).pack(side="left",
                                                      anchor="s", pady=(0, 6))
        if Sub:
            tk.Label(Content, text=Sub, fg=Text_Muted,
                     bg=BG_Card2, font=Font_Xxs).pack(anchor="w", pady=(4, 0))
        tk.Frame(self, bg=Color, height=2).pack(fill="x", side="bottom")


class Info_Row(tk.Frame):
    def __init__(self, Parent, Key, Val,
                 Key_Color=None, Val_Color=Neon_Cyan, **Kw):
        if Key_Color is None:
            Key_Color = Text_Subdued
        super().__init__(Parent, bg=BG_Card, **Kw)
        tk.Label(self, text=f"  {Key:<22}",
                 fg=Key_Color, bg=BG_Card,
                 font=Font_Xs).pack(side="left")
        tk.Label(self, text="::  ",
                 fg=Text_Muted, bg=BG_Card,
                 font=Font_Xs).pack(side="left")
        tk.Label(self, text=str(Val),
                 fg=Val_Color, bg=BG_Card,
                 font=Font_Xs).pack(side="left")


class Bar_Stat(tk.Frame):
    def __init__(self, Parent, Label, Used, Total_V,
                 Pct, Color=Neon_Green, **Kw):
        super().__init__(Parent, bg=BG_Card, **Kw)
        Header = tk.Frame(self, bg=BG_Card)
        Header.pack(fill="x", pady=(0, 5))
        tk.Label(Header, text=f"  >_ {Label.upper()}",
                 fg=Text_Subdued, bg=BG_Card,
                 font=Font_Xs).pack(side="left")
        tk.Label(Header, text=f"  {Used}  /  {Total_V}",
                 fg=Color, bg=BG_Card,
                 font=Font_Xs).pack(side="left")
        tk.Label(Header, text=f"  [{Pct}%]",
                 fg="#ffffff", bg=BG_Card,
                 font=Font_Xs).pack(side="right", padx=(0, 4))
        Bar_Frame = tk.Frame(self, bg=BG_Card, padx=4)
        Bar_Frame.pack(fill="x")
        Glow_Bar(Bar_Frame, Width=0, Height=11,
                 Value=Pct, Color=Color).pack(fill="x")
