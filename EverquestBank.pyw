from tkinter import *
import sqlite3
import os
from tkinter import ttk
import sqlite3
import csv, sqlite3
from tkinter import filedialog
import time
###################################################################
#Tkinter Set Up

ws = Tk()
ws.title('Eq Inventory Search')
ws.geometry('700x400')
nb = ttk.Notebook(ws)
nb.grid()
Search_Frame = Frame(nb, width=500, height = 500)
Db_Frame = Frame(nb, width=500, height = 500)

Search_Frame.grid()
Db_Frame.grid()

nb.add(Search_Frame, text="Search")
nb.add(Db_Frame, text="Database")

#########################################################################################################
#Search Tab

def myClick(ItemName):

    ItemName = e.get()
    conn = sqlite3.connect(os.path.realpath('Eqinv.db'))
    c = conn.cursor()
    c.execute("SELECT Type,Name,Count,Char FROM Inventory WHERE Name LIKE ?",(f'%{ItemName}%',))
    records = c.fetchall()
    print_records= Listbox(Search_Frame,yscrollcommand=w.set, width = 110, height = 17)
    for record in records:
            print_records.insert(END,str(record) + '\n')
    print_records.grid(row = 5)
    w.config(command = print_records.yview)
    ws.update()
    conn.close()
    

e = Entry(Search_Frame)
e.bind("<Return>",myClick)
e.grid(row = 1)
w = Scrollbar(Search_Frame, orient='vertical')
w.grid(row = 5, column = 1, sticky = 'ns')
Mylabel = Label(Search_Frame, text = "What Item Are You Looking For?", justify= CENTER)
Mylabel.grid(row = 0, padx=250)
Spacelabel = Label(Search_Frame)
Spacelabel.grid(row=4)



####################################################################################################
#Database Set Up

def dbClick():

    ws.filename = filedialog.askopenfilename()
    Playerfile = ws.filename
    PlayerName = str(Playerfile.split("/")[-1])
    PlayerName = str(PlayerName.split("-")[-2])
    PlayerName = str(PlayerName.strip())

    ws.update()
    conn = sqlite3.connect(r"Charpaths.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Charpath(Char string, path string)""")
    c.execute("""INSERT INTO Charpath(path) VALUES(?)""",(Playerfile,))
    conn.commit()
    c.execute("""SELECT * FROM Charpath WHERE path = ?""",(Playerfile,))
    records = c.fetchall()
    conn.close
    conn= sqlite3.connect(r"CharList.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Charlist(Char string)""")
    c.execute("""INSERT INTO Charlist(Char) VALUES(?)""",(PlayerName,))
    conn.commit()
    charlist.delete(0,'end')
    c.execute("SELECT * FROM Charlist")
    records = c.fetchall()
    for record in records:
            charlist.insert(END,str(record[0]) + '\n')
    conn.close()
    ws.update()
    Freshdb()

##########################################################################
#Resetting the Sqlite Character Database
def Resetchar():
    for i in charlist.curselection():
        charname = charlist.get(i)
        print(str(charname.strip()))
        conn= sqlite3.connect(r"CharList.db")
        c = conn.cursor()
        c.execute("""DELETE FROM Charlist WHERE Char = ?""",(str(charname.strip()),))
        c.execute("""CREATE TABLE IF NOT EXISTS Charlist(Char)""")
        conn.commit()
        conn.close()
        conn = sqlite3.connect(r"Charpaths.db")
        c = conn.cursor()
        c.execute("""DELETE FROM Charpath WHERE Char = ?""",(str(charname.strip()),))
        c.execute("""CREATE TABLE IF NOT EXISTS Charpath(Char string,path string)""")
        conn.commit()
        conn.close()
        charlist.delete(charlist.curselection())
        ws.update()
        Freshdb()


###########################################################################
# Recreates the Inventory Database using the Character Database
def Freshdb():
    conn = sqlite3.connect(r"Eqinv.db")
    c = conn.cursor()
    c.execute("""DROP TABLE Inventory""")
    c.execute("""CREATE TABLE IF NOT EXISTS Inventory(Type, Name , ID , Count, Slots, Char)""")
    conn.commit()
    conn.close()
    conn = sqlite3.connect(r"Eqinv.db")
    c = conn.cursor()
    c.execute("""DROP TABLE Inventory""")
    c.execute("""CREATE TABLE IF NOT EXISTS Inventory(Type, Name , ID , Count, Slots,Char)""")
    conn.commit()
    conn.close()
    ws.update()

    conn = sqlite3.connect(r"CharList.db")
    c = conn.cursor()
    c.execute("""SELECT * FROM Charlist""")
    chars = c.fetchall()
    conn.close()
    for record in chars:
        charname = record[0]
        conn = sqlite3.connect(r"Charpaths.db")
        c = conn.cursor()
        c.execute("""SELECT path FROM Charpath""")
        records = c.fetchall()
        conn.close()
        conn = sqlite3.connect(r"Eqinv.db")
        c = conn.cursor()
        for record in records:
            conn = sqlite3.connect(r"Eqinv.db")
            with open(f'{record[0]}', newline = '') as games:                                                                                          
                game_reader = csv.reader(games, delimiter='\t')
                for game in game_reader:
                   
                    c = conn.cursor()
                    c.execute("""INSERT INTO Inventory (Type, Name , ID , Count, Slots) VALUES(?,?,?,?,?)""",game)
                    c.execute("""UPDATE Inventory SET Char = ? WHERE Char is null """,(charname,))
                    c.execute("""DELETE FROM Inventory WHERE Name = 'Empty'""")
                    c.execute("""DELETE FROM Inventory WHERE Type = 'Location'""")
            conn.commit()
            ws.update()

    conn.close()
    ws.update()

######################################################################################
#Button Commands

resetchardata = Button(Db_Frame, text= "Delete Selected Character", command = Resetchar)
resetchardata.grid(row=3)

dbClickButton = Button(Db_Frame, text="Add Character", command=dbClick)
dbClickButton.grid(row = 2)

createfreshdb = Button(Db_Frame, text= "Create Fresh Database From Character List", command=Freshdb)
createfreshdb.grid(row = 4)


##################################################################################################
#Set up the Character List Database and Inventory Database
conn= sqlite3.connect(r"CharList.db")
c = conn.cursor()
charlist=Listbox(Db_Frame, width = 110, height = 17, selectmode=SINGLE)
charlist.grid(row = 6)
c.execute("""CREATE TABLE IF NOT EXISTS Charlist(Char)""")
c.execute("SELECT * FROM Charlist")
records = c.fetchall()
for record in records:
        charlist.insert(END,str(record[0]) + '\n')
conn.commit()
conn.close()
conn = sqlite3.connect(r"Eqinv.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Inventory(Type, Name , ID , Count, Slots, Char)""")
conn.commit()
conn.close()
conn = sqlite3.connect(r"Charpaths.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Charpath(Char string, path string)""")
conn.commit()
conn.close()
ws.update()
ws.mainloop()
