"""Main page user interface
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

Interface that shows the tool's main functionalities.
"""
import tkinter as tk
from tkinter import ttk
from pubsub import pub
from View.V_Page import Page
import cv2
from PIL import ImageTk

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)


class MainPage(Page):
    """
    A class used to shows the tool's main functionalities.
    ...
    Attributes
    ----------
    container : tkinter Tk
        root window
    lang : LanguageFile
        file with the variables translated
    Methods
    -------
    elements_page()
        Creates the frame and main labels of page_0's UI (Main Menu).
    apretar_boto_1()
        Shows page_1 UI (Process images).
    apretar_boto_2()
        Shows page_2 UI (View images).
    resize_img(img, scale_percent)
        Resizes the img according to the scale_percent.
    """
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
        p0_button_1 = ttk.Button(self.page, text=self.lang.BUTTON_1, command=self.apretar_boto_1, width=30)
        p0_button_2 = ttk.Button(self.page, text=self.lang.BUTTON_2, command=self.apretar_boto_2, width=30)
        p0_frame = tk.Frame(self.page)

        img_salle = cv2.imread("resources/Images/logoLA_SALLE.PNG", cv2.IMREAD_COLOR)
        img_salle = self.resize_img(img_salle, 10)
        b, g, r = cv2.split(img_salle)
        img = cv2.merge((r, g, b))
        im_p1 = ImageTk.Image.fromarray(img)
        imgtk_p1 = ImageTk.PhotoImage(im_p1)
        p0_img_salle = ttk.Label(p0_frame)
        p0_img_salle.configure(image=imgtk_p1)
        p0_img_salle.image = imgtk_p1

        img_acm = cv2.imread("resources/Images/logoACM.png", cv2.IMREAD_COLOR)
        img_acm = self.resize_img(img_acm, 24)
        b, g, r = cv2.split(img_acm)
        img = cv2.merge((r, g, b))
        im_p1 = ImageTk.Image.fromarray(img)
        imgtk_p1 = ImageTk.PhotoImage(im_p1)
        p0_img_acm = ttk.Label(p0_frame)
        p0_img_acm.configure(image=imgtk_p1)
        p0_img_acm.image = imgtk_p1

        self.page.grid(row=0, column=0, sticky="NESW")
        p0_label_0.pack(pady=20)
        p0_button_1.pack(ipadx=0, pady=5)
        p0_button_2.pack(ipadx=0, pady=5)
        p0_frame.pack(pady=50) #v1: pady=20
        p0_img_salle.pack(pady=5)
        p0_img_acm.pack(pady=5)

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

    def resize_img(self, img, scale_percent):
        """
        Resizes the img according to the scale_percent.
        Parameters
        ----------
        img : image cv2
           img selected by the user.
        scale_percent : int
            resize factor
        """
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        print("Dimensió: ", dim)
        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img = resized
        return img
