from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
start_pressed = False

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, start_pressed
    reps = 0
    start_pressed = False
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_label.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- #

def skip():
    global start_pressed
    window.after_cancel(timer)
    start_pressed = False
    start_timer()
def start_timer():
    global reps, start_pressed
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    while not start_pressed:
        start_pressed = True
        if reps in (1, 3, 5, 7):
            count_down(work_sec)
            title_label.config(text="Work", fg=YELLOW)
        elif reps == 8:
            count_down(long_break_sec)
            title_label.config(text="Break", fg=RED)
        elif reps in (2, 4, 6):
            count_down(short_break_sec)
            title_label.config(text="Break", fg=GREEN)
        else:
            reset_timer()

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    min = math.floor(count / 60)
    sec = count % 60
    if sec < 10:
        sec = f"0{sec}"
    canvas.itemconfig(timer_text, text=f"{min}:{sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        mark = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            mark += "✔"
        check_label.config(text=mark, font=(FONT_NAME, 10, "bold"))

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=PINK)

canvas = Canvas(width=200, height=224, bg=PINK, highlightthickness=0)
pic = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=pic)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)

title_label = Label(text="Timer", bg=PINK, fg=GREEN, font=(FONT_NAME, 50, "bold"))
title_label.grid(column=1, row=0)

check_label = Label(bg=PINK, fg=GREEN)
check_label.grid(column=1, row=3)

start_button = Button(text="Start", fg = "black", bg="white", font=("arial", 10), command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", fg = "black", bg="white", font=("arial", 10), command=reset_timer)
reset_button.grid(column=2, row=2)

skip_button = Button(text="Skip", fg="black", bg="white", font=("arial", 10), command=skip)
skip_button.grid(column=1, row=2)

window.mainloop()
