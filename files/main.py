from tkinter import *
import mysql.connector
from PIL import ImageTk, Image
from tkinter import messagebox
import admin
import pickle
import DB_config as db

try:
    o = open("db.dat", "rb")
    q = pickle.load(o)
    o.close()
    db_pw = q["pass"]
    db_db = q["db"]
    db_us = q["user"]
    db_hs = q["host"]
except:
    db.run()

def w(username, password):
    global root, haha, button_back, button_forward
    root = Tk()
    root.geometry("300x450")
    root.config(bg="black")
    root.title("BookMyShow.com")

    label = Label(
        root,
        text="BookMyShow.com",
        width=25,
        height=2,
        font=("Arial", 14, "bold"),
        padx=2,
    )
    label.grid(row=0, column=0, columnspan=3)

    haha = 0

    Label(
        text="----------------------------------------------------",
        font=("Arial", 9),
        bg="black",
        fg="white",
    ).grid(row=1, column=0, columnspan=3)
    Label(
        text="----------------------------------------------------",
        font=("Arial", 9),
        bg="black",
        fg="white",
    ).grid(row=6, column=0, columnspan=3)
    button_back = Button(root, text="<<", command=lambda: back())
    button_forward = Button(root, text=">>", command=lambda: forward())

    def check():
        st, st1 = admin.movie_urls()
        if haha == 0:
            button_back.config(state=DISABLED)
        else:
            button_back.config(state=NORMAL)

        if haha == (len(st) - 1):
            button_forward.config(state=DISABLED)
        else:
            button_forward.config(state=NORMAL)

    check()

    def forward():
        global haha, button_forward
        haha += 1
        check()
        showing()

    def back():
        global haha, button_back
        haha -= 1
        check()
        showing()

    def showing():
        frame = Canvas(width=240, height=300, bg="gray")
        frame.grid(row=2, column=0, columnspan=3, rowspan=3)
        # frame.place(anchor='center', relx=0.5, rely=0.5)

        st, st1 = admin.movie_urls()

        image2 = Image.open(st[haha])
        image1 = image2.resize((225, 285))

        image_no_1 = ImageTk.PhotoImage(image1)
        # image_no_1 = ImageTk.PhotoImage(Image.open(haha))
        # image1=image_no_1.resize((240,300))
        frame.create_image(10, 10, anchor=NW, image=image_no_1)
        frame.image = image_no_1
        hahan = st1[haha]
        hahan1 = st[haha]

        # buttonm=Button(text="makeout\n ----click to book----",command=lambda:book()).grid(row=5,column=0,columnspan=3)
        buttonm = Button(
            text=hahan + "\n ----click to book----",
            command=lambda: [des(), admin.book(hahan, hahan1)],
        ).grid(row=5, column=0, columnspan=3)
        button = Button(text="❌", command=lambda: delete_acc()).place(x=10, y=10)

        def delete_acc():
            res = messagebox.askquestion(
                "Delete Account", "Do you really want to delete your acc?"
            )
            if res == "yes":
                dataBase = mysql.connector.connect(
                    host=db_hs, user=db_us, passwd=db_pw, database=db_db
                )
                mycursor = dataBase.cursor()
                s = "DELETE FROM acc WHERE username = %s and pass = %s"
                v = (username, password)
                mycursor.execute(s, v)
                dataBase.commit()
                dataBase.close()
                print("Account deleted!!")
            elif res == "no":
                messagebox.showinfo("Return", "Not deleting acc")

        def des():
            root.destroy()

    showing()

    button_back.place(x=0, y=200)
    button_forward.place(x=273, y=200)
    root.mainloop()
