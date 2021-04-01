"""Script with the GUI text in CATALAN.
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>
WARNING: choose language options still in development (no functional).
"""

class LangCAST:
    def __init__(self):
        #MENU
        self.LANG = "Idioma"

        #MAIN PAGE
        self.MAIN_TITLE = "Anotación de imágenes de úlceras de presión"
        self.BUTTON_1 = "Procesar imágenes"
        self.BUTTON_2 = "Visualizar imágenes"
        # Source: (https://ca.wikipedia.org/wiki/Escala_de_Barthel)
        self.BARTHEL_DESCRIPTION = "Escalera ordinal utilizada para mesurar el cumplimiento de actividades básicas de la vida diaria (AVDB)."
        # Source: (https://www.murciasalud.es/preevid/1103)
        self.EMINA_DESCRIPTION = "La escalera Emina es un instrumiento de valoración del riesgo de desarrollo de úlceras de presión en pacientes hospitalizados."

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
        self.PRE_CONFIRM_REGION = "Confirmar región"
        self.PRE_CORRECT_REGION = "Es correcta la región seleccionada?"

        # SEGMENTATION GUI
        self.HELPER_GRANULATION = "El tejido granuloso suele tener un aspecto rojizo i abultado, parecido a un guijarro."
        self.HELPER_NECROSIS = "El tejido necrotico está compuesto por restos de tejido granulado, músculo, grasa, tendón y/o piel muerta."
        self.HELPER_SLOUGH = "El tejido esfacelo se identifica como una masa fibrosa blanca/amarilla/verde/marrón que puede no estar adherida a la zona afectada."
