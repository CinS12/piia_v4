"""Language selection class
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

Class to update language selection.
"""

import json

PATH_LANGUAGE = "resources/Language"
class ModelLanguageSelection:
    """
    Class responsible for loading and updating language selection
    from user.
    ...
    Attributes
    ----------
    lang : String
        language id
    Methods
    -------
    loadSelected()
        Reads and returns the language id from the file.
    updateSelected(lang)
        Updates the language file with the new option selected by the user.
    """

    def __init__(self):
        self.lang = ""

    def loadSelected(self):
        """
        Reads and returns the language id from the file.
        """
        with open(PATH_LANGUAGE + ".txt") as json_file:
            lang_selected = json.load(json_file)
            return lang_selected

    def updateSelected(self, lang):
        """
        Updates the language file with the new option selected by the user.
        Parameters
        ----------
        lang : String
            language id
        """
        with open(PATH_LANGUAGE + ".txt") as json_file:
            lang_selected = json.load(json_file)

        if lang == 0:
            lang_selected["selected"] = "cat"
        if lang == 1:
            lang_selected["selected"] = "cast"
        if lang == 2:
            lang_selected["selected"] = "eng"

        print(lang_selected)

        with open(PATH_LANGUAGE + ".txt", "w") as outfile:
           json.dump(lang_selected, outfile)