import cv2
from pubsub import pub
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)

class PreSegmentationGUI:

    def __init__(self, parent, lang):
        self.container = parent
        self.lang = lang
        return

    def ask_mask_confirmation(self, img_cv2_mask, scale_percent):
        """
        Displays a popup window to ask user confirmation about cropped mask.
        Parameters
        ----------
        img_cv2_mask : image cv2
           image that requires user confirmation
        scale_percent : int
           image resize value (default = 100)
        """

        cv2.destroyAllWindows()
        # Crear la finestra
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 1000
        h = 1100
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title(self.lang.PRE_CONFIRM_REGION)
        # Definir títol del popup
        title = ttk.Label(self.popup, text=self.lang.PRE_CORRECT_REGION, font=FONT_TITOL)
        title.configure(anchor="center")
        title.pack(side="top", fill="x", pady=10)
        # Carregar la roi
        im_rgb = cv2.cvtColor(img_cv2_mask, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im_rgb)
        # Escalar la imatge
        width = int(img_cv2_mask.shape[1] * scale_percent / 100)
        height = int(img_cv2_mask.shape[0] * scale_percent / 100)
        dim = (width, height)
        im = im.resize((width, height))
        # resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
        img_imgtk_mask = ImageTk.PhotoImage(image=im)
        self.confirmation_img = tk.Label(self.popup, image=img_imgtk_mask)
        self.confirmation_img.pack(pady=30)
        # Botons GUI
        button1 = ttk.Button(self.popup, text=self.lang.YES, command=lambda: self.segmentacio_ok(img_imgtk_mask, img_cv2_mask))
        button2 = ttk.Button(self.popup, text=self.lang.NO, command=self.segmentacio_ko)
        button1.pack()
        button2.pack()
        self.popup.mainloop()

    def segmentacio_ok(self, img_imgtk_mask, img_cv2_mask):
        """
        Closes the popup window and sends a request with the image(mask) and roi.
        Parameters
        ----------
        img_imgtk_mask : PIL Image
           image before cropping roi
        img_cv2_mask : image cv2
           image that requires user confirmation
        """

        self.popup.destroy()
        pub.sendMessage("PRE_SEGMENTATION_CONFIRMATED", img_imgtk_mask=img_imgtk_mask, img_cv2_mask=img_cv2_mask)

    def segmentacio_ko(self):
        """
        Closes the cv2 and popup window.
        """

        cv2.destroyAllWindows()
        self.popup.destroy()