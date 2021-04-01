import ctypes
import sys

from pubsub import pub

from Controller import C_Setup
from Model import M_LanguageSelection
from View import V_LanguageSelection
import tkinter as tk
class LanguageSelection:
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
        self.lang = lang
        self.model_lang.updateSelected(lang)
        pub.sendMessage("LANG_OK_ASKED", lang=lang)

    def change_lang(self, lang):
        self.model_lang.updateSelected(lang)
        self.view_lang.lang_changed()