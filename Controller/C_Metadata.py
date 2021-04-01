from pubsub import pub

class ControllerMetadata:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        pub.subscribe(self.barthel_data_sent, "BARTHEL_DATA_SENT")
        pub.subscribe(self.update_barthel, "UPDATE_BARTHEL")
        pub.subscribe(self.error_barthel, "ERROR_BARTHEL")
        pub.subscribe(self.emina_data_sent, "EMINA_DATA_SENT")
        pub.subscribe(self.update_emina, "UPDATE_EMINA")
        pub.subscribe(self.error_emina, "ERROR_EMINA")
        return

    def barthel_data_sent(self, data):
        """
         Calls the Model function to calculate barthel from data sent.
         Parameters
        ----------
        data : list
           list with all the field's values selected by the user
        """

        print("controller - barthel_data_sent!")
        self.model.calculateBarthel(data)

    def emina_data_sent(self, data):
        """
         Calls the Model function to calculate emina from data sent.
         Parameters
        ----------
        data : list
           list with all the field's values selected by the user
        """

        print("controller - emina_data_sent!")
        self.model.calculateEmina(data)

    def update_barthel(self, data):
        """
        Calls the View function update_barthel to update barthel value.
        Parameters
        ----------
        data : int
            value of the barthel scale
       """

        print("controller - update_barthel")
        self.view.processing_page.update_barthel(data)

    def update_emina(self, data):
        """
        Calls the View function update_emina to update emina value.
        Parameters
        ----------
        data : int
            value of the emina scale
       """

        print("controller - update_emina")
        self.view.processing_page.update_emina(data)

    def error_barthel(self):
        """
       View request to check barthel fields.
       """

        print("controller - error barthel")
        self.view.popupmsg("S'han d'omplir tots els camps")

    def error_emina(self):
        """
        View request to check emina fields.
        """

        print("controller - error emina")
        self.view.popupmsg("S'han d'omplir tots els camps")