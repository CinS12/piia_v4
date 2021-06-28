"""Tool tip class
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

Interface that sets up tool tips to guide the user.
"""

import tkinter as tk

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)
class ToolTip(object):
    """
    Interface that sets up tool tips to guide the user.
    ...
    Attributes
    ----------
    container : tkinter Tk
        root window
    lang : LanguageFile
        file with the variables translated
    Methods
    -------
    showtip(text)
        Display text in tooltip window.
    hidetip()
        Method to make the tooltip no visible.
    CreateToolTip(text)
        Creates and configures the tooltip with the message and the event.
    """
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def showtip(self, text):
        """
        Display text in tooltip window.
        Parameters
        ----------
        text : String
           message to guide the user
        """
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=FONT_MSG)
        label.pack(ipadx=1)

    def hidetip(self):
        """
        Method to make the tooltip no visible.
        """
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def CreateToolTip(widget, text):
        """
        Creates and configures the tooltip with the message and the event.
        Parameters
        ----------
        text : String
           message to guide the user
        """
        toolTip = ToolTip(widget)
        def enter(event):
            toolTip.showtip(text)
        def leave(event):
            toolTip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)