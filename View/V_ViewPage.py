import tkinter as tk
from tkinter import ttk
from pubsub import pub
from View.V_Page import Page

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)


class ViewPage(Page):
    def __init__(self, parent, lang):
        self.container = parent
        self.lang = lang
        self.page = tk.Frame(self.container)
        self.elements_page()
        return

    def elements_page(self):
        """
               Creates the frame and main labels of page_2's UI (View images).
               """
        p2_label_2 = ttk.Label(self.page, text="Visualitzar imatges", font=FONT_BENVINGUDA)
        p2_button_1 = ttk.Button(self.page, text="Enrere", command=self.tornar_main)
        self.crear_elements_viewer()
        self.page.grid(row=0, column=0, sticky="NESW")
        p2_label_2.pack(pady=20)
        p2_button_1.pack(pady=0)
        self.p2_frame_list.pack(pady=20)
        self.p2_frame_elements.pack(pady=20)
        self.p2_frame_img.grid(row=1, column=1, pady=20, padx=20, sticky="w")
        self.p2_frame_metadata.grid(row=1, column=2, pady=20, padx=20, sticky="w")
    def crear_elements_viewer(self):
        """
        Creates and places the main frames and labels of page 2 (View images).
        """

        self.p2_frame_list = tk.Frame(self.page, borderwidth=2, relief="groove")
        self.p2_label_info = ttk.Label(self.p2_frame_list, text="Elements trobats: ", font=FONT_TITOL)
        self.p2_label_info.pack()
        scrollbar = tk.Scrollbar(self.p2_frame_list)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.llista = tk.Listbox(self.p2_frame_list, yscrollcommand=scrollbar.set)
        self.llista.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.llista.yview)
        self.p2_frame_elements = tk.Frame(self.page)
        self.p2_frame_img = tk.Frame(self.p2_frame_elements)
        self.p2_frame_metadata = tk.Frame(self.p2_frame_elements)
        self.p2_label_metadata_code = ttk.Label(self.p2_frame_metadata, text="", font=FONT_MSG)
        self.p2_label_metadata_code.grid(row=1, column=2, padx=5, pady=5)
        self.p2_label_metadata_grade = ttk.Label(self.p2_frame_metadata, text="", font=FONT_MSG)
        self.p2_label_metadata_grade.grid(row=2, column=2, padx=5, pady=5)
        self.p2_label_metadata_cm = ttk.Label(self.p2_frame_metadata, text="", font=FONT_MSG)
        self.p2_label_metadata_cm.grid(row=3, column=2, padx=5, pady=5)
        self.assemble_img_frame()

    def assemble_img_frame(self):
        """
        Creates and places the label_img of page 2 (View images).
        """

        self.p2_label_img = ttk.Label(self.p2_frame_img, text="<Doble clic per carregar un element de la llista>",
                                      font=FONT_MSG)
        self.p2_label_img.grid(row=1, column=2, padx=5, pady=5)

    def tornar_main(self):
        pub.sendMessage("BACK_TO_MAIN_PAGE")


    def update_data_n_elements(self, num):
        """
        Updates the label_info of page 2
        with the number of elements found in the storage directory.
        Parameters
        ----------
        num : int
           number of images found in the storage directory
        """

        self.p2_label_info.config(text="Elements trobats: "+str(num))
        self.update_list(num)

    def update_list(self, num):
        """
        Displays all found elements on the list.
        Creates the "double click" event to select an element.
        """

        self.llista.delete(0, tk.END)
        for i in range(num):
            self.llista.insert(tk.END, "Imatge: "+str(i+1))
        self.llista.bind('<Double-1>', self.select_element)

    def select_element(self, aux):
        """
        Sends the request with the id of list's selected element.
        Parameters
        ----------
        """
        #print(aux)
        n_elements = self.llista.curselection()
        for i in n_elements:
            pub.sendMessage("ASK_IMAGE_i", i=i+1)

    def load_image_i(self, img_tk):
        """
        Loads the image to the label_img of page 2 (View images).
        Parameters
        ----------
        img_tk : PIL Image
           image ready to be loaded to a label
        """

        self.p2_label_img.configure(image=img_tk)
        self.p2_label_img.image = img_tk

    def load_metadata_i(self, metadata):
        """
        Loads the metadata to the metadata labels of page 2 (View images).
        Parameters
        ----------
        metadata : JSON Object
           data sent to be loaded into a label
        """
        self.p2_frame_metadata.configure(borderwidth = 2, relief = "groove")
        self.p2_label_metadata_code.config(text="Codi: "+metadata["metadata"]["code"])
        self.p2_label_metadata_grade.config(text="Grau: " + metadata["metadata"]["grade"])
        self.p2_label_metadata_cm.config(text="Perímetre: " + str(metadata["perimetre_cm"])+" cm")