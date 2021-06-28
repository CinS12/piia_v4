"""Pre segmentation class
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

Class to manage the pre-segmentation process.
"""
from pubsub import pub
from Model import M_ViewerManager
from resources import language_CAST, language_ENG, language_CAT


class ControllerImagePreSegmentation:
    """
    Class to see the ulcer's state and evolution.
    ...
    Attributes
    ----------
    view : ViewSetup
        view manager
    file_data_manager : FileDataManager
        methods to read and update files
    lang : String
        language id
    pressure_img : Pressure_img
        ulcer's image
    ulcer_location : String
        location of the ulcer
    is_new_ulcer : bool
        tells if ulcer is already registered
    is_new_patient : bool
        tells is patient is already registered
    Methods
    -------
    analyse_image()
        Checks if Pressure_img has been processed and calls processing function if not.
    ask_mask_confirmation(img_cv2_mask, scale_factor)
        Calls the View function to ask user confirmation about an image's mask.
    pre_segmentation_confirmated(img_imgtk_mask, img_cv2_mask)
        Calls the Pressure_img function for the first image segmentation.
    check_code_request(code)
        Loads the language file based on user's selection.
    code_checked(existence, code)
        Proceeds with the data saving based on the patient's existence on the database.
    new_code_location(location, new_patient, code)
        Calls the process to register a new ulcer.
    old_code_location(location, code)
        Calls the process to add a new picture of a registered ulcer.
    patient_selected(id)
        Gets all ulcers locations from a patient.
    location_selected(id, location)
        Gets all images dates from a selected ulcer (location).
    date_selected(id, location, dir)
        Executes the process to load a picture and its metadata.
    evo_selected(id, location)
        Executes the process to show the tissues evolution.
    """
    def __init__(self, view, file_data_manager, lang):
        self.view = view
        self.file_data_manager = file_data_manager
        self.lang = lang
        self.is_checked = False
        if self.lang == 0:
            self.lang = language_CAT.LangCAT()
        if self.lang == 1:
            self.lang = language_CAST.LangCAST()
        if self.lang == 2:
            self.lang = language_ENG.LangENG()
        self.pressure_img = None
        self.ulcer_location = None
        self.is_new_ulcer = None
        self.is_new_patient = None
        self.code = None
        pub.subscribe(self.analyse_image, "ANALYSE_IMAGE")
        pub.subscribe(self.ask_mask_confirmation, "ASK_MASK_CONFIRMATION")
        pub.subscribe(self.pre_segmentation_confirmated, "PRE_SEGMENTATION_CONFIRMATED")
        pub.subscribe(self.check_code_request, "CHECK_CODE_REQUEST")
        pub.subscribe(self.code_checked, "CODE_CHECKED")
        pub.subscribe(self.new_code_location, "NEW_CODE_LOCATION")
        pub.subscribe(self.old_code_location, "OLD_CODE_LOCATION")
        pub.subscribe(self.patient_selected, "PATIENT_SELECTED")
        pub.subscribe(self.location_selected, "LOCATION_SELECTED")
        pub.subscribe(self.date_selected, "DATE_SELECTED")
        pub.subscribe(self.evo_selected, "EVO_SELECTED")

    def analyse_image(self):
        """
        Checks if Pressure_img has been processed and calls processing function if not.
        """
        print("MVC controller - analyse_image!")
        if self.pressure_img.processed == False:
            self.pressure_img.crop_image(self.pressure_img.img_origin)
        else:
            self.view.popupmsg("La imatge ja ha estat processada.")

    def ask_mask_confirmation(self, img_cv2_mask, scale_factor):
        """
        Calls the View function to ask user confirmation about an image's mask.
        Parameters
        ----------
        img_cv2_mask : image cv2
           image that requires user confirmation
        scale_factor : int
           image resize value (default = 100)
        """

        print("MVC controller - ask_mask_confirmation!")
        try:
            self.view.pre_processing_gui.ask_mask_confirmation(img_cv2_mask, scale_factor)
        except:
            self.view.popupmsg("Alguna cosa ha fallat. Torna-ho a intentar!")

    def pre_segmentation_confirmated(self, img_imgtk_mask, img_cv2_mask):
        """
        Calls the Pressure_img function for the first image segmentation.
        Parameters
        ----------
        img_imgtk_mask : PIL Image
           image before cropping roi
        img_cv2_mask : image cv2
           image that requires user confirmation
        """
        print("controller - pre_segmentation_confirmated!")
        scale_factor = 100
        self.pressure_img.begin_segmentation(img_imgtk_mask=img_imgtk_mask, img_cv2_mask=img_cv2_mask, scale_factor= scale_factor)

    def check_code_request(self, code):
        """
        Loads the language file based on user's selection.
        Parameters
        ----------
        code : int
           file id
        """
        if self.lang == 0:
            self.lang = language_CAT.LangCAT()
        if self.lang == 1:
            self.lang = language_CAST.LangCAST()
        if self.lang == 2:
            self.lang = language_ENG.LangENG()
        if code != "":
            self.file_data_manager.check_code(code)
        else:
            self.view.popupmsg(self.lang.META_EMPTY_CODE)

    def code_checked(self, existence, code):
        """
        Proceeds with the data saving based on the patient's existence on the database.
        Parameters
        ----------
        existence : bool
           tells if patient is already registered
        code : String
            patient's code
        """
        if existence:
            saved_metadata = self.file_data_manager.get_saved_metadata(code)
            self.view.processing_page.load_saved_data(saved_metadata)
            locations = self.file_data_manager.get_locations(code)
            self.view.pre_processing_gui.popup_ask_code(code, locations)
        else:
            self.view.pre_processing_gui.popup_new_code(code)

    def new_code_location(self, location, new_patient, code):
        """
        Calls the process to register a new ulcer.
        Parameters
        ----------
        location : String
           ulcer's location
        new_patient : bool
            tells if the patient is already registered
        code : String
            patient's code
        """
        print("Nova ferida a: ", location)
        code_location_ok = True
        if new_patient == False:
            code_location_ok = self.file_data_manager.check_code_location(code, location)
        if code_location_ok:
            self.ulcer_location = location
            self.is_new_ulcer = True
            self.is_new_patient = new_patient
            self.is_checked = True
            self.code = code
        else:
            self.view.popupmsg(self.lang.PRE_LOCATION_REPEATED)

    def old_code_location(self, location, code):
        """
        Calls the process to add a new picture of a registered ulcer.
        Parameters
        ----------
        location : String
           ulcer's location
        code : String
            patient's code
        """
        print("Nova foto de: ", location)
        self.ulcer_location = location
        self.is_new_ulcer = False
        self.is_new_patient = False
        self.is_checked = True
        self.code = code

    def patient_selected(self, id):
        """
        Gets all ulcers locations from a patient.
        Parameters
        ----------
        id : String
            patient's code
        """
        locations = self.file_data_manager.get_locations(id)
        self.view.view_page.update_locations(id, locations)

    def location_selected(self, id, location):
        """
        Gets all images dates from a selected ulcer (location).
        Parameters
        ----------
        id : String
            patient's code
        location : String
           ulcer's location
        """
        dates = self.file_data_manager.get_dates(id, location)
        self.view.view_page.update_dates(id, location, dates)
        self.view.view_page.evo_button.pack()

    def date_selected(self, id, location, dir):
        """
        Executes the process to load a picture and its metadata.
        Parameters
        ----------
        id : String
            patient's code
        location : String
           ulcer's location
        dir : int
            data directory
        """
        self.file_data_manager.load_img_i(id, location, dir)
        metadata = self.file_data_manager.load_metadata(id, location, dir)
        self.view.view_page.load_metadata_i(metadata)

    def evo_selected(self, id, location):
        """
        Executes the process to show the tissues evolution.
        Parameters
        ----------
        id : String
            patient's code
        location : String
           ulcer's location
        """
        evo_data = self.file_data_manager.get_evo_data(id, location)
        M_ViewerManager.ViewerManager(evo_data, self.lang)