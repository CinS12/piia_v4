"""Script with the GUI text in CATALAN.
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>
"""

class LangCAST:
    def __init__(self):
        #BASICS
        self.YES = "Si"
        self.NO = "No"
        self.OK = "Ok"
        self.ACCEPT = "Aceptar"
        self.CANCEL = "Cancelar"
        self.CONTINUE = "Continuar"
        self.SAVE = "Guardar"
        self.BACK = "Atrás"
        # MENU
        self.LANG = "Idioma"

        # MAIN PAGE
        self.MAIN_TITLE = "Anotación de Imágenes de Úlceras por Presión"
        self.BUTTON_1 = "Añadir imagen a la base de datos"
        self.BUTTON_2 = "Consultar base de datos"

        # PROCESSING PAGE
        self.TITLE_PROCESSING = self.BUTTON_1
        self.IMAGE_LOAD = "Cargar imagen"
        self.IMAGE_PROCESSING = "Procesar imágenes"

        self.META_TITLE = "Recolección de datos"
        self.META_DATA_FILL = "Rellenar los campos siguientes:"
        self.META_CODE = "Código"
        self.META_CHECK = "Validar"
        self.META_YEAR = "Año nacimiento"
        self.META_SEX = "Sexo"
        self.META_MAN = "Hombre"
        self.META_WOMAN = "Mujer"
        self.META_OTHER = "Otro"
        self.META_IMMOBILIZATION = "Tiempo inmovilización"
        self.META_DAYS = "Días"
        self.META_WEEKS = "Semanas"
        self.META_MONTHS = "Meses"
        self.META_HOSPITALIZATION = "Tiempo hospitalización"
        self.META_INST = "Tiempo institucionalización"
        self.META_DATE = "Fecha"
        self.META_EMINA = "Emina"
        self.META_BARTHEL = "Índice Barthel"
        self.META_CALCULATE = "Calcular"
        self.META_CONTENTION = "Contención Mecánica"
        self.META_GRADE = "Grado de la herida"
        self.META_EXO = "Cultivo del exsudato"
        self.META_POSITIVE = "Positivo"
        self.META_NEGATIVE = "Negativo"
        self.META_PROTEIN = "Proteínas totales"
        self.META_ALB = "Albúmina"
        self.META_TREATMENT = "Tratamiento"
        self.META_ANTIBIOTIC = "Antibiótico"
        self.META_TOPIC = "Tópico"
        self.META_SAVE = "Guardar"
        self.META_EMPTY_CODE = "Escribe el código para su validación"

        self.CODE_ERROR = "El código ha de contener 4 dígitos"
        self.AGE_RROR = "El año de nacimiento ha de contener 4 enteros"
        self.N_IMM_ERROR = "Formato no válido: Tiempo inmovilización"
        self.H_HOSP_ERROR = "Formato no válido: Tiempo hospitalización"
        self.N_INST_ERROR = "Formato no válido: Tiempo institucionalización"
        self.DATE_ERROR = "Formato no válido: Fecha"
        self.N_CONTEN_ERROR = "Formato no válido: Contención mecánica"

        #PRE SEGMENTATION GUI
        self.PRE_CONFIRM_REGION = "Confirmar región"
        self.PRE_CORRECT_REGION = "Es correcta la región seleccionada?"

        self.PRE_NEW_CODE_TITLE = "Nuevo paciente"
        self.PRE_NEW_CODE_DESC_1 = "Se registrarà un nuevo paciente."
        self.PRE_LABEL_OLD = "Introduzca la localización de la herida:"
        self.PRE_NEW_LOCATION_EMPTY = "Rellenar el campo: localización."

        self.PRE_ASK_CODE_TITLE = "Paciente existente"
        self.PRE_ASK_CODE_DESC_1 = "Seleccionar opción:"
        self.PRE_RADIOBUTTON_OLD = "Añadir imagen de una herida registrada."
        self.PRE_RADIOBUTTON_NEW = "Registrar una nueva herida."
        self.PRE_LABEL_NEW = "Localización:"
        self.PRE_CODE_RADIOBUTTONS = "Selecciona una opción"

        self.PRE_LOCATION_REPEATED = "Localización ya existente. Ha de ser diferente."

        # SEGMENTATION GUI
        # Surce: https://www.woundsource.com/blog/identifying-types-tissues-found-pressure-ulcers
        self.HELPER_GRANULATION = "El tejido granuloso suele tener un aspecto rojizo i abultado, parecido a un guijarro."
        self.HELPER_NECROSIS = "El tejido necrótico suele ser negro o marrón está compuesto por restos de tejido granulado, músculo, grasa, tendón y/o piel muerta."
        self.HELPER_SLOUGH = "El tejido esfacelo se identifica como una masa fibrosa blanca/amarilla/verde/marrón que puede no estar adherida a la zona afectada."
        self.SEG_TITLE = "Herramienta de segmentación"
        self.SEG_DESC = "Selecciona el perímetro total y los diferentes tipos de tejidos de la herida:"
        self.SEG_WHITE = "Balance de blancos"
        self.SEG_PERIMETER = "Perímetro"
        self.SEG_GRANULATION = "Granuloso"
        self.SEG_NECROSIS = "Necrótico"
        self.SEG_SLOUGH = "Esfacelo"
        self.SEG_WHITEBALANCE_DESC = "Herramienta en desarrollo, requiere supervisión."
        self.SEG_PERIMETER_DESC = "Selecciona el perímetro total de la herida"
        self.SEG_SELECTED_ZONES = "Zonas seleccionadas: "
        self.SEG_GRANULATION_EX = "Ejemplo Granuloso"
        self.SEG_NECROSIS_EX = "Ejemplo Necrótico"
        self.SEG_SLOUGH_EX = "Ejemplo Esfacelo"
        self.SEG_CONFIRM_WB = "Confirmar balance de blancos"

        # MODEL PRESSURE IMAGE
        self.MODEL_PRESSURE_IMG = "Seleccionar zona rectangular: Marcador + Herida. ENTER para aceptar."

        #EMINA-BARTHEL
        self.EB_WINDOW_B = "Calcular índice Barthel"
        self.EB_WINDOW_E = "Calcular índice Emina"
        # Source: (https://ca.wikipedia.org/wiki/Escala_de_Barthel)
        self.EB_BARTHEL_DESCRIPTION = "Escalera ordinal utilizada para mesurar el cumplimiento de actividades básicas de la vida diaria (AVDB)."
        # Source: (https://www.murciasalud.es/preevid/1103)
        self.EB_EMINA_DESCRIPTION = "La escalera Emina es un instrumiento de valoración del riesgo de desarrollo de úlceras de presión en pacientes hospitalizados."
        self.EB_SELECT = "Selecciona los parámetros correspondientes:"
        self.EB_EAT = "Comer"
        self.EB_INDEP = "Independiente"
        self.EB_MIN_HELP = "Mínima ayuda"
        self.EB_HELP = "Necesita ayuda"
        self.EB_MAX_HELP = "Gran ayuda"
        self.EB_WHEEL_HELP = "Independiente en silla de ruedas"
        self.EB_DEP = "Dependiente"
        self.EB_WASH = "Lavarse (bañarse)"
        self.EB_DRESS = "Vestirse"
        self.EB_READY = "Arreglarse"
        self.EB_DEPO = "Deposición"
        self.EB_CONT = "Continente"
        self.EB_OCC = "Accidente ocasional"
        self.EB_INCONT = "Incontinente"
        self.EB_MICC = "Micción"
        self.EB_WC = "Ir al baño"
        self.EB_MOVE = "Trasladarse (ej: buataca/cama)"
        self.EB_WALK = "Deambulación"
        self.EB_STAIRS = "Subir y bajar escaleras"
        self.EB_MENTAL_STATE = "Estado mental"
        self.EB_ORIENTED = "Orientado"
        self.EB_DISORIENTED = "Desorientado, apático o pasivo"
        self.EB_LET = "Letárgico o hipercinético"
        self.EB_UNC = "Comatoso, inconsciente"
        self.EB_MOBILITY = "Mobilidad"
        self.EB_COMP = "Completa"
        self.EB_LIT_LIM = "Ligeramente limitada"
        self.EB_IMP_LIM = "Limitación importante"
        self.EB_IMM = "Inmóvil"
        self.EB_HUM = "Humidad R/C, Incontinencia"
        self.EB_OCC = "Urinária o fecal ocasional"
        self.EB_HAB = "Urinária o fecal habitual"
        self.EB_BOTH = "Urinária y fecal, ambas"
        self.EB_NUT = "Nutrición"
        self.EB_CORR = "Correcta"
        self.EB_OCC_UNC = "Ocasionalmente Incompleta"
        self.EB_UNC = "Incompleta"
        self.EB_NO = "No ingiere"
        self.EB_ACT = "Actividad"
        self.EB_DMB = "Deambula"
        self.EB_HLP_DMB = "Deambula con ayuda"
        self.EB_ALWS_HLP= "Siempre requiere de ayuda"
        self.EB_NO_DMB = "No deambula"
        self.EB_TXT = "Introducir texto"

        #MODEL VIEWER MANAGER
        self.VM_title = "Evolución de la herida"
        self.VM_id = "Id paciente: "
        self.VM_location = "Localización herida: "
        self.VM_cm = "cm"
        self.VM_perimeter_title = "Perímetro total"
        self.VM_perimeter_area = "Área total"
        self.VM_granulation = "Área tejido granuloso"
        self.VM_slough = "Área tejido esfacelo"
        self.VM_necrosis = "Área tejido necrótico"

        #VIEW PAGE
        self.VP_CON_DDBB = "Consultar base de datos"
        self.VP_PAC_ID = "Id paciente: "
        self.VP_LOC = "Localización: "
        self.VP_DATE = "Fecha: "
        self.VP_EVO = "Ver evolución"
        self.VP_IMG_LABEL = "<Doble clic para cargar un elemento de la lista>"
        self.VP_CODE = "Código: "
        self.VP_GRADE = "Grado: "

        #VIEW SETUP
        self.VS_AT = "Atención"
        self.VS_MSG = "Proceso finalizado con éxito. Pulsa OK para continuar."

        #VIEW SEG GUI
        self.SG_WB = "Corrección Balance de Blancos"
        self.SG_WARNING = "Atención: método en desarrollo. Supervisa el resultado: "
        self.SG_DESC = "Imagen original // Imagen balanceada"
        self.SG_TITLE = "Confirmar región"
        self.SG_CONF = "Es correcta la región seleccionada?"
        self.SG_ZONE_TITLE = "Tipo de zona"
        self.SG_ZONE = "Selecciona el tipo de zona:"
        self.SG_RING = "Anilla"
        self.SG_CLOSED = "Cerrada"
        self.SG_PER_EXT = "Perímetro exterior"
        self.SG_TISSUE = "Tejido "
        self.SG_SEL_EXT = " : selecciona el perímetro exterior de la región"
        self.SG_EXT = "Exterior"
        self.SG_PER_INT = "Perímetro interior"
        self.SG_SEL_INT = " : selecciona el perímetro interior de la región"
        self.SG_INT = "Interior"
        self.SG_PER_SEL = "Perímetro seleccionado"