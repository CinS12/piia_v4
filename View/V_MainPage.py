import tkinter as tk
from tkinter import ttk
from pubsub import pub
from View.V_Page import Page
FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)


class MainPage(Page):
    def __init__(self, parent, lang):
        self.container = parent
        self.lang = lang
        self.elements_page()
        return

    def elements_page(self):
        """
        Creates the frame and main labels of page_0's UI (Main Menu).
        """

        self.page = tk.Frame(self.container)
        p0_label_0 = ttk.Label(self.page, text=self.lang.MAIN_TITLE, font=FONT_BENVINGUDA)
        p0_button_1 = ttk.Button(self.page, text=self.lang.BUTTON_1, command=self.apretar_boto_1)
        p0_button_2 = ttk.Button(self.page, text=self.lang.BUTTON_2, command=self.apretar_boto_2)

        self.page.grid(row=0, column=0, sticky="NESW")
        p0_label_0.pack(pady=20)
        p0_button_1.pack()
        p0_button_2.pack()

    def apretar_boto_1(self):
        """
        Shows page_1 UI (Process images).
        """

        pub.sendMessage("GO_TO_PROCESSING_PAGE")

    def apretar_boto_2(self):
        """
        Shows page_2 UI (View images).
        """
        pub.sendMessage("BUTTON_2_PRESSED")
        pub.sendMessage("GO_TO_VIEW_PAGE")