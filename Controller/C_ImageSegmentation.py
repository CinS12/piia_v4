import cv2
from pubsub import pub


class ControllerImageSegmentation:
    def __init__(self, view):
        self.view = view
        self.pressure_img = None

        pub.subscribe(self.segmentation_gui, "SEGMENTATION_GUI")
        pub.subscribe(self.whitebalance, "WHITEBALANCE")
        pub.subscribe(self.whitebalance_confirmated, "WHITEBALANCE_CONFIRMATED")
        pub.subscribe(self.ask_perimeter, "ASK_PERIMETER")

        pub.subscribe(self.target_not_found, "TARGET_NOT_FOUND")

        pub.subscribe(self.ask_roi_confirmation, "ASK_ROI_CONFIRMATION")

        pub.subscribe(self.roi_granulation, "ROI_GRANULATION")
        pub.subscribe(self.roi_necrosis, "ROI_NECROSIS")
        pub.subscribe(self.roi_slough, "ROI_SLOUGH")

        pub.subscribe(self.closed_zone, "CLOSED_ZONE")
        pub.subscribe(self.ring_zone, "RING_ZONE")
        pub.subscribe(self.ring_ext, "RING_EXT")
        pub.subscribe(self.ring_int, "RING_INT")
        pub.subscribe(self.roi_confirmated, "ROI_CONFIRMATED")

        pub.subscribe(self.roi_ko, "ROI_KO")
        return

    def segmentation_gui(self, img_imgtk_mask, img_cv2_mask):
        """
        Updates the Pressure_img mask image, calls the target_detection process and calls the View UI for processing.
        Parameters
        ----------
        img_imgtk_mask : PIL Image BGR
           image before cropping roi
        img_cv2_mask : image cv2 BGR
           image that requires user confirmation
        """
        print("controller - segmentation_gui!")
        self.pressure_img.close_all()
        self.pressure_img.mask = img_cv2_mask
        self.pressure_img.previous_roi = img_cv2_mask.copy()
        self.view.processing_gui.segmentation_gui(img_imgtk_mask, img_cv2_mask)

    def whitebalance(self, img_cv2_mask):
        """
        Checks if flash reduction has been called and calls
        Pressure_img function to reduce flash if not.
        Calls the View function to ask user confirmation.
        Parameters
        ----------
        img_cv2_mask : image cv2
           image selected by user to reduce its flash
        """

        print("controller - whitebalance!")
        if self.pressure_img.whitebalanced == False:
                img_whitebalanced = self.pressure_img.target_detector.whiteBalance()
                self.view.processing_gui.ask_whitebalance_confirmation(img_cv2_mask, img_whitebalanced)
        else:
            self.view.popupmsg("Ja s'ha aplicat la reducció.")

    def whitebalance_confirmated(self, img_cv2_whitebalanced):
        """
        Updates Pressure_img mask and flash_reduced boolean.
        Calls the View function to update image label.
        Parameters
        ----------
        img_cv2_mask : image cv2
           image selected and validated by user to reduce its flash
        """

        print("controller - whitebalance_confirmated!")
        self.pressure_img.whitebalanced = True
        self.pressure_img.mask = img_cv2_whitebalanced
        self.pressure_img.img = img_cv2_whitebalanced.copy()
        self.view.processing_gui.update_whitebalanced_label(img_cv2_whitebalanced)

    def ask_perimeter(self):
        """
        Checks if perimeter has been cropped and calls the Pressure_img function if not.
        """

        print("controller - ask_perimeter!")
        img_cv2_mask = self.pressure_img.mask
        if self.pressure_img.perimetre_done:
            self.view.popupmsg("El perímetre ja ha estat seleccionat")
        else:
            self.pressure_img.roi_crop(img_cv2_mask, "Perimeter")

    def target_not_found(self):
        print("controller - target_not_found")
        self.view.popupmsg("Atenció. No s'ha trobat el target!")

    def ask_roi_confirmation(self, img_cv2_mask, img_cv2_roi, tissue, scale_factor, px_perimeter, ring):
        """
        Calls the View function to ask user confirmation about a image's roi.
        Parameters
        ----------
        img_cv2_mask : image cv2
           image before cropping roi
        img_cv2_roi : image cv2
           image that requires user confirmation
        tissue : String
            tissue of the roi
        scale_factor : int
           image resize value (default = 100)
        """
        print("controller - ask_roi_confirmation!")
        self.pressure_img.close_all()
        #try:
        cm_perimeter = px_perimeter * self.pressure_img.target_detector.px_dist
        print("Perímetre zona seleccionada: ",cm_perimeter)
        self.view.processing_gui.ask_roi_confirmation(img_cv2_mask, img_cv2_roi, tissue, scale_factor, ring)
        #except:
            #self.view.popupmsg("Alguna cosa ha fallat. Torna-ho a intentar!")

    def roi_granulation(self):
        """
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the granulation roi.
        """

        print("controller - roi_granulation!")
        self.view.processing_gui.ask_zone_type("Granulation")

    def roi_necrosis(self):
        """
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the necrosis roi.
        """

        print("controller - roi_necrosis!")
        self.view.processing_gui.ask_zone_type("Necrosis")

    def roi_slough(self):
        """
        Updates the Pressure_img mask image
        Calls the Pressure_img function to allow the user to select the slough roi.
        """
        print("controller - roi_slough!")
        self.view.processing_gui.ask_zone_type("Slough")

    def closed_zone(self, tissue):
        img_cv2_mask = self.pressure_img.mask
        self.pressure_img.roi_crop(img_cv2_mask, tissue)

    def ring_zone(self, tissue):
        print("controller - ring_zone!")
        self.view.processing_gui.ask_ring_out(tissue)

    def ring_ext(self, tissue):
        print("controller - ring_ext!")
        img_cv2_mask = self.pressure_img.mask
        self.pressure_img.roi_crop(img_cv2_mask, tissue, 1)

    def ring_int(self, tissue):
        print("controller - ring_int!")
        img_cv2_mask = self.pressure_img.ring_ext
        self.pressure_img.roi_crop(img_cv2_mask, tissue, 2)

    def roi_confirmated(self, img_cv2_roi, tissue, ring):
        """
        Calls the Pressure_img function to update granulation/necrosis/slough fields.
        Parameters
        ----------
        img_cv2_roi : image cv2
           roi selected by the user
        tissue : String
            tissue of the roi
        """
        print("controller - roi_confirmated!")
        #self.view.processing_gui.updateLabelGUI(self.pressure_img.mask)
        if(ring == 0):
            #Zona tancada
            self.view.processing_gui.updateLabelGUI(self.pressure_img.mask)
            self.pressure_img.save_mask_data(img_cv2_roi, tissue)
        if(ring==1):
            #Anella ext
            print("Anella exterior")
            self.pressure_img.ring_ext = img_cv2_roi
            self.view.processing_gui.ask_ring_in(tissue)
        if(ring==2):
            self.view.processing_gui.updateLabelGUI(self.pressure_img.mask)
            #Anella interna
            print("Anella interior")
            #self.pressure_img.mask = self.pressure_img.previous_roi
            self.pressure_img.ring_int = img_cv2_roi
            self.pressure_img.save_mask_data(img_cv2_roi, tissue)
            #Guardar imatge

    def roi_ko(self):
        self.pressure_img.mask = self.pressure_img.previous_roi