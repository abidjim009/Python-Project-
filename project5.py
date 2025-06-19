#corona virus live tracker

from tkinter import *
core = Tk()

core.title("Corona virus Information Tracker")

core.geometry('800x500+200+100')

core.configure(bg='#046173 ')
core.iconbitmap('corona.ico')


#Labels
mainlable = Label(core, text = "Corona Virus Live Tracker",font=("Time 20 bold", 30,"bold"), bg= "#05897A", wwidth = 33, fg= "black",bd=5)
mainlable.place(x=0,y=0)

