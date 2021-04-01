import abc
from abc import ABC, abstractmethod
import tkinter as tk

class Page(ABC):

    def __init__(self):
        self.container: tk.Tk = NotImplemented
        self.page: tk.Frame = NotImplemented
        return

    @abstractmethod
    def elements_page(self):
        pass