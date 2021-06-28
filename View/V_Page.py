"""Abstract class for the tool pages
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

Basic user interface with the window and a frame.
"""
from abc import ABC, abstractmethod
import tkinter as tk

class Page(ABC):
    """
    Basic user interface with the window and a frame.
    ...
    Attributes
    ----------
    container : tkinter Tk
        root window
    page : tkinter Frame
        frame where visual elements will be placed
    Methods
    -------
    elements_page()
        Basic function to place elements on the parent's frame.
    """
    def __init__(self):
        self.container: tk.Tk = NotImplemented
        self.page: tk.Frame = NotImplemented
        return

    @abstractmethod
    def elements_page(self):
        """
        Basic function to place elements on the parent's frame.
        """
        pass