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
        self.code_option = None
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
        h = 700
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
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
        button1 = ttk.Button(self.popup, text=self.lang.YES,
                             command=lambda: self.segmentacio_ok(img_imgtk_mask, img_cv2_mask))
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

    def popup_new_code(self):

        popup = tk.Toplevel()
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        w = 310
        h = 150
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        popup.wm_title(self.lang.PRE_NEW_CODE_TITLE)
        label1 = tk.Label(popup, text=self.lang.PRE_NEW_CODE_DESC_1, font=FONT_MSG)
        label1.pack(side="top", fill="both", pady=5)
        label = ttk.Label(popup, text=self.lang.PRE_LABEL_OLD)
        entry_new_ulcer = tk.Entry(popup, width=28, font=FONT_MSG)
        entry_new_ulcer.insert(tk.END, '')
        label.pack(padx=10)
        entry_new_ulcer.pack(pady=10)
        button1 = ttk.Button(popup, text=self.lang.CONTINUE,
                             command=lambda: self.new_code(popup, entry_new_ulcer.get()))
        button1.pack(pady=10)
        popup.resizable(False, False)
        popup.mainloop()

    def new_code(self, popup, location):
        if location != "":
            popup.destroy()
            pub.sendMessage("NEW_CODE_LOCATION", location=location, new_patient=True)
        else:
            pub.sendMessage("POPUP_MSG", msg=self.lang.PRE_NEW_LOCATION_EMPTY)

    def popup_ask_code(self):

        popup = tk.Toplevel()
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        w = 310
        h = 150
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        popup.wm_title(self.lang.PRE_ASK_CODE_TITLE)
        label1 = tk.Label(popup, text=self.lang.PRE_ASK_CODE_DESC_1, font=FONT_MSG)
        label1.configure(anchor="center")
        label1.pack(side="top", fill="both", pady=5)
        entry_new_ulcer = tk.Entry(popup, width=28, font=FONT_MSG)
        entry_new_ulcer.insert(tk.END, "")
        combobox_old_ulcer = ttk.Combobox(popup, state="readonly", width=25, justify="left", font=FONT_MSG)
        combobox_old_ulcer["values"] = [self.lang.META_DAYS, self.lang.META_WEEKS, self.lang.META_MONTHS]
        combobox_old_ulcer.current(0)
        code_radiobutton_old = ttk.Radiobutton(popup, variable="code", text=self.lang.PRE_RADIOBUTTON_OLD,
                                               value="old", command=lambda: self.old_ulcer_view(label, entry_new_ulcer,
                                                                                                combobox_old_ulcer))
        code_radiobutton_new = ttk.Radiobutton(popup, variable="code", text=self.lang.PRE_RADIOBUTTON_NEW,
                                               value="new", command=lambda: self.new_ulcer_view(label, entry_new_ulcer,
                                                                                                combobox_old_ulcer))
        label = ttk.Label(popup, text=self.lang.PRE_LABEL_NEW)
        code_radiobutton_old.pack()
        code_radiobutton_new.pack()

        button1 = ttk.Button(popup, text=self.lang.CONTINUE,
                             command=lambda: self.check_option(popup, entry_new_ulcer.get(), combobox_old_ulcer.get()))
        button1.pack(pady=10, side="bottom")
        popup.resizable(False, False)
        popup.mainloop()

    def check_option(self, popup, new_ulcer, old_ulcer):
        if self.code_option is not None:
            if self.code_option == 0:
                if new_ulcer != "":
                    # FALTA: COMPROVAR SI LOCALITZACIÓ EXISTEIX (potser a model)
                    # FALTA: COMPROVAR SI EL CODI S'HA CANVIAT (a l'apretar Guardar)
                    pub.sendMessage("NEW_CODE_LOCATION", location=new_ulcer, new_patient=False)
                    popup.destroy()
                else:
                    pub.sendMessage("POPUP_MSG", msg=self.lang.PRE_NEW_LOCATION_EMPTY)
            else:
                popup.destroy()
                pub.sendMessage("OLD_CODE_LOCATION", location=old_ulcer)
        else:
            pub.sendMessage("POPUP_MSG", msg=self.lang.PRE_CODE_RADIOBUTTONS)

    def new_ulcer_view(self, label, entry_new_ulcer, combobox_old_ulcer):
        combobox_old_ulcer.pack_forget()
        label.pack(side=tk.LEFT, padx=10)
        entry_new_ulcer.pack(pady=10)
        self.code_option = 0

    def old_ulcer_view(self, label, entry_new_ulcer, combobox_old_ulcer):
        label.pack(side=tk.LEFT, padx=10)
        entry_new_ulcer.pack_forget()
        combobox_old_ulcer.pack(pady=5)
        self.code_option = 1
