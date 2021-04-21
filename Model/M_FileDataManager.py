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
PATH_DATABASE_DIR = "../resources/Database/"


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
        self.check_dir()
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

    def load_data(self):
        # try:
        list = os.listdir(PATH_DATABASE_DIR)
        pub.sendMessage("DATA_N_PACIENTS", patient_list=list)

    # except:
    # pub.sendMessage("DATA_FILES_KO")

    def save_data(self, metadata, img, new_patient, new_ulcer):
        """
        Calls functions to save the images and metadata
        Parameters
        ----------
        metadata : list
           a list with all the metadata field's information written by the user
        img : Pressure_img
           the pressur image object class with all sub-images processed by user
        """
        print("New patient: ", new_patient)
        print("New ulcer: ", new_ulcer)
        self.save_metadata(metadata, img, new_patient, new_ulcer)

    def save_metadata(self, metadata, img, new_patient, new_ulcer):
        """
        Creates a JSON object with the image data and metadata and writes it to a txt file.
        Parameters
        ----------
        metadata : list
           a list with all the metadata field's information written by the user
        img : Pressure_img
           the pressur image object class with all sub-images processed by user
        new_patient: bool
            indicates that a new patient must be added
        new_ulcer: bool
            indicates that a new ulcer must be added
        """

        metadata_json_object = {
            "id": self.id,
            "location": metadata[1],
            "metadata": {
                "code": metadata[0],
                "age": metadata[2],
                "gender": metadata[3],
                "n_imm": metadata[4],
                "u_imm": metadata[5],
                "n_hosp": metadata[6],
                "u_hosp": metadata[7],
                "n_inst": metadata[8],
                "u_inst": metadata[9],
                "date": metadata[10],
                "escala_emina": metadata[11],
                "escala_barthel": metadata[12],
                "conten": metadata[13],
                "n_conten": metadata[14],
                "u_conten": metadata[15],
                "grade": metadata[16],
                "cultiu": metadata[17],
                "protein": metadata[18],
                "albumina": metadata[19],
                "tr_ant": metadata[20],
                "tr_top": metadata[21]
            },
            "whitebalanced": img.whitebalanced,
            "perimetre": img.perimetre_done,
            "perimetre_cm": img.perimetre_cm,
            "granulation": len(img.granulation),
            "slough": len(img.slough),
            "necrosis": len(img.necrosis)
        }
        #try:
        if new_patient:
            self.save_new_patient(metadata, metadata_json_object, img)
        else:
            if new_ulcer:
                self.save_new_ulcer(metadata, metadata_json_object, img)
            else:
                self.save_old_ulcer(metadata, metadata_json_object, img)
        #except OSError:
            #print("Error de gestió de fitxers.")

    def save_new_patient(self, metadata, metadata_json_object, img):
        os.mkdir(PATH_DATABASE_DIR + metadata[0])
        location_json = {"location": [metadata[1]]}
        with open(PATH_DATABASE_DIR + metadata[0] + "/" + metadata[0] + ".txt", "w+") as outfile:
            json.dump(location_json, outfile)
        os.mkdir(PATH_DATABASE_DIR + metadata[0] + "/1")
        os.mkdir(PATH_DATABASE_DIR + metadata[0] + "/1/1")
        with open(PATH_DATABASE_DIR + metadata[0] + "/1/1/Metadata_" + str(metadata[0]) + "_1_1" + ".txt",
                  "w") as outfile:
            json.dump(metadata_json_object, outfile)
        cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/1/1" + "/img_origin_"+ str(metadata[0]) +"_1_1.jpg", img.img_origin)
        cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/1/1" + "/mask_"+ str(metadata[0]) +"_1_1.jpg", img.mask)
        cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/1/1" + "/img_"+ str(metadata[0]) +"_1_1.jpg", img.img)
        if img.perimetre_done:
            cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/1/1" + "/perimetre_"+ str(metadata[0]) +"_1_1.jpg",
                        img.perimetre)
        for i in range(0, len(img.granulation)):
            cv2.imwrite(
                PATH_DATABASE_DIR + metadata[0] + "/1/1" + "/granulation_"+ str(metadata[0]) +"_1_1_" + str(i+1) + ".jpg",
                img.granulation[i])
        for i in range(0, len(img.slough)):
            cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/1/1" + "/slough_"+ str(metadata[0]) +"_1_1_" + str(i+1) + ".jpg",
                        img.slough[i])
        for i in range(0, len(img.necrosis)):
            cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/1/1" + "/necrosis_"+ str(metadata[0]) +"_1_1_" + str(i+1) + ".jpg",
                        img.necrosis[i])

    def save_new_ulcer(self, metadata, metadata_json_object, img):
        locations_list = {}
        locations_list["location"] = []
        with open(PATH_DATABASE_DIR + metadata[0] + "/" + metadata[0] + ".txt") as json_file:
            locations = json.load(json_file)
            json_file.close()
        i = 1
        for ulcers in locations["location"]:
            locations_list["location"].append(ulcers)
            i = i + 1
        locations_list["location"].append(str(metadata[1]))
        with open(PATH_DATABASE_DIR + metadata[0] + "/" + metadata[0] + ".txt", "w+") as outfile:
            json.dump(locations_list, outfile)
        os.mkdir(PATH_DATABASE_DIR + metadata[0] + "/" + str(i))
        os.mkdir(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + "1")
        with open(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/1/Metadata_" + str(metadata[0]) + "_" + str(
                i) + "_1" + ".txt",
                  "w") as outfile:
            json.dump(metadata_json_object, outfile)
        cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/1" + "/img_origin_" + str(metadata[0]) + "_" + str(i) + "_1.jpg", img.img_origin)
        cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/1" + "/mask_"+ str(metadata[0]) + "_" + str(i) + "_1.jpg", img.mask)
        cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/1" + "/img_"+ str(metadata[0]) + "_" + str(i) + "_1.jpg", img.img)
        if img.perimetre_done:
            cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/1" + "/perimetre_" + str(metadata[0]) + "_" + str(i) + "1_1.jpg",
                        img.perimetre)
        for j in range(0, len(img.granulation)):
            cv2.imwrite(
                PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/1/granulation_"+ str(metadata[0]) + "_" + str(i) + "_1_" + str(j + 1) + ".jpg",
                img.granulation[j])
        for j in range(0, len(img.slough)):
            cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/1/slough_"+ str(metadata[0]) + "_" + str(i) + "_1_" + str(j + 1) + ".jpg",
                        img.slough[j])
        for j in range(0, len(img.necrosis)):
            cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/1" + "/necrosis_"+ str(metadata[0]) + "_" + str(i) + "_1_" + str(j + 1) + ".jpg",
                        img.necrosis[j])

    def save_old_ulcer(self, metadata, metadata_json_object, img):
        with open(PATH_DATABASE_DIR + metadata[0] + "/" + metadata[0] + ".txt") as json_file:
            locations = json.load(json_file)
            json_file.close()
        i = 0
        for ulcers in locations["location"]:
            i = i+1
            if ulcers.lower() == metadata[1].lower():
                n_ulcers = len([name for name in os.listdir(PATH_DATABASE_DIR + metadata[0] + "/" + str(i))])
                os.mkdir(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers + 1))
                print("Metadata[0]: "+metadata[0])
                print("i: "+str(i))
                print("n_ulcers+1: "+ str(n_ulcers+1))
                #with open(PATH_DATABASE_DIR + metadata[0] + "/" + str(i - 1) + "/" + str(n_ulcers + 1) + "/Metadata_" + str(
                #        metadata[0]) + "_" + str(i) + "_" + str(n_ulcers + 1) + ".txt",
                #          "w") as outfile:
                with open(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers+1) + "/Metadata_" + str(metadata[0]) + "_" + str(i) + "_" + str(n_ulcers+1) + ".txt",
                          "w") as outfile:
                    json.dump(metadata_json_object, outfile)
                outfile.close()
                cv2.imwrite(
                    PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers + 1) + "/img_origin_"+ str(metadata[0]) +"_" + str(i) + "_" + str(n_ulcers+1) +".jpg",
                    img.img_origin)
                cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers + 1) + "/mask_"+ str(metadata[0]) +"_" + str(i) + "_" + str(n_ulcers+1) +".jpg",
                            img.mask)
                cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers + 1) + "/img_"+ str(metadata[0]) +"_" + str(i) + "_" + str(n_ulcers+1) +".jpg",
                            img.img)
                if img.perimetre_done:
                    cv2.imwrite(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers + 1) + "/perimetre_"+ str(metadata[0]) +"_" + str(i) + "_" + str(n_ulcers+1) +".jpg",
                        img.perimetre)
                for j in range(0, len(img.granulation)):
                    print(PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(
                        n_ulcers + 1) + "/granulation_1_1_" + str(j + 1) + ".jpg")
                    cv2.imwrite(
                        PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers + 1) + "/granulation_" + str(metadata[0]) + "_" + str(i) + "_" + str(n_ulcers+1) + str(j + 1) + ".jpg",
                        img.granulation[j])
                for j in range(0, len(img.slough)):
                    cv2.imwrite(
                        PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers + 1) + "/slough_" + str(metadata[0]) + "_" + str(i) + "_" + str(n_ulcers+1) + str(j + 1) + ".jpg",
                        img.slough[j])
                for j in range(0, len(img.necrosis)):
                    cv2.imwrite(
                        PATH_DATABASE_DIR + metadata[0] + "/" + str(i) + "/" + str(n_ulcers + 1) + "/necrosis_" + str(metadata[0]) + "_" + str(i) + "_" + str(n_ulcers+1) + str(j + 1) + ".jpg",
                        img.necrosis[j])

    def load_img_i(self, id, location, dir):
        """
        Reads the image with the specified id from the directory
        Parameters
        ----------
        id : int patient id
           id of the patient that has to be read
        location : int
            directory index of the ulcer that has to be read
        dir : int
            directory index of the image that has to be read
        """

        im = ImageTk.PhotoImage(Image.open(PATH_DATABASE_DIR + str(id) + "/" + str(location) + "/" + str(dir) + "/mask_" + str(id) + "_" + str(location) + "_" + str(dir) + ".jpg"))
        pub.sendMessage("IMAGE_LOAD_i", img_tk=im)

    def check_code(self, code):
        code_exists = os.path.isdir(PATH_DATABASE_DIR + str(code))
        pub.sendMessage("CODE_CHECKED", existence=code_exists, code=code)

    def check_code_location(self, code, location):
        with open(PATH_DATABASE_DIR + str(code) + "/" + code + ".txt") as json_file:
            patient_ulcers = json.load(json_file)
            json_file.close()
        for ulcer in patient_ulcers["location"]:
            if ulcer.lower() == location.lower():
                return False
        return True

    def get_locations(self, code):
        with open(PATH_DATABASE_DIR + str(code) + "/" + str(code) + ".txt") as json_file:
            patient_ulcers = json.load(json_file)
            json_file.close()
        locations = []
        for ulcer in patient_ulcers["location"]:
            locations.append(ulcer)
        return locations

    def get_dates(self, id, location):
        dates = []
        n_ulcers = len([name for name in os.listdir(PATH_DATABASE_DIR + id + "/" + str(location))])
        for x in range(n_ulcers):
            with open(PATH_DATABASE_DIR + id + "/" + str(location) + "/" + str(x+1) + "/Metadata_"+ str(id) + "_" + str(location) + "_" + str(x+1) +".txt") as json_file:
                metadata = json.load(json_file)
                json_file.close()
                dates.append(metadata["metadata"]["date"])
        return dates
