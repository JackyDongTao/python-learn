# Gui 上实现一个猜字小游戏
from tkinter import *

import tkinter.simpledialog as dl
import tkinter.messagebox as mb

root = Tk()
w = Label(root, text = "Guess Number Game!")
w.pack()

mb.showinfo("Welcome", "Welcome to Guess Number Game!")

number = 23
while True:
    guess = dl.askinteger("Number","What's your guess?")

    if guess == number:
       output = 'you guessed it right.'
       mb.showinfo("Hint", output)
       break

    elif guess < number:
         output = 'no! the number is higher than that.'
         mb.showinfo("Hint", output)
    else:
        output = 'no! the number is lower than that.'
        mb.showinfo("Hint", output)

print('Done')

