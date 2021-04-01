from pubsub import pub
from View import V_Setup
from Model.M_PressureImage import Pressure_img
from Controller import C_Metadata, C_ImagePreSegmentation, C_ImageSegmentation
from Model import M_MetadataManager, M_ImageReader, M_FileDataManager
from Controller import C_LanguageSelection
import tkinter as tk
import ctypes
class ControllerSetup:
    def __init__(self, parent, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.parent = parent
        self.pressure_img = None

        pub.subscribe(self.setup_lang_asked, "LANG_OK_ASKED")
        pub.subscribe(self.setup_lang_loaded, "LANG_OK_LOADED")

        pub.subscribe(self.button_1_pressed, "BUTTON_1_PRESSED")
        pub.subscribe(self.button_2_pressed, "BUTTON_2_PRESSED")
        pub.subscribe(self.button_3_pressed, "BUTTON_3_PRESSED")
        pub.subscribe(self.load_image, "LOAD_IMAGE")
        pub.subscribe(self.image_loaded, "IMAGE_LOADED")

        pub.subscribe(self.image_accepted, "IMG_ACCEPTED")

        pub.subscribe(self.tot_ple_ko, "TOT_PLE_KO")
        pub.subscribe(self.data_ko, "DATA_KO")
        pub.subscribe(self.data_ok, "DATA_OK")

        pub.subscribe(self.data_files_ko, "DATA_FILES_KO")
        pub.subscribe(self.data_n_elements, "DATA_N_ELEMENTS")

        pub.subscribe(self.ask_image_i, "ASK_IMAGE_i")
        pub.subscribe(self.load_image_i, "IMAGE_LOAD_i")
        pub.subscribe(self.load_metadata_i, "METADATA_LOAD_i")

        self.language_manager = C_LanguageSelection.LanguageSelection(self.parent)


    def setup_lang_asked(self, lang):
        self.parent.destroy()
        self.parent = tk.Tk()
        self.parent.title("PIIA")
        self.parent.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

        self.model_reader = M_ImageReader.ImageReader()
        self.model_metadata = M_MetadataManager.MetadataManager()
        self.view = V_Setup.ViewSetup(self.parent, lang)
        self.metadata = C_Metadata.ControllerMetadata(self.model_metadata, self.view)
        self.file_data_manager = M_FileDataManager.FileDataManager()
        self.img_pre_segmentation = C_ImagePreSegmentation.ControllerImagePreSegmentation(self.view)
        self.img_segmentation = C_ImageSegmentation.ControllerImageSegmentation(self.view)
        self.parent.mainloop()

    def setup_lang_loaded(self, lang):
        self.model_reader = M_ImageReader.ImageReader()
        self.model_metadata = M_MetadataManager.MetadataManager()
        self.view = V_Setup.ViewSetup(self.parent, lang)
        self.metadata = C_Metadata.ControllerMetadata(self.model_metadata, self.view)
        self.file_data_manager = M_FileDataManager.FileDataManager()
        self.img_pre_segmentation = C_ImagePreSegmentation.ControllerImagePreSegmentation(self.view)
        self.img_segmentation = C_ImageSegmentation.ControllerImageSegmentation(self.view)

    def button_1_pressed(self):
        """
        Prints that button_1 from view has been pressed.
        """

        print("controller - Botó 1!")

    def button_2_pressed(self):
        """
        Prints that button_2 from view has been pressed and calls the function.
        load_data from Data_manager.
        """

        print("MVC controller - Botó 2!")
        self.file_data_manager.load_data()

    def button_3_pressed(self, data):
        """
        Prints that button_3 from view has been pressed.
        Calls the functions to check metadata and images before saving.
        Parameters
        ----------
        data : list
           a list with all the metadata field's information written by the user
        """

        print("controller - Botó 3!")
        try:
            if self.pressure_img.loaded:
                if self.pressure_img.processed:
                    self.file_data_manager.load_data()
                    self.model_metadata.getData(data)
                else:
                    self.view.popupmsg("És necessari processar la imatge.")
            else:
                self.view.popupmsg("És necessari carregar una imatge")
        except:
            self.view.popupmsg("És necessari carregar una imatge")

    def load_image(self):
        """
        Calls the function to load a pressure injury's image.
        WARNING: For optimal visualization, images must be '560x390'
        """

        print("MVC controller - load imatge")
        self.model_reader.carregar_imatge()

    def image_loaded(self, image_original, image_tk):
        """
        Defines a Pressure_img object and saves its image.
        Calls the update_image from View to update the label with the loaded image.
        Calls the function from View to show "process" button.
        Parameters
        ----------
        image_tk : PIL Image
           image ready to be loaded in a label
        """
        pressure_img = Pressure_img()
        self.pressure_img = pressure_img
        self.pressure_img.img_origin = image_original
        self.pressure_img.loaded = True
        self.view.processing_page.update_image(image_tk)
        self.view.processing_page.botoImg()
        self.img_pre_segmentation.pressure_img = self.pressure_img
        self.img_segmentation.pressure_img = self.pressure_img

    def image_accepted(self):
        """
        Updates Pressure_img processed boolean to True.
        """

        print("controller - image_accepted!")
        self.pressure_img.close_all()
        self.view.processing_page.update_main_label(self.pressure_img.mask)
        self.pressure_img.processed = True

    def tot_ple_ko(self):
        """
        Calls a View function to warn the user that all metadata fields must be filled.
        """

        print("controller - tot_ple_ko!")
        self.view.popupmsg("S'han d'omplir tots els camps")
    def data_ko(self, error):
        """
        Calls a View function to warn the user what field has the wrong input data.
        Parameters
        ----------
        error : list
           wrong input data field's name
        """

        self.view.processing_page.show_error(error)
        print("controller - data_ko")

    def data_ok(self):
        """
        Sets Pressure_img loaded boolean to False.
        Calls View function to reset loaded image label.
        Calls the function to save all the data entered by the user.
        """

        print("controller - data_ok")
        self.pressure_img.loaded = False
        self.view.processing_page.reset_view()
        try:
            self.file_data_manager.save_data(self.model_metadata.metadata, self.pressure_img)
            self.view.popupmsg("Procés finalitzat amb èxit. Prem OK per continuar.")
        except:
            self.view.popupmsg("Error de gestió de fitxers.")

    def data_files_ko(self):
        """
        Calls the View function to warn the user about a file manager error.
        """

        print("controller - data_files_ko")
        self.view.popupmsg("Error de gestió dels fitxers.")

    def data_n_elements(self, num):
        """
        Calls the View function to update the element's label counter with a new value.
        Parameters
        ----------
        num : int
           number of images found in the storage directory
        """

        print("controller - data_n_elements")
        self.view.view_page.update_data_n_elements(num)

    def ask_image_i(self, i):
        """
        Calls the Data_manager functions to read and load the image and metadata "i".
        Parameters
        ----------
        i : int
           id of the image and metadata that have to be read
        """

        print("controller - ask_img_i")
        self.file_data_manager.load_img_i(i)
        self.file_data_manager.load_metadata_i(i)

    def load_image_i(self, img_tk):
        """
        Calls the View function to load the image_tk to the p2_label_img.
        Parameters
        ----------
        img_tk : PIL Image
           image ready to be loaded to a label
        """

        print("controller - load_img_i")
        self.view.view_page.load_image_i(img_tk)

    def load_metadata_i(self, metadata):
        """
        Calls the View function to load the metadata to the p2_label_metadata.
        Parameters
        ----------
        metadata : JSON Object
           data sent to be loaded into a label
        """

        print("controller - load_metadata_i")
        self.view.view_page.load_metadata_i(metadata)