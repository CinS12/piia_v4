"""Main data manager
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>
It is the application's dynamic data structure,
independent of the user interface. It directly manages the data.
"""

from datetime import datetime
from tkinter import filedialog
import cv2
from PIL import ImageTk
from pubsub import pub

class MetadataManager:
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
    getData(data)
        Saves the data from the list to the metadata variables.
        Calls the functions to check input data and sends the request.
    camps_plens(code, age, gender, n_imm, n_hosp, n_inst, date, conten,
                n_conten, grade, cultiu, protein, albumina)
        Returns if these input data fields are answered.
    comprova_errors(code, age, n_imm, n_hosp, n_inst, date, conten, n_conten)
        Checks if these user parameters match with their expected pattern.
        Sends a request with the errors found to the Controller.
    checkBarthel(data)
       Returns if all barthel data input fields have been answered.
    sumarBarthel(data)
        Returns the barthel sacle value from input data list.
    calculateBarthel(data)
        Calls the functions to check and get barthel value.
        and sends the request to the Controller.
    checkEmina(data)
         Returns if all emina data input fields have been answered.
    sumarEmina(data)
        Returns the emina sacle value from input data list.
    calculateEmina(data)
        Calls the functions to check and get emina value
        and sends a request to the Controller.
    """

    def __init__(self):
        self.metadata = []
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
            return path

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

    def getData(self, data):
        """
        Saves the data from the list to the metadata variables.
        Calls the functions to check input data and sends the request.
        Parameters
        ----------
        data : list
           a list with all the metadata field's information answered by the user
        """

        # Codi
        code = data[0].get()
        # Edat
        age = data[1].get()
        # Sexe
        gender = data[2].get()
        # Temps immobilització
        n_imm = data[3].get()
        u_imm = data[4].get()
        # Temps hospitalització
        n_hosp = data[5].get()
        u_hosp = data[6].get()
        # Temps institucionalització
        n_inst = data[7].get()
        u_inst = data[8].get()
        # Data
        date = data[9].get()
        # Escala EMINA
        escala_emina = data[10].get()
        # Escala Barthel
        escala_barthel = data[11].get()
        # Contenció mecànica
        conten = data[12]
        n_conten = 0
        u_conten = 0
        if conten == "si":
            n_conten = data[13].get()
            u_conten = data[14].get()
        # Grau de la nafra
        grade = data[15].get()
        # Cultiu de l’exsudat
        cultiu = data[16]
        # Proteïnes totals
        protein = data[17].get()
        # Albúmina
        albumina = data[18].get()
        #Tractament
        tr_ant = data[19]
        tr_top = data[20]
        tot_ple = self.camps_plens(code, age, gender, n_imm, n_hosp, n_inst, date, conten, n_conten, grade, cultiu, protein, albumina)
        if tot_ple:
            error = self.comprova_errors(code, age, n_imm, n_hosp, n_inst, date, conten, n_conten)
            if error == False:
                self.metadata = [code, age, gender, n_imm, u_imm, n_hosp, u_hosp, n_inst, u_inst, date, escala_emina,
                                 escala_barthel, conten, n_conten, u_conten, grade, cultiu, protein, albumina, tr_ant, tr_top]
                pub.sendMessage("DATA_OK")
        else:
            pub.sendMessage("TOT_PLE_KO")

    def camps_plens(self, code, age, gender, n_imm, n_hosp, n_inst, date, conten, n_conten, grade, cultiu, protein, albumina):
        """
        Returns if these input data fields are answered.
        Parameters
        ----------
        code : int
           4 digit code.
        age : int
           year of injury owner's birth.
        gender : String
           gender of injury owner's.
        n_imm : int
           number of "days/weeks/months" immobilized.
        n_hosp : int
           number of "days/weeks/months" hospitalized.
        n_inst : int
           number of "days/weeks/months" institutionalized.
        date : Date
           date when the processed picture was taken.
        conten : String
           Yes or no.
        n_conten : int
          number of "days/weeks/months" contention.
        grade : int
           grade classification of the injury (from 1 to 4)
        cultiu : String
           Yes or no.
        protein : String
           user comments about protein treatment.
        albumina : String
           user comments about "albumina" treatment.
        """
        tot_ple = True
        if code=="" or age=="" or gender=="" or n_imm =="" or n_hosp=="" or n_inst=="" or date=="" or conten=="" or n_conten=="" or grade=="" or cultiu=="" or protein=="" or albumina=="":
            tot_ple = False
        return tot_ple

    def comprova_errors(self, code, age, n_imm, n_hosp, n_inst, date, conten, n_conten):
        """
        Checks if these user parameters match with their expected pattern.
        Sends a request with the errors found to the Controller.
        Parameters
        ----------
        code : int
           4 digit code.
        age : int
           year of injury owner's birth.
        n_imm : int
           number of "days/weeks/months" immobilized.
        n_hosp : int
           number of "days/weeks/months" hospitalized.
        n_inst : int
           number of "days/weeks/months" institutionalized.
        date : Date
           date when the processed picture was taken.
        conten : String
           Yes or no.
        n_conten : int
          number of "days/weeks/months" contention.
        """

        data_error = []
        #Code
        if len(code) != 4:
            data_error.append("CODE_ERROR")
        #Age
        if len(age) != 4:
            data_error.append("AGE_ERROR")
        else:
            try:
                int(age)
            except:
                data_error.append("AGE_ERROR")
        #Immobilització
        try:
            int(n_imm)
        except:
            data_error.append("N_IMM_ERROR")
        # Hospitalització
        try:
            int(n_hosp)
        except:
            data_error.append("N_HOSP_ERROR")
        # Institucionalització
        try:
            int(n_inst)
        except:
            data_error.append("N_INST_ERROR")
        # Date
        try:
            datetime.strptime(date, "%m/%d/%y")
        except:
            data_error.append("DATE_ERROR")
        # Contenció Mecànica
        if conten == "si":
            try:
                int(n_conten)
            except:
                data_error.append("N_CONTEN_ERROR")
        #Gestió error
        if data_error == []:
            error = False
        else:
            error = True
            pub.sendMessage("DATA_KO", error=data_error)
        return error

    def checkBarthel(self, data):
        """
        Returns if all barthel data input fields have been answered.
        Parameters
        ----------
        data : list
           a list with all the barthel field's information answered by the user.
        """

        totOk = True
        menjar = data.menjar_combobox.current()
        rentar = data.rentar_combobox.current()
        vestir = data.vestir_combobox.current()
        arreglar = data.arreglar_combobox.current()
        deposicio = data.deposicio_combobox.current()
        miccio = data.miccio_combobox.current()
        lavabo = data.lavabo_combobox.current()
        trasllat = data.trasllat_combobox.current()
        deambulacio = data.deambulacio_combobox.current()
        escales = data.escales_combobox.current()

        if(menjar == -1 or rentar==-1 or vestir==-1 or arreglar==-1 or deposicio==-1 or miccio==-1 or lavabo==-1 or trasllat==-1 or deambulacio==-1 or escales==-1):
            totOk = False
        else:
            totOk = True

        return totOk

    def sumarBarthel(self, data):
        """
        Returns the barthel sacle value from input data list.
        Parameters
        ----------
        data : list
           a list with all the barthel field's information answered by the user.
        """

        menjar = data.menjar_combobox.current()
        rentar = data.rentar_combobox.current()
        vestir = data.vestir_combobox.current()
        arreglar = data.arreglar_combobox.current()
        deposicio = data.deposicio_combobox.current()
        miccio = data.miccio_combobox.current()
        lavabo = data.lavabo_combobox.current()
        trasllat = data.trasllat_combobox.current()
        deambulacio = data.deambulacio_combobox.current()
        escales = data.escales_combobox.current()

        switcher1 = {
            0: 10,
            1: 5,
            2: 0,
        }

        switcher2 = {
            0: 5,
            1: 0,
        }

        switcher3 = {
            0: 15,
            1: 10,
            2: 5,
            3: 0,
        }
        escala = switcher1.get(menjar) + switcher2.get(rentar) + switcher1.get(vestir) + switcher2.get(arreglar) + \
                 switcher1.get(deposicio) + switcher1.get(miccio) + switcher1.get(lavabo) + switcher3.get(trasllat) + switcher3.get(deambulacio) + switcher1.get(escales)
        return escala

    def calculateBarthel(self, data):
        """
        Calls the functions to check and get barthel value.
        and sends the request to the Controller.
        Parameters
        ----------
        data : list
           a list with all the barthel field's information answered by the user.
        """

        totOk = self.checkBarthel(data)
        if (totOk == True):
            escala = self.sumarBarthel(data)
            print(escala)
            pub.sendMessage("UPDATE_BARTHEL", data=escala)
        else:
            pub.sendMessage("ERROR_BARTHEL")

    def checkEmina(self, data):
        """
        Returns if all emina data input fields have been answered.
        Parameters
        ----------
        data : list
           a list with all the emina field's information answered by the user.
        """

        totOk = True
        mental = data.mental_combobox.current()
        movilitat = data.movilitat_combobox.current()
        humitat = data.humitat_combobox.current()
        nutricio = data.nutricio_combobox.current()
        activitat = data.activitat_combobox.current()
        if (mental == -1 or movilitat == -1 or humitat == -1 or nutricio == -1 or activitat == -1):
            totOk = False
        else:
            totOk = True
        return totOk

    def sumarEmina(self, data):
        """
        Returns the emina sacle value from input data list.
        Parameters
        ----------
        data : list
           a list with all the emina field's information answered by the user.
        """

        mental = data.mental_combobox.current()
        movilitat = data.movilitat_combobox.current()
        humitat = data.humitat_combobox.current()
        nutricio = data.nutricio_combobox.current()
        activitat = data.activitat_combobox.current()

        switcher = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
        }
        escala = switcher.get(mental) + switcher.get(movilitat) + switcher.get(humitat) + switcher.get(nutricio) + switcher.get(activitat)
        return escala

    def calculateEmina(self, data):
        """
        Calls the functions to check and get emina value
        and sends a request to the Controller.
        Parameters
        ----------
        data : list
           a list with all the emina field's information answered by the user.
        """

        totOk = self.checkEmina(data)
        if (totOk == True):
            escala = self.sumarEmina(data)
            print(escala)
            pub.sendMessage("UPDATE_EMINA", data=escala)
        else:
            pub.sendMessage("ERROR_EMINA")