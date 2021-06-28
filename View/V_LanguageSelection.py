"""Language selection viewer
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

Interface that allows user's language selection.
"""
import sys
import tkinter as tk
from tkinter import ttk
from pubsub import pub

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)

class ViewLanguageSelection():
    """
    A class used to render the program language selection's interface.
    ...
    Attributes
    ----------
    parent : tkinter Tk
        root window
    Methods
    -------
    ask_lang()
        Configures and renders the interface of language selection
        with the available language options.
    lang_selected(lang)
        Calls the function to load the variables with the user's language selection.
    lang_changed()
        Receives a JSON object with the image data and metadata of a new patient
        and writes it to a txt file.
    """
    def __init__(self, parent):
        self.parent = parent
        return
    def ask_lang(self):
        """
        Configures and renders the interface of language selection
        with the available language options.
        """
        popup = self.parent
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        w = 300
        h = 100
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        popup.wm_title("Language")
        frame_label = tk.Frame(popup)
        frame_label.pack(pady= 20)
        label = ttk.Label(frame_label, text="Select language:", font=FONT_MSG)
        label.configure(anchor="center")
        label.pack(side="left", padx=10)

        lang_combobox = ttk.Combobox(frame_label, state="readonly", width=10, justify="left")
        lang_combobox["values"] = ["Català", "Castellano", "English"]
        lang_combobox.current(0)
        lang_combobox.pack(side="left", padx=0)
        button1 = ttk.Button(popup, text="Ok", command=lambda: self.lang_selected(lang_combobox.current()))
        button1.pack(pady=0)
        popup.mainloop()

    def lang_selected(self, lang):
        """
        Calls the function to load the variables with the user's language selection.
        Parameters
        ----------
        lang : String
            user's language selection id
        """
        pub.sendMessage("LANG_SELECTED", lang=lang)

    def lang_changed(self):
        """
        Tells the user that program needs to be restarted when
        language is changed on execution time.
        """
        popup = tk.Toplevel()
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        w = 300
        h = 75
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        popup.wm_title("Atenció")
        label = ttk.Label(popup, text="Change language? Program reset required.", font=FONT_MSG)
        label.configure(anchor="center")
        label.pack(side="top", fill="x", pady=10)
        button1 = ttk.Button(popup, text="Accept", command=sys.exit)
        button1.pack()
        popup.mainloop()