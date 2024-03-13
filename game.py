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
    global highscore
    global online

    global multiply_js
    global divide_js
    global pwr_js
    global sqrt_js
    global timer

    global config_data
    config_data = initconfig()

    for i in config_data["active"]:
        mode = setmode(i["mode"])
        name = setname(i["name"])

    for i in config_data["saved"]:
        highscore = sethighscore(i["highscore"])
        online = setonline(i["online"])

    score = 0


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
    global exitscreen
    global score_info
    global highscore_txt
    global failmessage


    global bg_color_game

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

#Display Highscore right
    highscore_txt = ttk.Label(game, text=f"Highscore: {highscore}", background=bg_color_game, foreground=fg_color_game, font=("Modern", 20, "bold"),)
    highscore_txt.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="e")

#Start window
    start = Frame(game, bg=bg_color_game)
    start.grid(row=2, column=0, columnspan=6, rowspan=3, sticky="n", pady=((Height)/4))

    start_bt = Button(start, bg=bg_color_game, fg=fg_color_game, text="START", font=("Terminal", 50, "bold"), anchor="center", justify="center")
    #this somehow centers the button there probably is a way easier method but this worked so idc
    start_bt.grid(row=2, column=0, columnspan=6, sticky="n", padx=5, pady=5)
    start_bt.config(command=startgame)

    g_info_text = f"Wenn du bereit bist, drücke START! \n Dir werden dann Fragen gestellt, die du im darunter liegenden Eingabefeld beantwortest. \n Bei richtig beantworteten Fragen wird dein Score erhöht! \n Du hast jeweils {timer} Sekunden Zeit um die fragen zu beantworten! "
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
    
    bt_inp = Button(game_r, text="Confirm", bg="#333", fg=fg_color_game, font=("Terminal", 20), command=button_pressed)
    bt_inp.grid(row=4, column=0, columnspan=6, sticky="n", padx=5, pady=15)

#Exit screen
    exitscreen = Frame(game, bg=bg_color_game)
    #is hidden by default
    exitscreen.grid_forget()

    restart_txt = Label(exitscreen, bg=bg_color_game, fg=fg_color_game, text="GAME OVER", font=("Terminal", 50, "bold"), anchor="center", justify="center")
    restart_txt.grid(row=2, column=0, columnspan=6, sticky="n", padx=5, pady=5)

    score_info = Label(exitscreen, bg=bg_color_game, fg="yellow", font=("System", 15))
    score_info.grid(row=3, column=0, columnspan=6, sticky="n", padx=5, pady=5)

    failmessage = Label(exitscreen, bg=bg_color_game, fg="red", font=("System", 15))
    failmessage.grid(row=4, column=0, columnspan=6, sticky="n", padx=5, pady=10)


    restart_bt = Button(exitscreen, text="Restart", bg="#333", fg=fg_color_game, font=("Terminal", 20), command=restartbutton)
    restart_bt.grid(row=5, column=0, columnspan=6, sticky="n", padx=5, pady=15)
    
    
    game.protocol("WM_DELETE_WINDOW", window_close)
    game.mainloop()



#Start Game in sperate thread because it otherwise wont load
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
    global button_pressed_time
    global last_bt_pressed
    global running


    upl = 10
    counter = 0
    #content = p_input.get()

    start.grid_forget()
    game_r.grid(row=2, column=0, columnspan=6, rowspan=3, sticky="n", pady=((Height)/4))
    
    #while True:
    result, op = createnewlevel()
    running = True
    button_pressed_time = None
    last_bt_pressed = None
    checker_thread = threading.Thread(target=check_button, daemon=True)
    checker_thread.start()


def createnewlevel():
    calc, result, op = createcalc()
    updatecalc(calc)
    return result, op


def button_pressed():
    global button_pressed_time
    button_pressed_time = time()

def check_answer():
    global button_pressed_time
    global last_bt_pressed
    global timer
    global result
    global counter
    global score
    global upl
    global op
    global running
    global p_input


    #calculate time difference
    if last_bt_pressed == None:
        time_dif = time() - button_pressed_time
    else:
        time_dif = last_bt_pressed - button_pressed_time
    last_bt_pressed = button_pressed_time
    if (time_dif * -1) < timer:
        answer = float(p_input.get())
        if answer == float(result):
            counter += 1
            #calculate new score
            n_score = calcscore(score, time_dif)
            updatescore(n_score)
            score = n_score
            #every 5 rounds the range is getting increased by 5 and the timer gets a little bit smaller
            if counter%5 == 0:
                upl += 5
                timer = timer * 0.9
            result, op = createnewlevel()
            changebg(True)
            p_input.delete(0, END)
        else:
            running = False
            changebg(False)
            exitgame("Falsche Antwort!!!")
    else:
        running = False
        changebg(False)
        exitgame("Dein Zeit ist abgelaufen!!!")

def check_button():
    global button_pressed_time
    global running
    while running:
        if button_pressed_time:
            check_answer()
            button_pressed_time = None
        sleep(0.1)

def changebg(state):
    global bg_color_game
    if state:
        bg_color_game = "green"
    else:
        bg_color_game = "red"
    game.config(bg=bg_color_game)      
    game.update()
    sleep(0.3)
    bg_color_game = "black"
    game.config(bg=bg_color_game)
    game.update

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
def calcscore(score, r_time):
    global upl
    global op
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




def restartbutton():
    global score
    exitscreen.grid_forget()
    score = 0
    score_txt.config(text=f"Score: {score}")
    start.grid(row=2, column=0, columnspan=6, rowspan=3, sticky="n", pady=((Height)/4))

def exitgame(message):
    global highscore
    #print("Game Over")
    game_r.grid_forget()
    score_info.config(text=f"Dein Score: {score}")
    failmessage.config(text=message)
    exitscreen.grid(row=2, column=0, columnspan=6, rowspan=3, sticky="n", pady=((Height)/4))
    if score > highscore:
        highscore = score
        highscore_txt.config(text=f"Highscore: {highscore}")
        with open("config.json", "r+") as f:
            config = load(f)
            for i in config["saved"]:
                i["highscore"] = score

            f.seek(0)
            dump(config, f, indent=4)
            f.truncate()


#In case I want to add the ability to minimize the launcher window while running the game
def window_close():
    exit = messagebox.askyesno("Exit?", "Willst du das Fenster schließen? \n Es wird alles gespeichert!")
    if exit:
        #launcher.deiconify()
        game.destroy()


if __name__ == "__main__":
    startgamemain()