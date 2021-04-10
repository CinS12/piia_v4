"""File and directory manager
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>
Tool that allows to check, read and write files to specified directories
that contain image files and metadata files. The files must be "txt" and "jpg".
"""

from pubsub import pub
from PIL import ImageTk, Image
import os, os.path
import json
import cv2


PATH_METADATA_DIR = "../resources/Metadata"
PATH_IMG_DIR = "../resources/Images"
PATH_IMG_i = "../resources/Images/Img_"
PATH_METADATA_i = "../resources/Metadata/Metadata_"
PATH_CODE_DIR = "../resources/Database/"

class FileDataManager:
    """
    A class used to manage the files's data reading/writing
    ...
    Attributes
    ----------
    id : int
        an integer that identifies the file and directory
    num_file_ok : bool
        a boolean to check the image and metadata files
    Methods
    -------
    check_dir()
        Calls the functions to check or create the image and metadata directories
    check_metadata_dir()
        Checks or creates the metadata directory
    check_images_dir()
        Checks or creates the images directory
    check_files()
        Check if the image and metadata files's number match and set the id
    load_data()
        Sends the id to the Controller
    save_data(metadata, img)
        Saves the images and metadata
    save_metadata(metadata, img)
        Creates a JSON object with the image data and metadata and writes it to a txt file
    save_img(img)
        Saves all sub-images from Pressure_img object to a directory
    load_img_i(i)
        Reads the image with the specified id from the directory
    load_metadata_i(i)
        Reads the metadata file with the specified id from the directory
       """

    def __init__(self):
        self.id = None
        self.num_files_ok = True
        self.check_dir()
        self.check_files()
        return

    def check_dir(self):
        """
        Calls the functions to check or create the image and metadata directories.
        """

        self.check_metadata_dir()
        self.check_images_dir()

    def check_metadata_dir(self):
        """
        Checks or creates the metadata directory.
        Uses the constant PATH_METADATA_DIR to find the directory.
        """

        try:
            os.mkdir(PATH_METADATA_DIR)
        except OSError:
            print("Creation of the directory %s failed" % PATH_METADATA_DIR)
        else:
            print("Successfully created the directory %s " % PATH_METADATA_DIR)

    def check_images_dir(self):
        """
        Checks or creates the images directory.
        Uses the constant PATH_IMG_DIR to find the directory.
        """

        try:
            os.mkdir(PATH_IMG_DIR)
        except OSError:
            print("Creation of the directory %s failed" % PATH_IMG_DIR)
        else:
            print("Successfully created the directory %s " % PATH_IMG_DIR)

    def check_files(self):
        """
        Check if the image and metadata files's number match and set the id.
        Counts and compares all image folders with all metadata txt files.
        """

        n_metadata = len(
            [name for name in os.listdir(PATH_METADATA_DIR) if os.path.isfile(os.path.join(PATH_METADATA_DIR, name))])
        n_img = len([name for name in os.listdir(PATH_IMG_DIR)])
        if n_metadata != n_img:
            self.num_files_ok = False
        else:
            self.id = n_img + 1
    def load_data(self):
        """
       Checks files's number's and sends it as a request to the Controller
       """
        if self.num_files_ok:
            self.check_files()
            #Subtract 1 to the id because directory's files start with 1 and arrays with 0
            pub.sendMessage("DATA_N_ELEMENTS", num=(self.id - 1))
        else:
            pub.sendMessage("DATA_FILES_KO")

    def save_data(self, metadata, img):
        """
        Calls functions to save the images and metadata
        Parameters
        ----------
        metadata : list
           a list with all the metadata field's information written by the user
        img : Pressure_img
           the pressur image object class with all sub-images processed by user
        """

        if self.num_files_ok:
            self.save_metadata(metadata, img)
            self.save_img(img)
        else:
            pub.sendMessage("DATA_FILES_KO")

    def save_metadata(self, metadata, img):
        """
        Creates a JSON object with the image data and metadata and writes it to a txt file.
        Parameters
        ----------
        metadata : list
           a list with all the metadata field's information written by the user
        img : Pressure_img
           the pressur image object class with all sub-images processed by user
        """

        metadata_json_object = {
            "id": self.id,
            "metadata": {
                "code": metadata[0],
                "age": metadata[1],
                "gender": metadata[2],
                "n_imm": metadata[3],
                "u_imm": metadata[4],
                "n_hosp": metadata[5],
                "u_hosp": metadata[6],
                "n_inst": metadata[7],
                "u_inst": metadata[8],
                "date": metadata[9],
                "escala_emina": metadata[10],
                "escala_barthel": metadata[11],
                "conten": metadata[12],
                "n_conten": metadata[13],
                "u_conten": metadata[14],
                "grade": metadata[15],
                "cultiu": metadata[16],
                "protein": metadata[17],
                "albumina": metadata[18],
                "tr_ant": metadata[19],
                "tr_top": metadata[20]
            },
            "whitebalanced": img.whitebalanced,
            "perimetre": img.perimetre_done,
            "perimetre_cm": img.perimetre_cm,
            "granulation": len(img.granulation),
            "slough": len(img.slough),
            "necrosis": len(img.necrosis)
        }
        with open(PATH_METADATA_DIR + "/Metadata_" + str(self.id) + ".txt", "w") as outfile:
            json.dump(metadata_json_object, outfile)

    def save_img(self, img):
        """
        Saves all sub-images from Pressure_img object to a directory.
        Uses the constant "PATH_IMG_DIR" + id as a path to the folder.
        Parameters
        ----------
        img : Pressure_img
           the pressur image object class with all sub-images processed by user
        """

        try:
            os.mkdir(PATH_IMG_DIR + "/Img_" + str(self.id))
        except OSError:
            print("Creation of the directory %s failed" % PATH_IMG_DIR + "/Img_" + str(self.id))
        else:
            print("Successfully created the directory %s " % PATH_IMG_DIR + "/Img_" + str(self.id))
            cv2.imwrite(PATH_IMG_DIR + "/Img_" + str(self.id) + "/img_origin_" + str(self.id) + ".jpg", img.img_origin)
            cv2.imwrite(PATH_IMG_DIR + "/Img_" + str(self.id) + "/mask_" + str(self.id) + ".jpg", img.mask)
            cv2.imwrite(PATH_IMG_DIR + "/Img_" + str(self.id) + "/img_" + str(self.id) + ".jpg", img.img)
            if img.perimetre_done:
                cv2.imwrite(PATH_IMG_DIR + "/Img_" + str(self.id) + "/perimetre_" + str(self.id) + ".jpg",
                            img.perimetre)
        for i in range(0, len(img.granulation)):
            cv2.imwrite(
                PATH_IMG_DIR + "/Img_" + str(self.id) + "/granulation" + str(self.id) + "_" + str(i + 1) + ".jpg",
                img.granulation[i])
        for i in range(0, len(img.slough)):
            cv2.imwrite(PATH_IMG_DIR + "/Img_" + str(self.id) + "/slough" + str(self.id) + "_" + str(i + 1) + ".jpg",
                        img.slough[i])
        for i in range(0, len(img.necrosis)):
            cv2.imwrite(PATH_IMG_DIR + "/Img_" + str(self.id) + "/necrosis" + str(self.id) + "_" + str(i + 1) + ".jpg",
                        img.necrosis[i])

    def load_img_i(self, i):
        """
        Reads the image with the specified id from the directory
        Parameters
        ----------
        i : int
           id of the image that has to be read
        """

        im = ImageTk.PhotoImage(Image.open(PATH_IMG_i + str(i) + "/mask_" + str(i) + ".jpg"))
        pub.sendMessage("IMAGE_LOAD_i", img_tk=im)


    def load_metadata_i(self, i):
        """
        Reads the metadata file with the specified id from the directory
        Parameters
        ----------
        i : int
           id of the metadata file that has to be read
        """

        with open(PATH_METADATA_i + str(i) + ".txt") as json_file:
            data = json.load(json_file)
            pub.sendMessage("METADATA_LOAD_i", metadata=data)

    def check_code(self, code):
        code_exists = os.path.isdir(PATH_CODE_DIR + str(code))
        pub.sendMessage("CODE_CHECKED", existence=code_exists)