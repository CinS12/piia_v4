from pubsub import pub
import language_CAST
import language_CAT
import language_ENG
class ControllerImagePreSegmentation:

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
        if existence:
            locations = self.file_data_manager.get_locations(code)
            self.view.pre_processing_gui.popup_ask_code(code, locations)
        else:
            self.view.pre_processing_gui.popup_new_code(code)

    def new_code_location(self, location, new_patient, code):
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
        print("Nova foto de: ", location)
        self.ulcer_location = location
        self.is_new_ulcer = False
        self.is_new_patient = False
        self.is_checked = True
        self.code = code