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
        self.list_frame = tk.Frame(self.page)
        self.data_frame = tk.Frame(self.page)
        p2_label_2 = ttk.Label(self.page, text="Consultar base de dades", font=FONT_BENVINGUDA)
        p2_button_1 = ttk.Button(self.page, text="Enrere", command=self.tornar_main)
        self.crear_elements_viewer()
        self.page.grid(row=0, column=0, sticky="NESW")
        p2_label_2.pack(pady=20)
        p2_button_1.pack(pady=0, ipadx=15)
        self.list_frame.pack()
        self.data_frame.pack()
        self.p2_frame_list.pack(pady=15, padx=5, expand=False, side=tk.LEFT)
        self.p2_frame_list_3.pack(pady=15, padx=5, expand=False, side=tk.RIGHT)
        self.p2_frame_list_2.pack(pady=15, padx=5, expand=False, side=tk.RIGHT)
        self.p2_frame_list_1.pack(pady=15, padx=5, expand=False, side=tk.RIGHT)
        self.p2_frame_elements.pack(pady=0, padx=10, side=tk.LEFT)
        self.p2_frame_img.grid(row=1, column=1, pady=5, padx=20, sticky="w")
        self.p2_frame_metadata.grid(row=1, column=2, pady=20, padx=20, sticky="w")

    def crear_elements_viewer(self):
        """
        Creates and places the main frames and labels of page 2 (View images).
        """

        self.p2_frame_list = tk.Frame(self.list_frame, borderwidth=2, relief="groove")
        self.p2_label_info = ttk.Label(self.p2_frame_list, text="Id pacient: ", font=FONT_TITOL)
        self.p2_label_info.pack()
        scrollbar = tk.Scrollbar(self.p2_frame_list)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.llista = tk.Listbox(self.p2_frame_list, yscrollcommand=scrollbar.set, width=15, height=7)
        self.llista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.llista.yview)

        self.p2_frame_list_1 = tk.Frame(self.list_frame, borderwidth=2, relief="groove")
        self.p2_label_info_1 = ttk.Label(self.p2_frame_list_1, text="Localització: ", font=FONT_TITOL)
        self.p2_label_info_1.pack()
        scrollbar_1 = tk.Scrollbar(self.p2_frame_list_1)
        scrollbar_1.pack(side=tk.RIGHT, fill=tk.Y)
        self.llista_1 = tk.Listbox(self.p2_frame_list_1, yscrollcommand=scrollbar_1.set, width=15, height=7)
        self.llista_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_1.config(command=self.llista_1.yview)

        self.p2_frame_list_2 = tk.Frame(self.list_frame, borderwidth=2, relief="groove")
        self.p2_label_info_2 = ttk.Label(self.p2_frame_list_2, text="Data: ", font=FONT_TITOL)
        self.p2_label_info_2.pack()
        scrollbar_2 = tk.Scrollbar(self.p2_frame_list_2)
        scrollbar_2.pack(side=tk.RIGHT, fill=tk.Y)
        self.llista_2 = tk.Listbox(self.p2_frame_list_2, yscrollcommand=scrollbar_2.set, width=15, height=7)
        self.llista_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_2.config(command=self.llista_2.yview)

        self.p2_frame_list_3 = tk.Frame(self.list_frame, borderwidth=2, relief="groove")
        self.p2_label_info_3 = ttk.Label(self.p2_frame_list_3, text="Image: ", font=FONT_TITOL)
        self.p2_label_info_3.pack()
        scrollbar_3 = tk.Scrollbar(self.p2_frame_list_3)
        scrollbar_3.pack(side=tk.RIGHT, fill=tk.Y)
        self.llista_3 = tk.Listbox(self.p2_frame_list_3, yscrollcommand=scrollbar_3.set, width=15, height=7)
        self.llista_3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_3.config(command=self.llista_3.yview)

        self.p2_frame_elements = tk.Frame(self.data_frame, borderwidth=2, relief="groove")
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
        self.p2_label_img.grid(row=1, column=2, padx=5, pady=0)

    def tornar_main(self):
        pub.sendMessage("BACK_TO_MAIN_PAGE")

    def update_patients(self, list):
        """
        Displays all found elements on the list.
        Creates the "double click" event to select an element.
        """

        self.llista.delete(0, tk.END)
        for i in range(len(list)):
            self.llista.insert(tk.END, list[i])
        self.llista.bind('<Double-1>', self.select_patient)

    def update_locations(self, id, list):
        """
        Displays all found elements on the list.
        Creates the "double click" event to select an element.
        """

        self.llista_1.delete(0, tk.END)
        for i in range(len(list)):
            self.llista_1.insert(tk.END, list[i])
        self.llista_1.bind('<Double-1>', lambda _: self.select_location(id))


    def update_dates(self, id, location, dates):
        """
        Displays all found elements on the list.
        Creates the "double click" event to select an element.
        """

        self.llista_2.delete(0, tk.END)
        for i in range(len(dates)):
            self.llista_2.insert(tk.END, dates[i])
        self.llista_2.bind('<Double-1>', lambda _: self.select_date(id, location))

    def select_date(self, id, location):
        index_selected = self.llista_2.curselection()
        date_selected = self.llista_2.get(index_selected[0])
        pub.sendMessage("DATE_SELECTED", id=id, location=location, dir=index_selected[0]+1)

    def select_patient(self, aux):
        """
        Sends the request with the id of list's selected element.
        Parameters
        ----------
        """
        n_elements = self.llista.curselection()
        pub.sendMessage("PATIENT_SELECTED", id=self.llista.get(n_elements[0]))

    def select_location(self, id):
        """
        Sends the request with the id of list's selected element.
        Parameters
        ----------
        """
        n_elements = self.llista_1.curselection()
        location = n_elements[0] + 1
        pub.sendMessage("LOCATION_SELECTED", id=id, location=location)

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
        self.p2_frame_metadata.configure(borderwidth=2, relief="groove")
        self.p2_label_metadata_code.config(text="Codi: " + metadata["metadata"]["code"])
        self.p2_label_metadata_grade.config(text="Grau: " + str(metadata["metadata"]["grade"]))
        self.p2_label_metadata_cm.config(text="Data: " + metadata["metadata"]["date"])
