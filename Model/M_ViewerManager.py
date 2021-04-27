import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)

class ViewerManager:

    def __init__(self, evo_data, lang):
        self.evo_data = evo_data
        self.lang = lang
        self.setup_evolution(evo_data)
        return

    def setup_evolution(self, evo_data):
        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 900
        h = 700
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title(self.lang.VM_title)
        label_id = ttk.Label(self.popup, text=self.lang.VM_id + str(evo_data["id"]), font=FONT_TITOL)
        label_id.pack(pady=0)
        label_location = ttk.Label(self.popup, text=self.lang.VM_location + str(evo_data["location"]), font=FONT_TITOL)
        label_location.pack(pady=0)
        width = 0.3
        f = Figure(figsize=(7, 3), dpi=100)

        ax = f.add_subplot(121)
        ax.set_ylabel(self.lang.VM_cm)
        ax.set_title(self.lang.VM_perimeter_title)
        #ax.xticks(rotation=90)
        ax.bar(evo_data["date"], evo_data["perimeter"], width)

        ax1 = f.add_subplot(122)
        ax1.set_ylabel(self.lang.VM_cm + " * " + self.lang.VM_cm)
        ax1.set_title(self.lang.VM_perimeter_area)
        ax1.bar(evo_data["date"], evo_data["area_total"], width)

        f.autofmt_xdate()
        f.tight_layout(pad=1, w_pad=0, h_pad=0)

        canvas = FigureCanvasTkAgg(f, master=self.popup)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        f1 = Figure(figsize=(7, 3), dpi=100)

        ax2 = f1.add_subplot(131)
        ax2.set_ylabel(self.lang.VM_cm + " * " + self.lang.VM_cm)
        ax2.set_title(self.lang.VM_granulation)
        ax2.bar(evo_data["date"], evo_data["granulation"], width, color="orange")

        ax3 = f1.add_subplot(132)
        ax3.set_ylabel(self.lang.VM_cm + " * " + self.lang.VM_cm)
        ax3.set_title(self.lang.VM_slough)
        ax3.bar(evo_data["date"], evo_data["slough"], width, color="orange")

        ax4 = f1.add_subplot(133)
        ax4.set_ylabel(self.lang.VM_cm + " * " + self.lang.VM_cm)
        ax4.set_title(self.lang.VM_necrosis)
        ax4.bar(evo_data["date"], evo_data["necrosis"], width, color="orange")

        f1.autofmt_xdate()
        f1.tight_layout(pad=1, w_pad=0, h_pad=0)

        canvas1 = FigureCanvasTkAgg(f1, master=self.popup)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

