from tkinter import *
from tkinter import messagebox
from json import *

#Launcher for the Kopfrechentrainer

#functions to set configs
def setmode(modus):
    global mode
    mode = modus
    return mode

def setname(name):
    global username
    username = name
    return name

def setmultiply(multiply):
    global multiply_js
    multiply_js = int(multiply)
    return multiply_js

def setdivide(divide):
    global divide_js
    divide_js = int(divide)
    return divide_js

def setpwr(pwr):
    global pwr_js
    pwr_js = int(pwr)
    return pwr_js

def setsqrt(sqrt):
    global sqrt_js
    sqrt_js = int(sqrt)
    return sqrt_js

def settimer(time):
    global seconds
    seconds = time
    return seconds

def seteasy():
    for i in config_data["modes"]["easy"]:
        setmultiply(i["multiply"])
        setdivide(i["divide"])
        setpwr(i["pwr"])
        setsqrt(i["sqrt"])
        settimer(i["timer"])

def setmedium():
    for i in config_data["modes"]["medium"]:
        setmultiply(i["multiply"])
        setdivide(i["divide"])
        setpwr(i["pwr"])
        setsqrt(i["sqrt"])
        settimer(i["timer"])

def sethard():
    for i in config_data["modes"]["hard"]:
        setmultiply(i["multiply"])
        setdivide(i["divide"])
        setpwr(i["pwr"])
        setsqrt(i["sqrt"])
        settimer(i["timer"])

def setcustom():
    for i in config_data["modes"]["custom"]:
        setmultiply(i["multiply"])
        setdivide(i["divide"])
        setpwr(i["pwr"])
        setsqrt(i["sqrt"])
        settimer(i["timer"])

#Functions to change mode
def selecteasy():
    global mode 
    mode = "easy"
    seteasy()
    update_input(DISABLED, multiply_js, divide_js, pwr_js, sqrt_js, seconds)

def selectmedium():
    global mode
    mode = "medium"
    setmedium()
    #print(seconds)
    update_input(DISABLED, multiply_js, divide_js, pwr_js, sqrt_js, seconds)

def selecthard():
    global mode
    mode = "hard"
    sethard()
    update_input(DISABLED, multiply_js, divide_js, pwr_js, sqrt_js, seconds)

def selectcustom():
    global mode
    mode = "custom"
    setcustom()
    update_input(NORMAL, multiply_js, divide_js, pwr_js, sqrt_js, seconds)

def initconfig():
    global config_data
    f = open("config.json","r")
    config_data = load(f)
    return config_data

def main():
    #Get config from config.json
    initconfig()
    for i in config_data["active"]:
        setmode(i["mode"])
        setname(i["name"])

    try:
        match mode:
            case "easy":
                seteasy()
                initgui()
                selecteasy()
            case "medium":
                setmedium()
                initgui()
                selectmedium()
            case "hard":
                sethard()
                initgui()
                selecthard()
            case "custom":
                setcustom()
                initgui()
                selectcustom()
    except TclError:
        pass

def initgui():

    global multiply
    global multiply_var
    global divide
    global divide_var
    global pwr
    global pwr_var
    global sqrt
    global sqrt_var

    global bt_easy
    global bt_medium
    global bt_hard
    global bt_custom

    global timer
    global name
    global launcher

    #Create window for launcher
    bg_color = "white"
    launcher = Tk()
    launcher.title("Kopfrechentrainer Launcher")
    launcher.geometry("670x500")
    launcher.config(bg=bg_color)
    launcher.resizable(False,False)

    #Create layout

    #info about what to do
    info = Label(launcher, text="Konfiguriere das Spiel:", bg=bg_color)
    info.grid(row=0, columnspan=1, padx=5, pady=8)

    #Name input for online services (planed)
    Label(launcher, text="Name", bg=bg_color).grid(row=1, padx=5, pady=5)
    name = Entry(launcher, bd=3)
    name.insert(0, username)
    name.grid(row=1, column=1, columnspan=2, padx=5, pady=5,sticky=W+E)

    #Pick level
    bt_info = Label(launcher, text="Wähle das Level:", bg=bg_color)
    bt_info.grid(row=2, column=0, columnspan=1, padx=5, pady=8)

    bt_easy = Button(launcher, text="Easy", command=selecteasy, width=20)
    bt_medium = Button(launcher, text="Medium", command=selectmedium, width=20)
    bt_hard = Button(launcher, text="Hard", command=selecthard, width=20)
    bt_custom = Button(launcher, text="Custom", command=selectcustom, width=20)

    bt_easy.grid(row=3, column=0, padx=5, pady=5)
    bt_medium.grid(row=3, column=1, padx=5, pady=5)
    bt_hard.grid(row=3, column=2, padx=5, pady=5)
    bt_custom.grid(row=3, column=3, padx=5, pady=5)

    #Change level specifics
    specs = Frame(launcher, bg="lightgrey", height="360").grid(row=4, columnspan=4, rowspan=10, sticky=W+E+S+N)


    #Choose operators
    multiply_var = IntVar(value=multiply_js)
    divide_var = IntVar(value=divide_js)
    pwr_var = IntVar(value=pwr_js)
    sqrt_var = IntVar(value=sqrt_js)

    multiply = Checkbutton(specs, width=10, text="Multiplication", variable=multiply_var, bg="darkgrey")
    multiply.grid(row=4, column=2, padx=5, pady=10, sticky="n")
    divide = Checkbutton(specs, width=10, text="Division", variable=divide_var, bg="darkgrey")
    divide.grid(row=4, column=3, padx=5, pady=10, sticky="n")
    pwr = Checkbutton(specs, width=10, text="Power", variable=pwr_var, bg="darkgrey")
    pwr.grid(row=4, column=0, padx=5, pady=10, sticky="n", )
    sqrt = Checkbutton(specs, width=10, text="Squareroot", variable=sqrt_var, bg="darkgrey")
    sqrt.grid(row=4, column=1, padx=5, pady=10,sticky="n")

    #Timer
    Label(specs, text="Starttime per Question (seconds)", bg=bg_color).grid(row=5, padx=5, pady=5, sticky="n")
    timer = Entry(specs, bd=3, )
    timer.insert(0, f"{seconds}")
    timer.grid(row=5, column=1, columnspan=2, padx=5, pady=5,sticky="wen")

    #Launch btn
    Button(launcher, text="Launch", command=initlaunch, width = 10).grid(row=13, column=3, padx=5, pady=5, sticky="we")
    
    launcher.protocol("WM_DELETE_WINDOW", window_exit)
    launcher.mainloop()

#Updates the value shown on screen so that person sees them, takes a lot as input wtf why am i here its 0:37am xD
def update_input(status, m=None, d=None, p=None, s=None, t=None):

    #Used to toggle the active buttons
    bt_easy.config(state=NORMAL)
    bt_medium.config(state=NORMAL)
    bt_hard.config(state=NORMAL)
    bt_custom.config(state=NORMAL)
    match mode:
        case "easy":
            bt_easy.config(state=DISABLED)
        case "medium":
            bt_medium.config(state=DISABLED)
        case "hard":
            bt_hard.config(state=DISABLED)
        case "custom":
            bt_custom.config(state=DISABLED)
    
    timer.config(state=NORMAL)
    timer.delete(0, END)
    timer.insert(0, f"{t}")
    timer.config(state=status)
    pwr.config(state=status)
    pwr_var.set(p)
    sqrt.config(state=status)
    sqrt_var.set(s)
    multiply.config(state=status)
    multiply_var.set(m)
    divide.config(state=status)
    divide_var.set(d)
    launcher.update()

#Overrides config file
def update_config(m, d, p, s, t):
    with open("config.json", "r+") as f:
        config = load(f)
        for i in config["active"]:
            i["mode"] = mode
            i["name"] = name.get()

        for i in config["modes"]["custom"]:
            i["multiply"] = m
            i["divide"] = d
            i["pwr"] = p
            i["sqrt"] = s
            i["timer"] = t

        f.seek(0)
        dump(config, f, indent=4)
        f.truncate()

#Saving config when closing window
def window_exit():
    exit = messagebox.askyesno("Exit?", "Willst du das Fenster schließen? \n Es wird alles gespeichert!")
    if exit:
        update_config(bool(int(multiply_var.get())), bool(int(divide_var.get())), bool(int(pwr_var.get())), bool(int(sqrt_var.get())), int(timer.get()))
        launcher.destroy()

#initialize launch
def initlaunch():
    update_config(bool(int(multiply_var.get())), bool(int(divide_var.get())), bool(int(pwr_var.get())), bool(int(sqrt_var.get())), int(timer.get()))

if __name__ == "__main__":
    main()
