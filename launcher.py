from tkinter import *
from json import *

#Launcher for the Kopfrechentrainer

#functions to set configs
def setmode(modus):
    global mode
    mode = modus

def setname(name):
    global username
    username = name

def setmultiply(multiply):
    global multiply_js
    multiply_js = int(multiply)

def setdivide(divide):
    global divide_js
    divide_js = int(divide)

def setpwr(pwr):
    global pwr_js
    pwr_js = int(pwr)

def setsqrt(sqrt):
    global sqrt_js
    sqrt_js = int(sqrt)

def settimer(time):
    global seconds
    seconds = time

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

#Get config from config.json
f = open("config.json","r")
config_data = load(f)

for i in config_data["active"]:
    setmode(i["mode"])
    setname(i["name"])

match mode:
    case "easy":
        seteasy()
    case "medium":
        setmedium()
    case "hard":
        sethard()
    case "custom":
        setcustom()


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

#Create window for launcher
bg_color = "white"
launcher = Tk()
launcher.title("Kopfrechentrainer Launcher")
launcher.geometry("670x500")
launcher.config(bg=bg_color)

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
specs = Frame(launcher, bg="lightgrey", height="360").grid(row=4, columnspan=4, rowspan=4, sticky=W+E+S+N)


#Choose operators
multiply_var = IntVar(value=multiply_js)
divide_var = IntVar(value=divide_js)
pwr_var = IntVar(value=pwr_js)
sqrt_var = IntVar(value=sqrt_js)

multiply = Checkbutton(specs, width=10, text="Multiplication", variable=multiply_var, bg="darkgrey")
multiply.grid(row=4, column=2, padx=5, pady=5, sticky="n")
divide = Checkbutton(specs, width=10, text="Division", variable=divide_var, bg="darkgrey")
divide.grid(row=4, column=3, padx=5, pady=5, sticky="n")
pwr = Checkbutton(specs, width=10, text="Power", variable=pwr_var, bg="darkgrey")
pwr.grid(row=4, column=0, padx=5, pady=5, sticky="n", )
sqrt = Checkbutton(specs, width=10, text="Squareroot", variable=sqrt_var, bg="darkgrey")
sqrt.grid(row=4, column=1, padx=5, pady=5,sticky="n")


#Timer
Label(specs, text="Starttime per Question (seconds)", bg=bg_color).grid(row=5, padx=5, pady=5, sticky="wen")
timer = Entry(specs, bd=3, )
timer.insert(0, f"{seconds}")
timer.grid(row=5, column=1, columnspan=2, padx=5, pady=5,sticky="wen")

#Updates the value shown on screen so that person sees them, takes a lot as input wtf why am i here its 0:37am xD

def update_input(status, m=None, d=None, p=None, s=None, t=None):

    match mode:
        case "easy":
            bt_easy.config(state=DISABLED)
        case "medium":
            bt_easy.config(state=DISABLED)
        case "hard":
            bt_easy.config(state=DISABLED)
        case "custom":
            bt_easy.config(state=DISABLED)
    
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



if mode == "easy" or "medium" or "hard":
    update_input(DISABLED)

launcher.mainloop()
