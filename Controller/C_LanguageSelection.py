"""Language selection manager class
sectionauthor:: Artur Martí Gelonch <artur.marti@students.salle.url.edu>

Class to manage the language selection process.
"""
from pubsub import pub
from Model import M_LanguageSelection
from View import V_LanguageSelection

class LanguageSelection:
    """
    Class to manage the language selection process.
    ...
    Attributes
    ----------
    lang : String
        language selection id
    view_lang : ViewLanguageSelection
        language selection viewer
    model_lang : ModelLanguageSelection
        language selection logic
    Methods
    -------
    check_language()
        Checks on file if language has been selected previously by the user.
    lang_selected(lang)
        Calls the Model function to update the language selection.
    change_lang(lang)
        Calls the Model function to change the language selection on execution time.
    """
    def __init__(self, parent):
        self.lang = ""
        self.parent = parent
        pub.subscribe(self.lang_selected, "LANG_SELECTED")
        pub.subscribe(self.change_lang, "CHANGE_LANG")

        self.view_lang = V_LanguageSelection.ViewLanguageSelection(parent)
        self.model_lang = M_LanguageSelection.ModelLanguageSelection()
        self.check_language()
        return

    def check_language(self):
        """
        Checks on file if language has been selected previously by the user.
        """
        lang = self.model_lang.loadSelected()
        if lang["selected"] == "":
            self.view_lang.ask_lang()
        else:
            lang = lang["selected"]
            self.lang = lang
            if lang == "cat":
                lang = 0
            else:
                if lang == "cast":
                    lang = 1
                else:
                    if lang == "eng":
                        lang = 2
            pub.sendMessage("LANG_OK_LOADED", lang=lang)

    def lang_selected(self, lang):
        """
        Calls the Model function to update the language selection.
        Parameters
        ----------
        lang : String
            language selection id
       """
        self.lang = lang
        self.model_lang.updateSelected(lang)
        pub.sendMessage("LANG_OK_ASKED", lang=lang)

    def change_lang(self, lang):
        """
        Calls the Model function to change the language selection on execution time.
        Parameters
        ----------
        lang : String
            language selection id
       """
        self.model_lang.updateSelected(lang)
        self.view_lang.lang_changed()