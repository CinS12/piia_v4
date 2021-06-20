import tkinter as tk
from tkinter import ttk
from pubsub import pub

FONT_BENVINGUDA = ("Verdana", 12)
FONT_TITOL = ("Verdana", 10)
FONT_MSG = ("Verdana", 8)

class EminaBarthel:
    def __init__(self, lang):
        self.lang = lang
        self.popup_tr_ant = []
        self.popup_tr_top = []
        return
    def popup_barthel(self, title):
        """
        Display a popup for barthel scale's value calculation.
        Parameters
        ----------
        title : String
           title of the widget
        """
        self.popup_sit_nutr = ""
        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 800
        h = 700
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title(self.lang.EB_WINDOW_B)

        label = ttk.Label(self.popup, text=title, font=FONT_TITOL)
        label.pack(pady=10)
        text = tk.Text(self.popup, font=FONT_TITOL, relief=tk.GROOVE, width=70, height=3, wrap=tk.WORD)
        text.insert(tk.END, self.lang.EB_BARTHEL_DESCRIPTION, "desc")
        text.config(state=tk.DISABLED)
        text.tag_configure("desc", justify="center")
        text.config(pady=10, padx=10)
        text.pack(pady=20)
        self.barthel_frame = tk.Frame(self.popup)
        self.barthel_frame.pack(pady=5, padx=10)
        #Selecció
        label_description = ttk.Label(self.barthel_frame, text=self.lang.EB_SELECT, font=FONT_MSG)
        label_description.grid(row=1, column=2, padx=10, pady=10)
        #Camp menjar
        barthel_menjar = ttk.Label(self.barthel_frame, text=self.lang.EB_EAT, font=FONT_MSG)
        barthel_menjar.grid(row=2, column=1, padx=10, pady=10)
        self.menjar_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.menjar_combobox["values"] = [self.lang.EB_INDEP, self.lang.EB_HELP, self.lang.EB_DEP]
        self.menjar_combobox.grid(row=2, column=2, padx=10, pady=10)
        #Camp rentar-se/banyar-se
        barthel_rentar = ttk.Label(self.barthel_frame, text=self.lang.EB_WASH, font=FONT_MSG)
        barthel_rentar.grid(row=3, column=1, padx=10, pady=10)
        self.rentar_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.rentar_combobox["values"] = [self.lang.EB_INDEP, self.lang.EB_DEP]
        self.rentar_combobox.grid(row=3, column=2, padx=10, pady=10)
        #Camp vestir-se
        barthel_vestir = ttk.Label(self.barthel_frame, text=self.lang.EB_DRESS, font=FONT_MSG)
        barthel_vestir.grid(row=4, column=1, padx=10, pady=10)
        self.vestir_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.vestir_combobox["values"] = [self.lang.EB_INDEP, self.lang.EB_HELP, self.lang.EB_DEP]
        self.vestir_combobox.grid(row=4, column=2, padx=10, pady=10)
        #Camp arreglar-se
        barthel_arreglar = ttk.Label(self.barthel_frame, text=self.lang.EB_READY, font=FONT_MSG)
        barthel_arreglar.grid(row=5, column=1, padx=10, pady=10)
        self.arreglar_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.arreglar_combobox["values"] = [self.lang.EB_INDEP, self.lang.EB_DEP]
        self.arreglar_combobox.grid(row=5, column=2, padx=10, pady=10)
        #Camp deposició
        barthel_deposicio = ttk.Label(self.barthel_frame, text=self.lang.EB_DEPO, font=FONT_MSG)
        barthel_deposicio.grid(row=6, column=1, padx=10, pady=10)
        self.deposicio_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.deposicio_combobox["values"] = [self.lang.EB_CONT, self.lang.EB_OCC, self.lang.EB_INCONT]
        self.deposicio_combobox.grid(row=6, column=2, padx=10, pady=10)
        #Camp micció
        barthel_miccio = ttk.Label(self.barthel_frame, text=self.lang.EB_MICC, font=FONT_MSG)
        barthel_miccio.grid(row=7, column=1, padx=10, pady=10)
        self.miccio_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.miccio_combobox["values"] = [self.lang.EB_CONT, self.lang.EB_OCC, self.lang.EB_INCONT]
        self.miccio_combobox.grid(row=7, column=2, padx=10, pady=10)
        #Camp anar al lavabo
        barthel_lavabo = ttk.Label(self.barthel_frame, text=self.lang.EB_WC, font=FONT_MSG)
        barthel_lavabo.grid(row=8, column=1, padx=10, pady=10)
        self.lavabo_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.lavabo_combobox["values"] = [self.lang.EB_INDEP, self.lang.EB_HELP, self.lang.EB_DEP]
        self.lavabo_combobox.grid(row=8, column=2, padx=10, pady=10)
        #Camp traslladar-se (ex: butaca/llit)
        barthel_trasllat = ttk.Label(self.barthel_frame, text=self.lang.EB_MOVE, font=FONT_MSG)
        barthel_trasllat.grid(row=9, column=1, padx=10, pady=10)
        self.trasllat_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.trasllat_combobox["values"] = [self.lang.EB_INDEP, self.lang.EB_MIN_HELP, self.lang.EB_MAX_HELP, self.lang.EB_DEP]
        self.trasllat_combobox.grid(row=9, column=2, padx=10, pady=10)
        #Camp deambulació
        barthel_deambulacio = ttk.Label(self.barthel_frame, text=self.lang.EB_WALK, font=FONT_MSG)
        barthel_deambulacio.grid(row=10, column=1, padx=10, pady=10)
        self.deambulacio_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.deambulacio_combobox["values"] = [self.lang.EB_INDEP, self.lang.EB_MIN_HELP, self.lang.EB_WHEEL_HELP, self.lang.EB_DEP]
        self.deambulacio_combobox.grid(row=10, column=2, padx=10, pady=10)
        #Camp pujar i baixar escales
        barthel_escales = ttk.Label(self.barthel_frame, text=self.lang.EB_STAIRS, font=FONT_MSG)
        barthel_escales.grid(row=11, column=1, padx=10, pady=10)
        self.escales_combobox = ttk.Combobox(self.barthel_frame, state="readonly", width=15, justify="left")
        self.escales_combobox["values"] = [self.lang.EB_INDEP, self.lang.EB_HELP, self.lang.EB_DEP]
        self.escales_combobox.grid(row=11, column=2, padx=10, pady=10)

        button_ok = ttk.Button(self.popup, text=self.lang.SAVE, command=self.barthel_getData)
        button_ok.pack(pady=20)

    def popup_emina(self, title):
        """
        Display a popup for emina scale's value calculation.
        Parameters
        ----------
        title : String
           title of the widget
        """

        self.popup_sit_nutr = ""
        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 800
        h = 600
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title(self.lang.EB_WINDOW_E)

        label = ttk.Label(self.popup, text=title, font=FONT_BENVINGUDA)
        label.pack(pady=10)
        text = tk.Text(self.popup, font=FONT_TITOL, relief=tk.GROOVE, width=70, height=3, wrap=tk.WORD)
        text.insert(tk.END, self.lang.EB_EMINA_DESCRIPTION, "desc")
        text.config(state=tk.DISABLED)
        text.tag_configure("desc", justify="center")
        text.config(pady=10, padx=10)
        text.pack(pady=30)
        self.emina_frame = tk.Frame(self.popup)
        self.emina_frame.pack(pady=5, padx=10)
        # Descripció
        label_description = ttk.Label(self.emina_frame, text=self.lang.EB_SELECT,
                                      font=FONT_MSG)
        label_description.grid(row=1, column=2, padx=10, pady=10)
        # Estat mental
        emina_mental = ttk.Label(self.emina_frame, text=self.lang.EB_MENTAL_STATE, font=FONT_MSG)
        emina_mental.grid(row=2, column=1, padx=10, pady=10)
        self.mental_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.mental_combobox["values"] = [self.lang.EB_ORIENTED, self.lang.EB_DISORIENTED, self.lang.EB_LET, self.lang.EB_UNC]
        self.mental_combobox.grid(row=2, column=2, padx=10, pady=10)
        # Movilitat
        emina_movilitat = ttk.Label(self.emina_frame, text=self.lang.EB_MOBILITY, font=FONT_MSG)
        emina_movilitat.grid(row=3, column=1, padx=10, pady=10)
        self.movilitat_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.movilitat_combobox["values"] = [self.lang.EB_COMP, self.lang.EB_LIT_LIM, self.lang.EB_IMP_LIM, self.lang.EB_IMM]
        self.movilitat_combobox.grid(row=3, column=2, padx=10, pady=10)
        # Humitat R/C, Incontinencia
        emina_humitat = ttk.Label(self.emina_frame, text=self.lang.EB_HUM, font=FONT_MSG)
        emina_humitat.grid(row=4, column=1, padx=10, pady=10)
        self.humitat_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.humitat_combobox["values"] = [self.lang.NO, self.lang.EB_OCC, self.lang.EB_HAB, self.lang.EB_BOTH]
        self.humitat_combobox.grid(row=4, column=2, padx=10, pady=10)
        # Nutrició
        emina_nutricio = ttk.Label(self.emina_frame, text=self.lang.EB_NUT, font=FONT_MSG)
        emina_nutricio.grid(row=5, column=1, padx=10, pady=10)
        self.nutricio_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.nutricio_combobox["values"] = [self.lang.EB_CORR, self.lang.EB_OCC_UNC, self.lang.EB_UNC, self.lang.EB_NO]
        self.nutricio_combobox.grid(row=5, column=2, padx=10, pady=10)
        # Activitat
        emina_activitat = ttk.Label(self.emina_frame, text=self.lang.EB_ACT, font=FONT_MSG)
        emina_activitat.grid(row=6, column=1, padx=10, pady=10)
        self.activitat_combobox = ttk.Combobox(self.emina_frame, state="readonly", width=30, justify="left")
        self.activitat_combobox["values"] = [self.lang.EB_DMB, self.lang.EB_HLP_DMB, self.lang.EB_ALWS_HLP, self.lang.EB_NO_DMB]
        self.activitat_combobox.grid(row=6, column=2, padx=10, pady=10)

        button_ok = ttk.Button(self.popup, text=self.lang.SAVE, command=self.emina_getData)
        button_ok.pack()

    def barthel_getData(self):
        """
        Saves the barthel sacle answers to an attribute,
        sends a request with this data and closes popup.
        """

        data = self
        pub.sendMessage("BARTHEL_DATA_SENT", data=data)
        self.popup.destroy()

    def emina_getData(self):
        """
        Saves the emina sacle answers to an attribute,
        sends a request with this data and closes popup.
        """

        data = self
        pub.sendMessage("EMINA_DATA_SENT", data=data)
        self.popup.destroy()

    def entry_popup_tr_ant(self, title):
        """
        Display a popup for antibiotics treatment's comments.

        Parameters
        ----------
        title : String
           title of the widget
        """

        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 600
        h = 400
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title(self.lang.EB_TXT)
        label = ttk.Label(self.popup, text=title, font=FONT_TITOL)
        label.pack(pady=10)
        self.tr_ant_text = tk.Text(self.popup, font=FONT_MSG)
        try:
            self.tr_ant_text.insert(tk.INSERT, self.popup_tr_ant)
        except:
            pass
        self.tr_ant_text.pack(pady=5, padx=10)
        button_ok = ttk.Button(self.popup, text=self.lang.SAVE, command=self.p1_tr_ant_ok)
        button_ok.pack()

    def entry_popup_tr_top(self, title):
        """
        Display a popup for topical treatment's comments.

        Parameters
        ----------
        title : String
           title of the widget
        """

        self.popup = tk.Tk()
        ws = self.popup.winfo_screenwidth()
        hs = self.popup.winfo_screenheight()
        w = 600
        h = 400
        x = (ws / 2) - (w / 2)
        y = (hs / 3) - (h / 3)
        self.popup.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.popup.wm_title(self.lang.EB_TXT)
        label = ttk.Label(self.popup, text=title, font=FONT_TITOL)
        label.pack(pady=10)
        self.tr_top_text = tk.Text(self.popup, font=FONT_MSG)
        try:
            self.tr_top_text.insert(tk.INSERT, self.popup_tr_top)
        except:
            pass
        self.tr_top_text.pack(pady=5, padx=10)
        button_ok = ttk.Button(self.popup, text=self.lang.SAVE, command=self.p1_tr_top_ok)
        button_ok.pack()

    def p1_tr_top_ok(self):
        """
        Saves the topical treatment's comments to an attribute and closes popup.
        """

        self.popup_tr_top = self.tr_top_text.get(1.0, tk.END)
        self.popup.destroy()
        #print(self.popup_res_mic)

    def p1_tr_ant_ok(self):
        """
        Saves the antibiotics treatment's comments to an attribute and closes popup.
        """

        self.popup_tr_ant = self.tr_ant_text.get(1.0, tk.END)
        self.popup.destroy()
        #print(self.popup_sit_nutr)