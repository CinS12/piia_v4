"""Script with the GUI text in CATALAN.
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>
WARNING: choose language options still in development (no functional).
"""
class LangENG:
    def __init__(self):

        #MENU
        self.LANG = "Language"

        #MAIN PAGE
        self.MAIN_TITLE = "Pressure Injuries Image Analysis"
        self.BUTTON_1 = "Image processing"
        self.BUTTON_2 = "Image viewer"
        # Source: (https://ca.wikipedia.org/wiki/Escala_de_Barthel)
        BARTHEL_DESCRIPTION = "Escala ordinal utilitzada per mesurar l'acompliment en activitats de la vida diària bàsiques (AVDB)."
        # Source: (https://www.murciasalud.es/preevid/1103)
        EMINA_DESCRIPTION = "L'escala Emina és un instrument de valoració del risc de desenvolupament d'úlceres de pressió en pacients hospitalitzats."

        # PROCESSING PAGE (FALTA)
        self.TITLE_PROCESSING = "Processar imatges"
        self.IMAGE_LOAD = "Carrega imatge"
        self.BACK = "Enrere"
        self.IMAGE_PROCESSING = "Processar imatge"

        self.META_TITLE = "Recull de dades"
        self.META_DATA_FILL = "Omplir els camps següents:"
        self.META_CODE = "Codi"
        self.META_YEAR = "Any neixament"
        self.META_SEX = "Sexe"
        self.META_MAN = "Home"
        self.META_WOMAN = "Dona"
        self.META_OTHER = "Altre"
        self.META_IMMOBILIZATION = "Temps d'immobilització"
        self.META_DAYS = "Dies"
        self.META_WEEKS = "Setmanes"
        self.META_MONTHS = "Mesos"
        self.META_HOSPITALIZATION = "Temps hospitalització"
        self.META_INST = "Temps institucionalització"
        self.META_DATE = "Data"
        self.META_EMINA = "Emina"
        self.META_BARTHEL = "Escala Barthel"
        self.META_CALCULATE = "Calcular"
        self.META_CONTENTION = "Contenció Mecànica"
        self.META_YES = "Sí"
        self.META_NO = "No"
        self.META_GRADE = "Grau de la nafra"
        self.META_EXO = "Cultiu de l'exsudat"
        self.META_POSITIVE = "Positiu"
        self.META_NEGATIVE = "Negatiu"
        self.META_PROTEIN = "Proteïnes totals"
        self.META_ALB = "Albúmina"
        self.META_TREATMENT = "Tractament"
        self.META_ANTIBIOTIC = "Antibiòtic"
        self.META_TOPIC = "Tòpic"
        self.META_SAVE = "Guardar"

        self.CODE_ERROR = "El codi ha de contenir 4 dígits"
        self.AGE_RROR = "L'any de naixement ha de contenir 4 enters"
        self.N_IMM_ERROR = "Format no vàlid: Temps d'immobilització"
        self.H_HOSP_ERROR = "Format no vàlid: Temps d'hospitalització"
        self.N_INST_ERROR = "Format no vàlid: Temps d'institucionalització"
        self.DATE_ERROR = "Format no vàlid: Data"
        self.N_CONTEN_ERROR = "Format no vàlid: Contenció mecànica"

        #PRE SEGMENTATION GUI
        self.PRE_CONFIRM_REGION = "Confirma region"
        self.PRE_CORRECT_REGION = "Is the region OK?"

        # SEGMENTATION GUI
        self.HELPER_GRANULATION = "Granulation tissue often appears as red, bumpy tissue that is described as “cobblestone-like” in appearance."
        self.HELPER_NECROSIS = "Necrosis tissue is composed of dead granulation tissue, muscle, fat, tendon or skin."
        self.HELPER_SLOUGH = "Slough can be identified as a stringy white/yellow/green/brown mass that may or may not be firmly attached to surrounding tissue."