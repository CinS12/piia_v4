"""Script with the GUI text in CATALAN.
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>
WARNING: choose language options still in development (no functional).
"""

class LangCAT:
    def __init__(self):
        #BASICS
        self.YES = "Sí"
        self.NO = "No"
        self.OK = "Ok"
        self.ACCEPT = "Acceptar"
        self.CONTINUE = "Continuar"
        # MENU
        self.LANG = "Idioma"

        # MAIN PAGE
        self.MAIN_TITLE = "Anotació d'imatges d'úlceres de pressió" #"Pressure Injuries Image Analysis"
        self.BUTTON_1 = "Afegir imatge a la base de dades"
        self.BUTTON_2 = "Consultar base de dades"

        # PROCESSING PAGE
        self.TITLE_PROCESSING = self.BUTTON_1
        self.IMAGE_LOAD = "Carrega imatge"
        self.BACK = "Enrere"
        self.IMAGE_PROCESSING = "Processar imatge"

        self.META_TITLE = "Recull de dades"
        self.META_DATA_FILL = "Omplir els camps següents:"
        self.META_CODE = "Codi"
        self.META_CHECK = "Comprovar"
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
        self.META_EMPTY_CODE = "Escriu el codi per validar-lo"

        self.CODE_ERROR = "El codi ha de contenir 4 dígits"
        self.AGE_RROR = "L'any de naixement ha de contenir 4 enters"
        self.N_IMM_ERROR = "Format no vàlid: Temps d'immobilització"
        self.H_HOSP_ERROR = "Format no vàlid: Temps d'hospitalització"
        self.N_INST_ERROR = "Format no vàlid: Temps d'institucionalització"
        self.DATE_ERROR = "Format no vàlid: Data"
        self.N_CONTEN_ERROR = "Format no vàlid: Contenció mecànica"

        #PRE SEGMENTATION GUI
        self.PRE_CONFIRM_REGION = "Confirmar regió"
        self.PRE_CORRECT_REGION = "És correcte la regió seleccionada?"

        self.PRE_NEW_CODE_TITLE = "Nou pacient"
        self.PRE_NEW_CODE_DESC_1 = "Es registrarà un nou pacient."
        self.PRE_LABEL_OLD = "Introdueix la localització de la ferida:"
        self.PRE_NEW_LOCATION_EMPTY = "S'ha d'omplir el camp: localització."

        self.PRE_ASK_CODE_TITLE = "Pacient existent"
        self.PRE_ASK_CODE_DESC_1 = "Seleccionar opció:"
        self.PRE_RADIOBUTTON_OLD = "Afegir imatge d'una ferida registrada."
        self.PRE_RADIOBUTTON_NEW = "Registrar una nova ferida."
        self.PRE_LABEL_NEW = "Localització:"
        self.PRE_CODE_RADIOBUTTONS = "Selecciona una opció"

        self.PRE_LOCATION_REPEATED = "Localització repetida. Escriu-ne una de nova."

        # SEGMENTATION GUI
        # Surce: https://www.woundsource.com/blog/identifying-types-tissues-found-pressure-ulcers
        self.HELPER_GRANULATION = "El teixit granulós sol tenir un aspecte vermellós i abultat, semblant a un còdol."
        self.HELPER_NECROSIS = "El teixit necrotic sol ser negre o marró i està compost per restes de teixit, múscul, greix, tendó o pell morta."
        self.HELPER_SLOUGH = "El teixit esfàcel és identificat com una massa fibrosa blanca/groga/verda/marró que pot no estar adherida a la zona afectada."
        self.SEG_TITLE = "Eina de segmentació"
        self.SEG_DESC = "Selecciona el perímetre total i els diferents tipus de teixits de la ferida:"
        self.SEG_WHITE = "Balanç de blancs"
        self.SEG_PERIMETER = "Perímetre"
        self.SEG_GRANULATION = "Granulós"
        self.SEG_NECROSIS = "Necròtic"
        self.SEG_SLOUGH = "Esfàcel"
        self.SEG_WHITEBALANCE_DESC = "Eina en desenvolupament, requereix supervisió."
        self.SEG_PERIMETER_DESC = "Selecciona el perímetre total de la ferida"
        self.SEG_SELECTED_ZONES = "Zones seleccionades: "
        self.SEG_GRANULATION_EX = "Exemple Granulation"
        self.SEG_NECROSIS_EX = "Exemple Necrosis"
        self.SEG_SLOUGH_EX = "Exemple Slough"
        self.SEG_CONFIRM_WB = "Confirm white balance"

        # MODEL PRESSURE IMAGE
        self.MODEL_PRESSURE_IMG = "Seleccionar zona rectangular: Marcador + Ferida. ENTER per acceptar."

        #EMINA-BARTHEL
        self.EB_WINDOW_B = "Calcular escala Barthel"
        self.EB_WINDOW_E = "Calcular escala Emina"
        # Source: (https://ca.wikipedia.org/wiki/Escala_de_Barthel)
        self.EB_BARTHEL_DESCRIPTION = "Escala ordinal utilitzada per mesurar l'acompliment en activitats de la vida diària bàsiques (AVDB)."
        # Source: (https://www.murciasalud.es/preevid/1103)
        self.EB_EMINA_DESCRIPTION = "L'escala Emina és un instrument de valoració del risc de desenvolupament d'úlceres de pressió en pacients hospitalitzats."
        self.EB_SELECT = "Selecciona els paràmetres corresponents:"
        self.EB_EAT = "Menjar"
        self.EB_INDEP = "Independent"
        self.EB_MIN_HELP = "Mínima ajuda"
        self.EB_HELP = "Necessita ajuda"
        self.EB_MAX_HELP = "Gran ajuda"
        self.EB_WHEEL_HELP = "Independent en cadira de rodes"
        self.EB_DEP = "Dependent"
        self.EB_WASH = "Rentar-se (banyar-se)"
        self.EB_DRESS = "Vestir-se"
        self.EB_READY = "Arreglar-se"
        self.EB_DEPO = "Deposició"
        self.EB_CONT = "Continent"
        self.EB_OCC = "Accident ocasional"
        self.EB_INCONT = "Incontinent"
        self.EB_MICC = "Micció"
        self.EB_WC = "Anar al lavabo"
        self.EB_MOVE = "Traslladar-se (ex: buataca/llit)"
        self.EB_WALK = "Deambulació"
        self.EB_STAIRS = "Pujar i baixar escales"
        self.EB_SAVE = "Desar"

        #VIEWER MANAGER
        self.VM_title = "Evolució de la ferida"
        self.VM_id = "Id pacient: "
        self.VM_location = "Localització ferida: "
        self.VM_cm = "cm"
        self.VM_perimeter_title = "Perímetre total"
        self.VM_perimeter_area = "Àrea total"
        self.VM_granulation = "Àrea teixit granulós"
        self.VM_slough = "Àrea teixit esfàcel"
        self.VM_necrosis = "Àrea teixit necròtic"