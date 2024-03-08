from json import *
from tkinter import *

from launcher import *

def startgamemain():
    global config_data
    config_data = initconfig()

    for i in config_data["active"]:
        mode = setmode(i["mode"])
        name = setname(i["name"])

    match mode:
        case "easy":
            seteasy()
            initgamegui()
        case "medium":
            setmedium()
            initgamegui()
        case "hard":
            sethard()
            initgamegui()
        case "custom":
            setcustom()
            initgamegui()

    print(f"Mode: {mode}, Name {name}")

def initgamegui():
    global game
    game = Tk()
    game.title("Kopfrechentrainer Launcher")
    game.config(bg="white")
    game.resizable(False,False)
    game.state("zoomed")
    game.mainloop()

"""
In case I want to add the ability to minimize the launcher window while running the game
def window_close():
    exit = messagebox.askyesno("Exit?", "Willst du das Fenster schließen? \n Es wird alles gespeichert!")
    if exit:
        game.destroy()
"""

if __name__ == "__main__":
    startgamemain()