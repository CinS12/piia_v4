from tkinter import filedialog
import cv2
from PIL import ImageTk
from pubsub import pub

class ImageReader:
    """
    Class responsible for managing the data of the application.
    It receives user input from the controller.
    ...
    Attributes
    ----------
    metadata : list
        user data inputs from all metadata fields
    Methods
    -------
    carregar_imatge()
        File dialog to ask user for an image. Calls the functions to check img size.
        Sends a request to the Controller with the PIL image read.
    check_img_size(img)
        Checks if image has too much resolution. Calls the function to resize if needed.
    resize_img(self, img, scale_percent)
        Resizes the img according to the scale_percent.
    """

    def __init__(self):
        self.image_size_ok = False
        self.img = None
        return

    def carregar_imatge(self):
        """
        File dialog to ask user for an image. Calls the functions to check img size.
        Sends a request to the Controller with the PIL image read.
        WARNING: For optimal visualization, images must be '560x390'
        """
        self.image_size_ok = False
        path = 0
        path = filedialog.askopenfilename()
        if len(path) > 0:
            img_original = cv2.imread(path, cv2.IMREAD_COLOR)
            while (self.image_size_ok == False):
                img_original = self.check_img_size(img_original)
            #print("Original size: ", img_original.shape)
            # Rearrange the color channel
            b, g, r = cv2.split(img_original)
            self.img = cv2.merge((r, g, b))
            self.im_p1 = ImageTk.Image.fromarray(self.img)
            self.imgtk_p1 = ImageTk.PhotoImage(image=self.im_p1)
            pub.sendMessage("IMAGE_LOADED", image_original=img_original, image_tk=self.imgtk_p1)

    def check_img_size(self, img):
        """
        Checks if image has too much resolution. Calls the function to resize if needed.
        Parameters
        ----------
        img : image cv2
            img selected by the user.
        """
        width = int(img.shape[1])
        height = int(img.shape[0])
        #Resolució proposada: 1080 x 720
        if (width > 1080 or height > 720):
            img = self.resize_img(img, 50)
        else:
            self.image_size_ok = True
            pub.sendMessage("IMAGE_SIZE_OK", image_cv2=img)
        return img

    def resize_img(self, img, scale_percent):
        """
        Resizes the img according to the scale_percent.
        Parameters
        ----------
        img : image cv2
           img selected by the user.
        scale_percent : int
            resize factor
        """
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        print(dim)
        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img = resized
        return img