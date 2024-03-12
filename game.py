from json import *
import multiprocessing
from random import randint
import threading
from time import *
from tkinter import *
from tkinter import ttk

from launcher import *

def startgamemain():
    global score
    global mode
    global name

    global multiply_js
    global divide_js
    global pwr_js
    global sqrt_js
    global timer
    

    score = 0

    global config_data
    config_data = initconfig()

    for i in config_data["active"]:
        mode = setmode(i["mode"])
        name = setname(i["name"])

    match mode:
        case "easy":
            multiply_js, divide_js, pwr_js, sqrt_js, timer = seteasy()
            initgamegui()
        case "medium":
            multiply_js, divide_js, pwr_js, sqrt_js, timer = setmedium()
            initgamegui()
        case "hard":
            multiply_js, divide_js, pwr_js, sqrt_js, timer = sethard()
            initgamegui()
        case "custom":
            multiply_js, divide_js, pwr_js, sqrt_js, timer = setcustom()
            initgamegui()


    #print(f"Mode: {mode}, Name {name}")

def initgamegui():
    global game
    global start
    global game_r
    global Height
    global Width
    global calc
    global p_input
    global score_txt

    bg_color_game = "black"
    fg_color_game = "white"
    calculation = "None"


    game = Tk()
    game.title("Kopfrechentrainer Launcher")
    game.config(bg=bg_color_game)
    game.resizable(False,False)
    game.state("zoomed")

    Height = game.winfo_screenheight()
    Width = game.winfo_screenheight()

    #Create Grid
    for i in range(6):
        if i == 0:
            game.columnconfigure(i, weight=1)
        else:
            game.columnconfigure(i, weight=6)

#Display Score left
    score_txt = ttk.Label(game, text=f"Score: {score}", background=bg_color_game, foreground=fg_color_game, font=("Modern", 20, "bold"),)
    score_txt.grid(row=0, column=0, padx=5, pady=5)

#Display Mode in Center
    mode_txt = ttk.Label(game, text=mode.upper(), anchor="center", background=bg_color_game, foreground=fg_color_game, font=("Modern", 20, "bold"))
    mode_txt.grid(padx=5, pady=5, row=0, column=0, columnspan=6, sticky="n")

#Display Username right
    name_txt = ttk.Label(game, text=f"Username: {name}", background=bg_color_game, foreground=fg_color_game, font=("Modern", 20, "bold"),)
    name_txt.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="e")

#Start window
    start = Frame(game, bg=bg_color_game)
    start.grid(row=2, column=0, columnspan=6, rowspan=3, sticky="n", pady=((Height)/4))

    start_bt = Button(start, bg=bg_color_game, fg=fg_color_game, text="START", font=("Terminal", 50, "bold"), anchor="center", justify="center")
    #this somehow centers the button there probably is a way easier method but this worked so idc
    start_bt.grid(row=2, column=0, columnspan=6, sticky="n", padx=5, pady=5)
    start_bt.config(command=startgame)

    g_info_text = "Wenn du bereit bist, drücke START! \n Dir werden dann Fragen gestellt, die du im darunter liegenden Eingabefeld beantwortest. \n Bei richtig beantworteten Fragen wird dein Score erhöht!  "
    g_info = Label(start, bg=bg_color_game, fg=fg_color_game, text=g_info_text, font=("System", 15))
    g_info.grid(row=3, column=0, columnspan=6, sticky="n", padx=5, pady=5)

#Game window
    game_r = Frame(game, bg=bg_color_game)
    #is hidden by default
    game_r.grid_forget()

    calc = Label(game_r, bg=bg_color_game, fg=fg_color_game, text=calculation, font=("Terminal", 50, "bold"), anchor="center", justify="center")
    calc.grid(row=2, column=0, columnspan=6, sticky="n", padx=5, pady=5)

    p_input = Entry(game_r, bg="#333", fg=fg_color_game, font=("Terminal", 20))
    p_input.grid(row=3, column=0, columnspan=6, sticky="n", padx=5, pady=20)
    
    bt_inp = Button(game_r, text="Confirm", bg="#333", fg=fg_color_game, font=("Terminal", 20), command=getcontentonpress)
    bt_inp.grid(row=4, column=0, columnspan=6, sticky="n", padx=5, pady=15)
    
    game.protocol("WM_DELETE_WINDOW", window_close)
    game.mainloop()

def startgamethread():
    threading.Thread(target=startgame).start()


#actuall game
def startgame():
    global timer
    global upl
    global result
    global op
    global counter
    global score
    global timer_thread
    global won
    global check

    upl = 10
    counter = 0
    #content = p_input.get()

    start.grid_forget()
    game_r.grid(row=2, column=0, columnspan=6, rowspan=3, sticky="n", pady=((Height)/4))
    t = multiprocessing.Queue()
    timer_thread = multiprocessing.Process(target=starttimer,daemon=True, args=(t, ))
    
    while True:
        won = False
        check = False
        calc, result, op = createcalc()
        updatecalc(calc)
        timer_thread.start()
        checker_thread = threading.Thread(target=constant_check)
        checker_thread.start()
        checker_thread.join()
        if check == False:
            exitgame()
            break

def constant_check():
    while (timer - t.get()) <= 0:
        if won == True:
            check = True
            timer_thread.terminate()
    

def getcontentonpress():
    global content
    content = p_input.get()
    checkresult(content)


def checkresult(inp):
    global result
    global counter
    global score
    global upl
    global t
    global timer_thread
    global won
    if float(inp) == float(result):
        counter += 1
        #calculate new score
        n_score = calcscore(score)
        updatescore(n_score)
        score = n_score
        #every 5 rounds the range is getting increased by 5 and the timer gets a little bit smaller
        if counter%5 == 0:
            upl += 5
            #timer = timer * 0.9
        won = True
        print("LEts go ")




def starttimer(t):
    time = 0
    while True:
        time += 1
        t.put(time)
        sleep(1)
        #print(r_time)



def exitgame():
    print("Game Over")

#func to create new calculation
def createcalc():
    modes = [multiply_js, divide_js, pwr_js, sqrt_js]
    r_calc = randint(0,3)
    while modes[r_calc] != 1:
        r_calc = randint(0,3)
    else:
        match r_calc:
            case 0:
                n1 = randint(1, upl)
                n2 = randint(1, upl)
                result = n1 * n2
                op = 3
                calc = f"{n1} * {n2}"
            case 1:
                n1 = randint(1, upl)
                n2 = randint(1, upl)
                result = float(n1 / n2)
                result = round(result, 1)
                op = 3
                calc = f"{n1} / {n2}"
            case 2:
                n1 = randint(1, upl)
                n2 = 2
                result = n1 ** n2
                op = 3
                calc = f"{n1}^{n2}"
            case 3:
                n1 = randint(1, upl)
                result = n1
                op = 4
                calc = f"sqrt({n1**2})"

    #op is only used to get a good score
    return calc, result, op

#func to calc new score
def calcscore(score):
    global r_time
    global upl
    global op
    r_time = 4
    """
    Die score-Berechnung folgt folgendem schema:
    - bei jeder richtigen Rechnung wird 10 addiert
    - die Schwerness wird mit 0.3 multipliziert, damit diese ebenso miteinfließt
    - die Restzeit wird ebenso mit 0.7 multipliziert, womit sie mehr gewichtet ist und somit mehr in den score einfließt
    - die Zahlenrange wird ebenso mit 0.6 multipliziert, damit es auch in betracht gezogen wird
    """
    n_score = score + 10 + (r_time*0.7) + (upl*0.6) + (op*0.3)
    n_score = round(n_score, 0)
    return n_score
    

#func to update calc with correct calculation
def updatecalc(calculation):
    calc.config(text=calculation)
    game_r.update()
    game.update()

#func to update score
def updatescore(score):
    score_txt.config(text=f"Score: {score}")
    game.update()



#In case I want to add the ability to minimize the launcher window while running the game
def window_close():
    exit = messagebox.askyesno("Exit?", "Willst du das Fenster schließen? \n Es wird alles gespeichert!")
    if exit:
        #launcher.deiconify()
        game.destroy()


if __name__ == "__main__":
    startgamemain()