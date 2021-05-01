"""Pressure injury image class
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>
Class to manage the pressure injurie's images.
Its stucture allows to process the user's selected images and masks.
"""

import cv2
import numpy as np
from peakdetect import peakdetect
from pubsub import pub

from resources import language_CAST, language_ENG, language_CAT
from Model.M_TargetDetector import TargetDetector


class Pressure_img:
    """
    A class with the pressure injury image class structure
    ...
    Attributes
    ----------
    img_origin : image cv2
        original uploaded image.
    img : image cv2
        sub region of the original uploaded image.
    mask : image cv2
        processed mask of the original uploaded image.
    perimetre_done : bool
        boolean to check if perimeter has been cropped.
    perimetre : image cv2
        sub image with the perimeter selected by user.
    granulation : image cv2
        sub image with the granulation tissue selected by user.
    slough : image cv2
        sub image with the slough tissue selected by user.
    necrosis : image cv2
        sub image with the necrosis tissue selected by user.
    flash_reduced : bool
        boolean to check if flash has been reduced.
    processed : bool
        boolean to check if image has been processed.
    path : String
        path to the image's directory
    loaded : bool
        boolean to check if image has been loaded.
    Methods
    -------
    crop_image(path)
        Allows user to crop the image with a rectangular shape.
    close_all()
        Closes all cv2 windows.
    scale_image(img, scale_percent)
        Resize the img with the scale factor given.
    begin_segmentation(img_imgtk_mask, img_cv2_mask, scale_factor)
        Updates and scales sub image mask. Sends a request for segmentation.
    save_mask_data(img_cv2_roi, tissue)
        Updates Pressure_img structure of the given tissue.
    roi_crop(im, tissue)
       Calls the Point class and functions to let the user
        select a free shape roi with the mouse.
    """

    def __init__(self, parent, lang):
        self.parent = parent
        self.lang = lang
        self.img_origin = None
        self.img = None
        self.mask = None
        self.previous_roi = None
        self.perimetre_done = False
        self.perimetre_total_cm = 0
        self.area_aux_cm = 0
        self.area_cm = 0
        self.area_aux_cm = 0
        self.area_total_cm = 0
        self.area_granulation_cm = 0
        self.area_slough_cm = 0
        self.area_necrosis_cm = 0
        self.perimetre = None
        self.granulation = []
        self.slough = []
        self.necrosis = []
        self.whitebalanced = False
        self.processed = False
        self.path = None
        self.loaded = False
        self.target_detector = None
        self.ring_ext = None
        self.ring_int = None
        if self.lang == 0:
            self.lang = language_CAT.LangCAT()
        if self.lang == 1:
            self.lang = language_CAST.LangCAST()
        if self.lang == 2:
            self.lang = language_ENG.LangENG()
        return

    def crop_image(self, im):
        """
        Allows user to crop the image with a rectangular shape.
        Parameters
        ----------
        im : cv2 image bgr
            path to the image's directory
        """
        # Select ROI
        showCrosshair = False
        fromCenter = False
        r = cv2.selectROI(self.lang.MODEL_PRESSURE_IMG, im, showCrosshair, fromCenter)
        # Crop image
        img_cv2_mask = im[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
        # img_cv2_mask = im
        # Ask user for confirmation
        pub.sendMessage("ASK_MASK_CONFIRMATION", img_cv2_mask=img_cv2_mask, scale_factor=100)

    def close_all(self):
        """
         Closes all cv2 windows.
        """
        cv2.destroyWindow("Image")
        cv2.destroyWindow("Segmentation")
        cv2.destroyAllWindows()

    def scale_image(self, img, scale_percent):
        """
        Resize the img with the scale factor given (default = 100)
        Parameters
        ----------
        img : opencv.Image
            ulcer's image
        scale_percent: int
            value of the resize scale (default = 100)
        """

        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized

    def begin_segmentation(self, img_imgtk_mask, img_cv2_mask, scale_factor):
        """
        Updates and scales sub image mask. Sends a request for segmentation.
        Parameters
        ----------
        img_imgtk_mask : PIL Image
            image ready to be loaded to a label
        img_cv2_mask : image cv2
            image that will be processed
        scale_factor: int
            value of the resize scale (default = 100)
        """
        # Save image to class atributte
        self.img = img_cv2_mask
        # Scale image
        img_cv2_mask = self.scale_image(img_cv2_mask, scale_factor)
        # Create GUI
        self.target_detector = TargetDetector(img_cv2_mask)
        pub.sendMessage("SEGMENTATION_GUI", img_imgtk_mask=img_imgtk_mask, img_cv2_mask=img_cv2_mask)

    def save_mask_data(self, img_cv2_roi, tissue):
        """
        Updates Pressure_img structure of the given tissue.
        Request to update View's tissues labels.
        Parameters
        ----------
        img_cv2_roi : image cv2
            processed img that will be stored to the object structure
        tissue : String
            tissue of the roi
        """

        img_cv2_roi = cv2.cvtColor(img_cv2_roi, cv2.COLOR_BGR2RGB)
        if (tissue == "Perimeter"):
            self.perimetre = img_cv2_roi
            self.perimetre_done = True
            pub.sendMessage("UPDATE_PERIMETER_COUNT")
        elif (tissue == "Granulation"):
            self.area_granulation_cm += round(self.area_aux_cm, 2)
            self.granulation.append(img_cv2_roi)
            pub.sendMessage("UPDATE_GRANULATION_COUNT", number=len(self.granulation))
        elif (tissue == "Necrosis"):
            self.area_necrosis_cm += round(self.area_aux_cm, 2)
            self.necrosis.append(img_cv2_roi)
            pub.sendMessage("UPDATE_NECROSIS_COUNT", number=len(self.necrosis))
        elif (tissue == "Slough"):
            self.area_slough_cm += round(self.area_aux_cm, 2)
            self.slough.append(img_cv2_roi)
            pub.sendMessage("UPDATE_SLOUGH_COUNT", number=len(self.slough))

    def roi_crop(self, im, tissue, *args):

        """Tool used to allow user select a free shape roi with the mouse
        """

        if (tissue == "Perimeter"):
            self.previous_roi = im.copy()
        if len(args) == 0:
            self.previous_roi = im.copy()
        for ar in args:
            if ar == 2:
                pass
            else:
                self.previous_roi = im.copy()

        class Point:
            """
           Class that allows the free shape cropping with its methods and attributes.
           ...
           Attributes
           ----------
           x : int
               x coordinates's value of image window.
           y : int
               y coordinates's value of image window.
           Methods
           -------
           draw(event, former_x, former_y, flags, param)
               Listens mouse events and saves its coordinates as Points.
           assemble_mask(mask_points)
               Storages all Points selected by user in a list of Points.
           roi(img, vertices)
               Isolates a sub region as a roi using the image and the list of Points.
           """

            def __init__(self, x, y):
                self.x = x
                self.y = y

        color = (255, 255, 255)
        thickness = 4

        # Dibuixar a la imatge
        global drawing
        drawing = False  # true if mouse is pressed
        global mode
        mode = True  # if True, draw rectangle. Press 'm' to toggle to curve

        # mouse callback function
        def draw(event, former_x, former_y, flags, param):
            """
            Listens mouse events and saves its coordinates as Points.
            Parameters
            ----------
            event : int
                event listened.
            former_x : int
                x coordinates's value of image window.
            former_y : int
               y coordinates's value of image window.
            flags : int
                no flags used
            param : list
                list of all selected coordinates as Points
            """

            global current_former_x, current_former_y, drawing, mode, first_x, first_y
            # Apretar el ratoí
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                current_former_x, current_former_y = former_x, former_y
                first_x = current_former_x
                first_y = current_former_y
            # Moure el ratolí
            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing == True:
                    if mode == True:
                        cv2.line(im, (current_former_x, current_former_y), (former_x, former_y), [0, 0, 0], thickness)
                        current_former_x = former_x
                        current_former_y = former_y
                        point = Point(former_x, former_y)
                        mask_points.append(point)

            # Stop clicking
            elif event == cv2.EVENT_LBUTTONUP:
                punts = assemble_mask(mask_points)
                cv2.line(im, (current_former_x, current_former_y), (first_x, first_y), [0, 0, 0], thickness)
                drawing = False
                if mode == True:
                    cv2.line(im, (current_former_x, current_former_y), (former_x, former_y), [0, 0, 0], thickness)
                    current_former_x = former_x
                    current_former_y = former_y
                roi(self.img, punts)
                # roi(im, punts)

        mask_points = []

        def assemble_mask(mask_points):
            """
            Storages all Points selected by user in a list of Points.
            Parameters
            ----------
            mask_points : int
                list of all selected coordinates as Points
            """

            x_ok = False
            y_ok = False
            mask_x = []
            mask_y = []
            punts = []
            for k in range(len(mask_points)):
                mask_x.append(mask_points[k].x)
                mask_y.append(mask_points[k].y)
                punts.append([mask_points[k].x, mask_points[k].y])
            return punts

        def roi(img, vertices):
            """
            Isolates a sub region as a roi using the image and the list of Points.
            Parameters
            ----------
            img : image cv2
                image used to select the roi
            vertices : list
                list of all selected coordinates as Points.
            """

            # blank mask:
            mask = np.zeros_like(img)
            a3 = np.array([vertices], dtype=np.int32)
            # filling pixels inside the polygon defined by "vertices" with the fill color
            cv2.fillPoly(mask, a3, [255, 255, 255])
            # returning the image only where mask pixels are nonzero
            masked = cv2.bitwise_and(img, mask)
            gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
            px_area = cv2.countNonZero(gray)
            self.area_cm = px_area * self.target_detector.px_dist * self.target_detector.px_dist
            for ar in args:
                if ar == 2:
                    #Zona anella
                    self.area_cm = self.area_aux_cm - self.area_cm
            self.area_aux_cm = self.area_cm.copy()
            print("Àrea: ", round(self.area_cm, 2), " cm^2")
            px_perimeter = a3.shape[1]
            print("Perímetre zona seleccionada: ", (round(px_perimeter * self.target_detector.px_dist, 2)), " cm")
            for ar in args:
                if ar == 1:
                    pub.sendMessage("ASK_ROI_CONFIRMATION", img_cv2_mask=img, img_cv2_roi=masked, tissue=tissue,
                                    scale_factor=100, ring=1)
                    return masked
                else:
                    #Anella interior
                    sub = cv2.subtract(self.ring_ext, masked)
                    pub.sendMessage("ASK_ROI_CONFIRMATION", img_cv2_mask=img, img_cv2_roi=sub, tissue=tissue,
                                    scale_factor=100, ring=2)
                    return masked
            if (tissue == "Perimeter"):
                cm_perimeter_total = px_perimeter * self.target_detector.px_dist
                cm_perimeter_total = round(cm_perimeter_total, 2)
                self.perimetre_total_cm = cm_perimeter_total
                self.area_cm = cm_perimeter_total * self.target_detector.px_dist
                self.area_total_cm = round(self.area_cm, 2)
            if (tissue == "Granulation"):
                cm_area_granulation = round(self.area_cm, 2)
                self.area_cm = cm_area_granulation
            if (tissue == "Slough"):
                cm_area_slough = round(self.area_cm, 2)
                self.area_cm = cm_area_slough
            if (tissue == "Necrosis"):
                cm_area_necrosis = round(self.area_cm, 2)
                self.area_cm = cm_area_necrosis
            pub.sendMessage("ASK_ROI_CONFIRMATION", img_cv2_mask=img, img_cv2_roi=masked, tissue=tissue,
                            scale_factor=100, ring=0)
            # cv2.imshow(tissue+"Tissue", masked)
            #cv2.imwrite("area.jpg", area)
            return masked

        height, width, channel = im.shape
        cv2.namedWindow("Segmentation")
        cv2.setMouseCallback("Segmentation", draw, param=mask_points)
        while (1):
            cv2.imshow("Segmentation", im)
            k = cv2.waitKey(1) & 0xFF
            try:
                aux= self.parent.winfo_exists()
            except:
                break

            if k == 27:
                break