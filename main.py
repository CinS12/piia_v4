import tkinter as tk
import ctypes
import Controller.C_Setup as C_Setup

if __name__ == "__main__":
    #lang = C_LanguageSelection.LanguageSelection()
    #print("Lang: ",lang.lang)
    #if lang.lang != "":
    root = tk.Tk()
    root.title("PIIA")

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    w = screensize[0]
    h = screensize[1]
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 3) - (h / 3)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    app = C_Setup.ControllerSetup(root, w, h, x, y)
    root.mainloop()
    #else:
        #lang.lang = lang.view_lang.ask_lang()