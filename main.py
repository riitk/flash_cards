from tkinter import *
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
FONT1 = ("Ariel", 40, "italic")
FONT2 = ("Ariel", 60, "bold")

if os.path.isfile("data/words_to_learn.csv"):
    data = pandas.read_csv("data/words_to_learn.csv")
else:
    data = pandas.read_csv("data/spanish_data.csv")
to_learn = data.to_dict(orient="records")
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(card_title, text="Spanish", fill='black')
    canvas.itemconfig(card_word, text=current_card['Spanish'], fill='black')
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(card_title, text="English", fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')
    canvas.itemconfig(card_img, image=card_back_img)


def is_known():
    global current_card
    spanish = current_card['Spanish']

    if not os.path.isfile("data/words_to_learn.csv"):
        data.to_csv("data/words_to_learn.csv", mode='a', index=False, header=True)
    else:
        words_to_learn = pandas.read_csv("data/words_to_learn.csv")
        words_to_learn.drop(index=words_to_learn.index[(words_to_learn['Spanish'] == spanish)], axis=0, inplace=True)
        words_to_learn.to_csv("data/words_to_learn.csv", mode='w', index=False, header=True)
    next_card()


# --------------------------------------- UI SETUP ----------------------------------------#


window = Tk()
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)
window.title("Flashy")
window.minsize()
flip_timer = window.after(3000, func=flip_card)


# Images
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file=r"images/card_back.png")
right_img = PhotoImage(file="images/right.png")
wrong_img = PhotoImage(file="images/wrong.png")


canvas = Canvas(height=526, width=800, highlightthickness=0, background=BACKGROUND_COLOR)
card_img = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=FONT1)
card_word = canvas.create_text(400, 263, text="", font=FONT2)
canvas.grid(row=0, column=0, columnspan=2)


# --------------------------------------- BUTTON ----------------------------------------#

wrong_button = Button(image=wrong_img, highlightthickness=0, background=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(row=1, column=0)

check_button = Button(image=right_img, highlightthickness=0, background=BACKGROUND_COLOR, command=is_known)
check_button.grid(row=1, column=1)

next_card()
window.mainloop()
