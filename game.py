from launcher import *
from json import *
from tkinter import *

def main():
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
    game = Tk()
    game.title("Kopfrechentrainer Launcher")
    game.config(bg="white")
    game.resizable(False,False)
    game.state("zoomed")
    game.mainloop()

if __name__ == "__main__":
    main()