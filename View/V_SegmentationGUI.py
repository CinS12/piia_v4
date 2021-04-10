import ctypes

import cv2
from pubsub import pub
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from View.V_ToolTip import ToolTip

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)


class SegmentationGUI:

    def __init__(self, parent, lang):
        self.lang = lang
        self.container = parent

        return

    def segmentation_gui(self, img_imgtk_mask, img_cv2_mask):
        """
        Creates a GUI for the image segmentation and processing.
        Parameters
        ----------
        img_imgtk_mask : PIL Image
           image before cropping roi
        img_cv2_mask : image cv2
           image that requires user confirmation
        """

        # Crear la finestra
        self.popup_img = tk.Toplevel()
        ws = self.popup_img.winfo_screenwidth()
        hs = self.popup_img.winfo_screenheight()
        w = 1100
        h = 600
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.popup_img.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup_img.wm_title(self.lang.SEG_TITLE)
        # Definir títol del popup
        title = ttk.Label(self.popup_img,
                          text=self.lang.SEG_DESC,
                          font=FONT_TITOL)
        title.configure(anchor="center")
        #Frame pels widgets
        self.widgets = tk.Frame(self.popup_img)
        self.widgets_img = tk.Frame(self.widgets)
        self.widgets_data = tk.Frame(self.widgets)
        # Frame per les dades
        balance_frame = ttk.Frame(self.widgets_data, borderwidth=2, relief="groove")
        data_frame = ttk.Frame(self.widgets_data)
        accept_frame = ttk.Frame(self.popup_img)
        # Botons GUI
        button_balance = ttk.Button(balance_frame, text=self.lang.SEG_WHITE,
                                    command=lambda: self.whitebalance(img_cv2_mask))
        button_perimeter = ttk.Button(data_frame, text=self.lang.SEG_PERIMETER, command=self.ask_perimeter)
        button_granulation = ttk.Button(data_frame, text=self.lang.SEG_GRANULATION, command=self.roi_granulation)
        button_necrosis = ttk.Button(data_frame, text=self.lang.SEG_NECROSIS, command=self.roi_necrosis)
        button_slough = ttk.Button(data_frame, text=self.lang.SEG_SLOUGH, command=self.roi_slough)
        button_accept = ttk.Button(accept_frame, text=self.lang.ACCEPT, command=self.img_processed_accepted)
        button_helper_granulation = tk.Button(data_frame, text="?", height=1, width=2,
                                              command=lambda: self.show_example(0))
        button_helper_necrosis = tk.Button(data_frame, text="?", height=1, width=2,
                                           command=lambda: self.show_example(1))
        button_helper_slough = tk.Button(data_frame, text="?", height=1, width=2, command=lambda: self.show_example(2))
        # Labels de la GUI
        self.label_balance = tk.Label(balance_frame, text=self.lang.SEG_WHITEBALANCE_DESC, fg="black",
                                      font=FONT_MSG)
        self.label_perimeter = tk.Label(data_frame, text=self.lang.SEG_PERIMETER_DESC, fg="black",
                                        font=FONT_MSG)
        self.label_granulation = ttk.Label(data_frame, text=(self.lang.SEG_SELECTED_ZONES + "0"), font=FONT_MSG)
        self.label_necrosis = ttk.Label(data_frame, text=(self.lang.SEG_SELECTED_ZONES + "0"), font=FONT_MSG)
        self.label_slough = ttk.Label(data_frame, text=(self.lang.SEG_SELECTED_ZONES + "0"), font=FONT_MSG)
        # Carregar la roi
        self.img_show = tk.Label(self.widgets_img, image=img_imgtk_mask)

        # Col·locar els elements
        button_balance.grid(row=1, column=1, padx=5, pady=5)
        self.label_balance.grid(row=1, column=2, padx=5, pady=5)
        button_perimeter.grid(row=2, column=1, padx=5, pady=5)
        self.label_perimeter.grid(row=2, column=2, padx=5, pady=5)
        button_granulation.grid(row=3, column=1, padx=5, pady=5)
        self.label_granulation.grid(row=3, column=2, padx=5, pady=5)
        button_necrosis.grid(row=4, column=1, padx=5, pady=5)
        self.label_necrosis.grid(row=4, column=2, padx=5, pady=5)
        button_slough.grid(row=5, column=1, padx=5, pady=5)
        self.label_slough.grid(row=5, column=2, padx=5, pady=5)
        button_accept.pack()

        button_helper_granulation.grid(row=3, column=0, padx=5, pady=5)
        button_helper_necrosis.grid(row=4, column=0, padx=5, pady=5)
        button_helper_slough.grid(row=5, column=0, padx=5, pady=5)

        title.pack(pady=10)
        self.widgets.pack(pady=10)
        self.widgets_img.pack(side=tk.LEFT)
        self.widgets_data.pack(side=tk.RIGHT, padx=10)
        balance_frame.pack(pady=5, padx=5)
        data_frame.pack(pady=5, padx=5)
        self.img_show.pack(pady=10)
        accept_frame.pack(pady=10, padx=0)

        # Add tool tips to tissue buttons
        ToolTip.CreateToolTip(button_helper_granulation, text=self.lang.HELPER_GRANULATION)
        ToolTip.CreateToolTip(button_helper_necrosis, text=self.lang.HELPER_NECROSIS)
        ToolTip.CreateToolTip(button_helper_slough, text=self.lang.HELPER_SLOUGH)

        self.popup_img.mainloop()

    def show_example(self, tissue):
        if tissue == 0:
            title = self.lang.SEG_GRANULATION_EX
            path = "../resources/ex_granulation.png"
            description = self.lang.HELPER_GRANULATION
        else:
            if tissue == 1:
                title = self.lang.SEG_NECROSIS_EX
                path = "../resources/ex_necrosis.png"
                description = self.lang.HELPER_NECROSIS
            else:
                if tissue == 2:
                    title = self.lang.SEG_SLOUGH_EX
                    path = "../resources/ex_slough.png"
                    description = self.lang.HELPER_SLOUGH
        # Crear la finestra
        popup = tk.Toplevel()
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        w = 650
        h = 500
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        popup.wm_title(title)
        title = ttk.Label(popup, text=title, font=FONT_TITOL)
        title.configure(anchor="center")
        title.pack(side="top", fill="x", pady=10)
        #label_description = ttk.Label(popup, text=description, font=FONT_MSG)
        text = tk.Text(popup, font=FONT_TITOL, relief=tk.GROOVE, width=65, height=2, wrap=tk.WORD)
        text.insert(tk.END, description, "desc")
        text.config(state=tk.DISABLED)
        text.tag_configure("desc", justify="center")
        #text.config(pady=10, padx=10)
        text.pack(pady=5)
        #label_description.pack(pady=5)
        # Carregar la imatge
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im_rgb)
        img_imgtk_mask = ImageTk.PhotoImage(image=im)
        self.confirmation_img = tk.Label(popup, image=img_imgtk_mask)
        self.confirmation_img.pack(pady=30)
        # Botons GUI
        button1 = ttk.Button(popup, text=self.lang.OK, command=popup.destroy)
        button1.pack()
        popup.mainloop()

    def whitebalance(self, img_cv2_mask):
        """
        Sends a request to the Controller for flash reduction.
        Parameters
        ----------
        img_cv2_mask : image cv2
           image selected by user to reduce its flash
        """

        pub.sendMessage("WHITEBALANCE", img_cv2_mask=img_cv2_mask)

    def ask_perimeter(self):
        """
        Sends a request to the Controller for perimeter's roi selection.
        """
        pub.sendMessage("ASK_PERIMETER")

    def roi_granulation(self):
        """
        Sends a request to the Controller for granulation's roi selection.
        """
        pub.sendMessage("ROI_GRANULATION")

    def roi_necrosis(self):
        """
        Sends a request to the Controller for necrosis's roi selection.
        """
        pub.sendMessage("ROI_NECROSIS")

    def roi_slough(self):
        """
        Sends a request to the Controller for slough's roi selection.
        """

        pub.sendMessage("ROI_SLOUGH")

    def img_processed_accepted(self):
        """
        Sends the request that image has been processed.
        """

        self.popup_img.destroy()
        pub.sendMessage("IMG_ACCEPTED")

    def ask_whitebalance_confirmation(self, img_cv2_mask, img_whitebalanced):
        """
        Displays a popup window to ask user confirmation about the white balanced result.
        Parameters
        ----------
        img_cv2_mask : image cv2
           image selected by user to correct white balance
        """

        cv2.destroyAllWindows()
        # Crear la finestra
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        w = screensize[0]
        h = screensize[1]
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title(self.lang.SEG_CONFIRM_WB)
        # Definir títol del popup
        title = ttk.Label(self.popup, text="White Balance Correction", font=FONT_TITOL)
        label_warning = ttk.Label(self.popup,
                                  text="Waring: method is still developing and testing. Please check the result:",
                                  font=FONT_MSG)
        label_info = ttk.Label(self.popup, text="Original image // White balanced image", font=FONT_MSG)
        title.configure(anchor="center")
        label_warning.configure(anchor="center")
        label_info.configure(anchor="center")
        title.pack(side="top", fill="x", pady=10)
        label_warning.pack(side="top", fill="x", pady=10)
        label_info.pack(side="top", fill="x", pady=10)
        # Carregar la roi i la imatge
        im_rgb = cv2.cvtColor(img_cv2_mask, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im_rgb)
        whitebalanced_rgb = cv2.cvtColor(img_whitebalanced, cv2.COLOR_BGR2RGB)
        whitebalanced = Image.fromarray(whitebalanced_rgb)
        images_frame = ttk.Frame(self.popup)
        imgtk = ImageTk.PhotoImage(image=im)
        whitebalanced_tk = ImageTk.PhotoImage(image=whitebalanced)
        img_label = tk.Label(images_frame, image=imgtk)
        whitebalanced_label = tk.Label(images_frame, image=whitebalanced_tk)
        img_label.grid(row=1, column=1, padx=5, pady=5)
        whitebalanced_label.grid(row=1, column=2, padx=5, pady=5)
        images_frame.pack(pady=30)
        # Botons GUI
        button1 = ttk.Button(self.popup, text="Accept", command=lambda: self.whitebalanced_ok(img_whitebalanced))
        button2 = ttk.Button(self.popup, text="Decline", command=self.whitebalanced_ko)
        button1.pack()
        button2.pack()
        self.popup.mainloop()

    def whitebalanced_ok(self, img_cv2_roi):
        """
        Sends a request to Controller with the image's white balanced result.
        Closes popup window.
        Parameters
        ----------
        img_cv2_roi : image cv2
           image selected and validated by user to reduce its flash
        """

        self.popup.destroy()
        pub.sendMessage("WHITEBALANCE_CONFIRMATED", img_cv2_whitebalanced=img_cv2_roi)

    def whitebalanced_ko(self):
        """
        Closes popup and all cv2 windows.
        """

        cv2.destroyAllWindows()
        self.popup.destroy()

    def update_whitebalanced_label(self, img_cv2_flash):
        """
        Updates the image's label of GUI processing with the whitebalanced one.
        Parameters
        ----------
        img_cv2_flash : image cv2
           image selected and validated by user to reduce its flash
        """

        whitebalanced_rgb = cv2.cvtColor(img_cv2_flash, cv2.COLOR_BGR2RGB)
        whitebalanced = Image.fromarray(whitebalanced_rgb)
        whitebalanced_tk = ImageTk.PhotoImage(image=whitebalanced)
        self.img_show.configure(image=whitebalanced_tk)
        self.img_show.image = whitebalanced_tk

    def ask_roi_confirmation(self, img_cv2_mask, img_cv2_roi, tissue, scale_percent, ring):
        """
        Displays a popup window to ask user confirmation about cropped roi
        comparing it with the image mask.
        Parameters
        ----------
        img_cv2_mask : image cv2
           image before cropping roi
        img_cv2_roi : image cv2
           image that requires user confirmation
        tissue : String
            tissue of the roi
        scale_percent : int
           image resize value (default = 100)
        """
        cv2.destroyAllWindows()
        # Crear la finestra
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        w = screensize[0]
        h = screensize[1]
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Confirmar regió")
        # Definir títol del popup
        title = ttk.Label(self.popup, text="És correcte la regió seleccionada?", font=FONT_TITOL)
        title.configure(anchor="center")
        title.pack(side="top", fill="x", pady=10)
        # Carregar la roi i la imatge
        im_rgb = cv2.cvtColor(img_cv2_mask, cv2.COLOR_BGR2RGB)
        roi_rgb = cv2.cvtColor(img_cv2_roi, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(im_rgb)
        roi = Image.fromarray(roi_rgb)
        # Escalar la imatge
        width = int(img_cv2_mask.shape[1] * scale_percent / 100)
        height = int(img_cv2_mask.shape[0] * scale_percent / 100)
        im = im.resize((width, height))
        images_frame = ttk.Frame(self.popup)
        imgtk = ImageTk.PhotoImage(image=im)
        roitk = ImageTk.PhotoImage(image=roi)
        img_label = tk.Label(images_frame, image=imgtk)
        roi_label = tk.Label(images_frame, image=roitk)
        img_label.grid(row=1, column=1, padx=5, pady=5)
        roi_label.grid(row=1, column=2, padx=5, pady=5)
        images_frame.pack(pady=30)
        # Botons GUI
        button1 = ttk.Button(self.popup, text="Sí", command=lambda: self.roi_ok(roi_rgb, tissue, ring))
        button2 = ttk.Button(self.popup, text="No", command=self.segmentacio_ko)
        button1.pack()
        button2.pack()
        self.popup.mainloop()

    def roi_ok(self, img_cv2_roi, tissue, ring):
        """
        Closes the popup window and sends a request with the roi and tissue's type.
        Parameters
        ----------
        img_cv2_roi : image cv2
           roi selected by the user
        tissue : String
            tissue of the roi
        """

        self.popup.destroy()
        if (ring == 1):
            img_cv2_roi = cv2.cvtColor(img_cv2_roi, cv2.COLOR_BGR2RGB)
            pub.sendMessage("ROI_CONFIRMATED", img_cv2_roi=img_cv2_roi, tissue=tissue, ring=ring)
        else:
            pub.sendMessage("ROI_CONFIRMATED", img_cv2_roi=img_cv2_roi, tissue=tissue, ring=ring)

    def segmentacio_ko(self):
        """
        Closes the cv2 and popup window.
        """

        cv2.destroyAllWindows()
        self.popup.destroy()
        pub.sendMessage("ROI_KO")

    def ask_zone_type(self, tissue):

        cv2.destroyAllWindows()
        # Crear la finestra
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 600
        h = 300
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Tipus de zona")
        # Definir títol del popup
        title = ttk.Label(self.popup, text="Selecciona el tipus de zona:", font=FONT_TITOL)
        title.configure(anchor="center")
        title.pack(side="top", fill="x", pady=20)
        frame = tk.Frame(self.popup)
        frame.pack()
        # Carregar les imatges
        path = "../resources/anella.png"
        img_a = ImageTk.PhotoImage(Image.open(path))
        img_anella = tk.Label(frame, image=img_a)
        img_anella.grid(row=1, column=1, padx=5, pady=5)
        path = "../resources/tancat.png"
        img_t = ImageTk.PhotoImage(Image.open(path))
        img_tancat = tk.Label(frame, image=img_t)
        img_tancat.grid(row=1, column=2, padx=5, pady=5)

        # Botons GUI
        button1 = ttk.Button(frame, text="Anella", command=lambda: self.zona_anella(tissue))
        button2 = ttk.Button(frame, text="Tancada", command=lambda: self.zona_tancada(tissue))
        button1.grid(row=2, column=1, padx=5, pady=10)
        button2.grid(row=2, column=2, padx=5, pady=10)
        self.popup.mainloop()

    def zona_anella(self, tissue):
        self.popup.destroy()
        pub.sendMessage("RING_ZONE", tissue=tissue)

    def zona_tancada(self, tissue):
        self.popup.destroy()
        pub.sendMessage("CLOSED_ZONE", tissue=tissue)

    def ask_ring_out(self, tissue):
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 400
        h = 75
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Perímetre exterior")
        label = ttk.Label(self.popup, text="Teixit " + tissue + " : selecciona el perímetre exterior de la regió",
                          font=FONT_MSG)
        label.configure(anchor="center")
        label.pack(side="top", fill="x", pady=10)
        button1 = ttk.Button(self.popup, text="Exterior", command=lambda: self.ring_ext_clicked(tissue=tissue))
        button1.pack()
        self.popup.mainloop()

    def ring_ext_clicked(self, tissue):
        self.popup.destroy()
        pub.sendMessage("RING_EXT", tissue=tissue)

    def ring_int_clicked(self, tissue):
        self.popup.destroy()
        pub.sendMessage("RING_INT", tissue=tissue)

    def updateLabelGUI(self, img_mask):
        img_mask_rgb = cv2.cvtColor(img_mask, cv2.COLOR_BGR2RGB)
        img_mask = Image.fromarray(img_mask_rgb)
        img_mask_tk = ImageTk.PhotoImage(image=img_mask)
        self.img_show.configure(image=img_mask_tk)
        self.img_show.image = img_mask_tk

    def ask_ring_in(self, tissue):
        self.popup = tk.Toplevel()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 400
        h = 75
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title("Perímetre interior")
        label = ttk.Label(self.popup, text="Teixit " + tissue + " : selecciona el perímetre interior de la regió",
                          font=FONT_MSG)
        label.configure(anchor="center")
        label.pack(side="top", fill="x", pady=10)
        button1 = ttk.Button(self.popup, text="Interior", command=lambda: self.ring_int_clicked(tissue=tissue))
        button1.pack()
        self.popup.mainloop()

    def update_perimeter_count(self):
        """
        Updates the perimeter selection label as selected.
        """

        self.label_perimeter["text"] = "Perímetre seleccionat"
        self.label_perimeter["fg"] = "green"

    def update_granulation_count(self, number):
        """
        Update the granulation tissue's label with the number of rois selected.
        Parameters
        ----------
        number : int
           number of granulation rois already selected
        """

        self.label_granulation["text"] = self.lang.SEG_SELECTED_ZONES + str(number)

    def update_necrosis_count(self, number):
        """
        Update the necrosis tissue's label with the number of rois selected.
        Parameters
        ----------
        number : int
           number of necrosis rois already selected
        """

        self.label_necrosis["text"] = self.lang.SEG_SELECTED_ZONES + str(number)

    def update_slough_count(self, number):
        """
        Update the slough tissue's label with the number of rois selected.
        Parameters
        ----------
        number : int
           number of slough rois already selected
        """
        self.label_slough["text"] = self.lang.SEG_SELECTED_ZONES + str(number)
