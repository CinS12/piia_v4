import json
from pubsub import pub
PATH_LANGUAGE = "../resources/Language"
class ModelLanguageSelection:
    def __init__(self):
        self.lang = ""

    def loadSelected(self):
        with open(PATH_LANGUAGE + ".txt") as json_file:
            lang_selected = json.load(json_file)
            return lang_selected

    def updateSelected(self, lang):
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