import tkinter as tk
from tkinter import ttk
from pubsub import pub
from pathlib import Path
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from View import V_EminaBarthel
import cv2
from View.V_Page import Page
FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)
from language_CAT import *

class ProcessingPage(Page):
    def __init__(self, parent, lang):
        self.container = parent
        self.lang = lang
        self.page = tk.Frame(self.container)
        self.elements_page()
        self.emina_barthel = V_EminaBarthel.EminaBarthel()
        return

    def elements_page(self):
        """
        Creates the frame and main labels of page_1's UI (Process images).
        """
        p1_label_1 = ttk.Label(self.page, text=self.lang.TITLE_PROCESSING, font=FONT_BENVINGUDA)
        p1_button_1 = ttk.Button(self.page, text=self.lang.IMAGE_LOAD, command=self.carregar_imatge)
        p1_button_2 = ttk.Button(self.page, text=self.lang.BACK, command=self.tornar_main)
        self.p1_button_img = ttk.Button(self.page, text=self.lang.IMAGE_PROCESSING, command=self.processar_img)
        path = Path(__file__).parent / "../resources/load_img.png"
        img = ImageTk.PhotoImage(Image.open(path))
        self.p1_img_label = tk.Label(self.page, image=img)
        self.p1_img_label.image = img
        self.crear_camps_dades()
        self.page.grid(row=0, column=0, sticky="NESW")
        p1_label_1.grid(row=0, column=2, pady=10, padx=1)
        p1_button_1.grid(row=1, column=1, pady=0, padx=20, sticky="SW")
        self.p1_img_label.grid(row=2, column=1, pady=0, padx=20, sticky="N")
        self.p1_data_frame.grid(row=2, column=3, pady=5, padx=1, sticky="n")
        p1_button_2.grid(row=1, column=2, pady=20, padx=20, sticky="w")
        self.p1_label_2.grid(row=1, column=1, padx=5, pady=0, sticky="n")
        self.p1_data_camps.grid(row=2, column=1, pady=20, padx=10)
        self.p1_button_3.grid(row=3, column=1, pady=10, padx=10, sticky="e")

    def carregar_imatge(self):
        """
        Sends a request to Controller to load an image.
        """

        pub.sendMessage("LOAD_IMAGE")

    def processar_img(self):
        """
        Sends a request to the Controller to start image processing.
        """
        pub.sendMessage("ANALYSE_IMAGE")

    def crear_camps_dades(self):
        """
        Creates and places all metadata fields's widgets and button 3 (save data).
        """

        self.popup_tr_ant = []
        self.popup_tr_top = []
        self.p1_data_frame = tk.Frame(self.page, borderwidth=2, relief="groove")
        self.p1_label_2 = ttk.Label(self.p1_data_frame, text=self.lang.META_TITLE, font=FONT_BENVINGUDA)

        self.p1_data_camps = ttk.Frame(self.p1_data_frame, borderwidth=2, relief="groove")
        self.p1_data_label = ttk.Label(self.p1_data_camps, text=self.lang.META_DATA_FILL, font=FONT_TITOL)
        self.p1_data_label.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        #Codi
        code_label = ttk.Label(self.p1_data_camps, text=self.lang.META_CODE, font=FONT_MSG)
        code_label.grid(row=2, column=1, padx=0, pady=10)
        self.code_entry = ttk.Entry(self.p1_data_camps)
        self.code_entry.insert(tk.END, '')
        self.code_entry.grid(row=2, column=2, padx=0, pady=10)
        #Edat
        age_label = ttk.Label(self.p1_data_camps, text=self.lang.META_YEAR, font=FONT_MSG)
        age_label.grid(row=3, column=1, padx=0, pady=10)
        self.age_pers_entry = ttk.Entry(self.p1_data_camps)
        self.age_pers_entry.insert(tk.END, '')
        self.age_pers_entry.grid(row=3, column=2, padx=0, pady=10)
        #Sexe
        gender_pers_label = ttk.Label(self.p1_data_camps, text=self.lang.META_SEX, font=FONT_MSG)
        gender_pers_label.grid(row=4, column=1, padx=5, pady=10)
        self.gender_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=17, justify="left")
        self.gender_combobox["values"] = [self.lang.META_MAN, self.lang.META_WOMAN, self.lang.META_OTHER]
        self.gender_combobox.grid(row=4, column=2, padx=5, pady=10)
        #Temps immobilització
        temps_imm = ttk.Label(self.p1_data_camps, text=self.lang.META_IMMOBILIZATION, font=FONT_MSG)
        temps_imm.grid(row=6, column=1, padx=0, pady=10)
        self.temps_imm_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.temps_imm_entry.insert(tk.END, '')
        self.temps_imm_entry.grid(row=6, column=2, padx=0, pady=10, sticky="w")
        self.temps_imm_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.temps_imm_combobox["values"] = [self.lang.META_DAYS, self.lang.META_WEEKS, self.lang.META_MONTHS]
        self.temps_imm_combobox.current(0)
        self.temps_imm_combobox.grid(row=6, column=2, padx=5, pady=10, sticky="e")
        #Temps hospitalització
        temps_hosp = ttk.Label(self.p1_data_camps, text=self.lang.META_HOSPITALIZATION, font=FONT_MSG)
        temps_hosp.grid(row=7, column=1, padx=0, pady=10)
        self.temps_hosp_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.temps_hosp_entry.insert(tk.END, '')
        self.temps_hosp_entry.grid(row=7, column=2, padx=0, pady=10, sticky="w")
        self.temps_hosp_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.temps_hosp_combobox["values"] = [self.lang.META_DAYS, self.lang.META_WEEKS, self.lang.META_MONTHS]
        self.temps_hosp_combobox.current(0)
        self.temps_hosp_combobox.grid(row=7, column=2, padx=5, pady=10, sticky="e")
        # Temps institucionalització
        temps_inst = ttk.Label(self.p1_data_camps, text=self.lang.META_INST, font=FONT_MSG)
        temps_inst.grid(row=8, column=1, padx=0, pady=10)
        self.temps_inst_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.temps_inst_entry.insert(tk.END, '')
        self.temps_inst_entry.grid(row=8, column=2, padx=0, pady=10, sticky="w")
        self.temps_inst_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.temps_inst_combobox["values"] = [self.lang.META_DAYS, self.lang.META_WEEKS, self.lang.META_MONTHS]
        self.temps_inst_combobox.current(0)
        self.temps_inst_combobox.grid(row=8, column=2, padx=5, pady=10, sticky="e")
        #Data
        date_label = ttk.Label(self.p1_data_camps, text=self.lang.META_DATE, font=FONT_MSG)
        date_label.grid(row=9, column=1, padx=5, pady=10)
        self.cal_data_entry = DateEntry(self.p1_data_camps, dateformat=3, width=12, background='darkblue',
                        foreground='white', borderwidth=4)
        self.cal_data_entry.grid(row=9, column=2, sticky='nsew')
        # Escala EMINA
        emina_label = ttk.Label(self.p1_data_camps, text=self.lang.META_EMINA, font=FONT_MSG)
        emina_label.grid(row=10, column=1, padx=0, pady=10)
        self.emina_scale = tk.Scale(self.p1_data_camps, from_=0, to=15, resolution=1, orient=tk.HORIZONTAL)
        self.emina_scale.grid(row=10, column=2, padx=0, pady=10)
        barthel_button = ttk.Button(self.p1_data_camps, text="Calcular",
                                    command=lambda: self.emina_barthel.popup_emina(self.lang.META_EMINA))
        barthel_button.grid(row=10, column=3, pady=10, padx=0)
        #Escala Barthel
        barthel_label = ttk.Label(self.p1_data_camps, text=self.lang.META_BARTHEL, font=FONT_MSG)
        barthel_label.grid(row=11, column=1, padx=0, pady=10)
        self.barthel_scale = tk.Scale(self.p1_data_camps, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL)
        self.barthel_scale.grid(row=11, column=2, padx=0, pady=10)
        barthel_button = ttk.Button(self.p1_data_camps, text=self.lang.META_CALCULATE,
                                    command=lambda: self.emina_barthel.popup_barthel(self.lang.META_BARTHEL))
        barthel_button.grid(row=11, column=3, pady=10, padx=0)
        #Contenció mecànica
        self.contencio=""
        conten_label = ttk.Label(self.p1_data_camps, text=self.lang.META_CONTENTION, font=FONT_MSG)
        conten_label.grid(row=12, column=1, padx=0, pady=10)
        self.conten_radiobutton_si = ttk.Radiobutton(self.p1_data_camps, variable="conten", text=self.lang.YES, value="si", command=self.ask_time)
        self.conten_radiobutton_no = ttk.Radiobutton(self.p1_data_camps, variable="conten", text=self.lang.NO, value="no", command=self.no_time)
        self.conten_radiobutton_si.grid(row=12, column=2, padx=0, pady=10, sticky="w")
        self.conten_radiobutton_no.grid(row=13, column=2, padx=0, pady=10, sticky="w")
        self.temps_conten_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.temps_conten_entry.insert(tk.END, '')
        self.temps_conten_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.temps_conten_combobox["values"] = [self.lang.META_DAYS, self.lang.META_WEEKS, self.lang.META_MONTHS]
        self.temps_conten_combobox.current(0)
        #Grau de la nafra
        grade_label = ttk.Label(self.p1_data_camps, text=self.lang.META_GRADE, font=FONT_MSG)
        grade_label.grid(row=14, column=1, padx=0, pady=10)
        self.grade_combobox = ttk.Combobox(self.p1_data_camps, state="readonly", width=9, justify="left")
        self.grade_combobox["values"] = [1, 2, 3, 4]
        self.grade_combobox.grid(row=14, column=2, padx=5, pady=10, sticky="w")
        #Cultiu de l’exsudat
        self.cultiu=""
        cultiu_label = ttk.Label(self.p1_data_camps, text=self.lang.META_EXO, font=FONT_MSG)
        cultiu_label.grid(row=15, column=1, padx=0, pady=10)
        self.cultiu_radiobutton_positive = ttk.Radiobutton(self.p1_data_camps, variable="cultiu", text=self.lang.META_POSITIVE, value="positive", command=self.cultiu_si)
        self.cultiu_radiobutton_negative = ttk.Radiobutton(self.p1_data_camps, variable="cultiu", text=self.lang.META_NEGATIVE, value="negative", command=self.cultiu_no)
        self.cultiu_radiobutton_positive.grid(row=15, column=2, padx=0, pady=10, sticky="w")
        self.cultiu_radiobutton_negative.grid(row=15, column=2, padx=0, pady=10, sticky="e")
        #Proteïnes totals
        protein_label = ttk.Label(self.p1_data_camps, text=self.lang.META_PROTEIN, font=FONT_MSG)
        protein_label.grid(row=16, column=1, padx=0, pady=10)
        self.protein_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.protein_entry.insert(tk.END, '')
        self.protein_entry.grid(row=16, column=2, padx=0, pady=10, sticky="w")
        protein_unit_label = ttk.Label(self.p1_data_camps, text="g/l", font=FONT_MSG)
        protein_unit_label.grid(row=16, column=2, padx=0, pady=10)
        #Albúmina
        albumina_label = ttk.Label(self.p1_data_camps, text=self.lang.META_ALB, font=FONT_MSG)
        albumina_label.grid(row=17, column=1, padx=0, pady=10)
        self.albumina_entry = ttk.Entry(self.p1_data_camps, width=6)
        self.albumina_entry.insert(tk.END, '')
        self.albumina_entry.grid(row=17, column=2, padx=0, pady=10, sticky="w")
        albumina_unit_label = ttk.Label(self.p1_data_camps, text="g/l", font=FONT_MSG)
        albumina_unit_label.grid(row=17, column=2, padx=0, pady=10)
        #Tractament
        tr_label = ttk.Label(self.p1_data_camps, text=self.lang.META_TREATMENT, font=FONT_MSG)
        tr_label.grid(row=18, column=1, padx=5, pady=10)
        tr_ant_button = ttk.Button(self.p1_data_camps, text=self.lang.META_ANTIBIOTIC,
                                     command=lambda: self.emina_barthel.entry_popup_tr_ant(self.lang.META_ANTIBIOTIC))
        tr_ant_button.grid(row=18, column=2, pady=10, padx=0, sticky="e")
        tr_top_button = ttk.Button(self.p1_data_camps, text=self.lang.META_TOPIC,
                                   command=lambda: self.emina_barthel.entry_popup_tr_top(
                                       self.lang.META_TOPIC))
        tr_top_button.grid(row=18, column=3, pady=10, padx=0)
        #Submit
        self.p1_button_3 = ttk.Button(self.p1_data_frame, text=self.lang.META_SAVE, command=self.apretar_boto_3)


    def ask_time(self):
        """
        Places the widgets of contention's time field.
        """

        self.temps_conten_entry.grid(row=12, column=2, padx=0, pady=10, sticky="e")
        self.temps_conten_combobox.grid(row=12, column=3, padx=5, pady=10, sticky="w")
        self.contencio = "si"

    def no_time(self):
        """
        Hides the widgets of contention's time field.
        """
        self.temps_conten_entry.grid_forget()
        self.temps_conten_combobox.grid_forget()
        self.contencio = "no"

    def cultiu_si(self):
        """
        Updates the value of "cultiu" to Yes.
        """

        self.cultiu = "si"

    def cultiu_no(self):
        """
        Updates the value of "cultiu" to Yes.
        """

        self.cultiu = "no"

    def apretar_boto_3(self):
        """
        Sends a request to check and storage the metadata and processed image.
        """

        print("view -   Botó 3!")
        data = [self.code_entry, self.age_pers_entry, self.gender_combobox, self.temps_imm_entry,
                self.temps_imm_combobox, self.temps_hosp_entry, self.temps_hosp_combobox, self.temps_inst_entry,
                self.temps_inst_combobox, self.cal_data_entry, self.emina_scale, self.barthel_scale,
                self.contencio, self.temps_conten_entry, self.temps_conten_combobox, self.grade_combobox, self.cultiu,
                self.protein_entry, self.albumina_entry, self.emina_barthel.popup_tr_ant, self.emina_barthel.popup_tr_top]
        pub.sendMessage("BUTTON_3_PRESSED", data=data)

    def tornar_main(self):
        pub.sendMessage("BACK_TO_MAIN_PAGE")

    def update_image(self, img_tk):
        """
        Sends a request to Controller to update the image label.
        Parameters
        ----------
        image_tk : PIL Image
           image ready to be loaded in a label
        """

        self.p1_img_label.configure(image=img_tk)
        self.p1_img_label.image = img_tk
        return

    def botoImg(self):
        """
        Places the button to process image.
        """

        self.p1_button_img.grid(row=1, column=1, pady=0, padx=20, sticky="SE")

    def update_main_label(self, img_tk):
        img_mask_rgb = cv2.cvtColor(img_tk, cv2.COLOR_BGR2RGB)
        img_mask = Image.fromarray(img_mask_rgb)
        img_mask_tk = ImageTk.PhotoImage(image=img_mask)
        self.p1_img_label.configure(image=img_mask_tk)
        self.p1_img_label.image = img_mask_tk

    def update_barthel(self, data):
        """
        Updates barthel's Scale widget with the calculated value.
        Parameters
        ----------
        data : int
            value of the barthel scale
       """

        self.barthel_scale.set(data)

    def update_emina(self, data):
        """
        Updates emina's Scale widget with the calculated value.
        Parameters
        ----------
        data : int
            value of the emina scale
       """

        self.emina_scale.set(data)

    def show_error(self, data_error):
        """
        Calls the popup function to display the errors found.
        Parameters
        ----------
        error : list
           wrong input data field's name
        """

        if "CODE_ERROR" in data_error:
            pub.sendMessage("POPUP_MSG", msg=self.lang.CODE_ERROR)
        if "AGE_ERROR" in data_error:
            pub.sendMessage("POPUP_MSG", msg=self.lang.AGE_RROR)
        if "N_IMM_ERROR" in data_error:
            pub.sendMessage("POPUP_MSG", msg=self.lang.N_IMM_ERROR)
        if "N_HOSP_ERROR" in data_error:
            pub.sendMessage("POPUP_MSG", msg=self.lang.H_HOSP_ERROR)
        if "N_INST_ERROR" in data_error:
            pub.sendMessage("POPUP_MSG", msg=self.lang.N_INST_ERROR)
        if "DATE_ERROR" in data_error:
            pub.sendMessage("POPUP_MSG", msg=self.lang.DATE_ERROR)
        if "N_CONTEN_ERROR" in data_error:
            pub.sendMessage("POPUP_MSG", msg=self.N_CONTEN_ERROR)

    def reset_view(self):
        """
        Resets image label (after processing process).
        """

        path = Path(__file__).parent / "../resources/load_img.png"
        img = ImageTk.PhotoImage(Image.open(path))
        self.p1_img_label.configure(image=img)
        self.p1_img_label.image = img
        self.p1_button_img.grid_forget()