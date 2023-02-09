from tkinter import *
import mysql.connector
import csv
from random import randint
import pandas as pd
import pickle
import DB_config as db
import main


def bicreate():
    try:
        with open("db.dat", "rb") as o:
            return
    except:
        db.run()


bicreate()

o = open("db.dat", "rb")
q = pickle.load(o)
o.close()
db_pw = q["pass"]
db_db = q["db"]
db_us = q["user"]
db_hs = q["host"]


def csvcreate():
    try:
        with open("acc.csv", mode="r") as f:
            return
    except:
        with open("acc.csv", mode="w") as f:
            f = csv.writer(f, delimiter=",")
            st = ["slno", "username", "phno", "password"]
            f.writerow(st)


csvcreate()


def sqlcreate():
    try:
        dataBase = mysql.connector.connect(
            host=db_hs, user=db_us, passwd=db_pw, database=db_db
        )

    except:
        dataBase = mysql.connector.connect(host=db_hs, user=db_us, passwd=db_pw)
        mc = dataBase.cursor()
        mc.execute(f"create database {db_db};")
        mc.execute(f"use {db_db}")
        mc.execute(
            "CREATE TABLE acc (username VARCHAR(255) PRIMARY KEY, phno VARCHAR(255), pass VARCHAR(255))ENGINE=InnoDB DEFAULT CHARSET=latin1"
        )
        mc.execute("desc acc;")


print("Correct password")


def w():
    global ro, pp
    ro = Tk()
    ro.title("login")
    ro.geometry("380x400")
    ro.config(bg="black")

    Label(
        ro,
        text="LOGIN IN",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    ).place(x=140, y=20)
    Label(
        ro,
        text="Username",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    ).place(x=20, y=71)
    Label(
        ro,
        text="password",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    ).place(x=20, y=121)

    entry1 = Entry(
        ro, width=12, font=("Arial", 23), borderwidth=2, fg="black", bg="#e4c8e6"
    )
    entry2 = Entry(
        ro,
        width=12,
        font=("Arial", 23),
        borderwidth=2,
        fg="black",
        bg="#e4c8e6",
        show="*",
    )

    entry1.place(x=140, y=70)
    entry2.place(x=140, y=120)

    pp = Label(
        ro,
        text="                      ",
        bg="black",
        fg="white",
        cursor="hand2",
        font=("Arial", 12),
    )
    pp.place(x=30, y=300)

    # show pass
    showme = IntVar(value=0)

    def showp():
        if showme.get() == 1:
            entry2.config(show="")
            entry2.after(1000, lambda: entry2.config(show="*"))
            entry2.after(1000, lambda: show.deselect())

        else:
            entry2.config(show="*")

    show = Checkbutton(
        ro,
        text="show password",
        font=("Arial", 10),
        height=1,
        variable=showme,
        onvalue=1,
        offvalue=0,
        command=lambda: showp(),
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        width=12,
        pady=0,
    )
    show.place(x=20, y=170)

    # hyperlink forgot password
    t = Label(
        ro,
        text="forgot password?",
        bg="black",
        fg="blue",
        cursor="hand2",
        font=("Arial", 10),
    )
    t.place(x=20, y=190)
    # t.bind("<Button-1>",lambda x:webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    t.bind("<Button-1>", lambda x: forgotpass())

    # login
    lb = Button(
        ro,
        text="login",
        font=("Helvetica", 8),
        height=1,
        width=12,
        bg="lightgray",
        activebackground="white",
        borderwidth=0,
        padx=9,
        pady=4,
        relief=GROOVE,
        command=lambda: checkpass(a, b),
    ).place(x=140, y=210)

    # sign up
    Label(
        ro,
        text="did not sign up yet?",
        font=("Arial", 8),
        bg="black",
        fg="white",
        height=1,
        padx=2,
        pady=10,
        width=20,
    ).place(x=125, y=240)

    sp = Button(
        ro,
        text="sign up",
        font=("Helvetica", 8),
        height=1,
        width=12,
        bg="lightgray",
        activebackground="white",
        borderwidth=0,
        padx=9,
        pady=4,
        relief=GROOVE,
        command=lambda: signup(),
    ).place(x=140, y=270)

    a = entry1.get()
    b = entry2.get()

    # C1 = Checkbutton(ro,text="i am not a robot",font=("Arial", 10),height=3,width=14).place(x=20,y=170)
    def checkpass(a, b):
        global pp
        a = entry1.get()
        b = entry2.get()
        a = a.replace(" ", "")
        b = b.replace(" ", "")
        # print(a)
        dataBase = mysql.connector.connect(
            host=db_hs, user=db_us, passwd=db_pw, database=db_db
        )
        mycursor = dataBase.cursor()
        sq = "SELECT * FROM acc WHERE username = %s and pass = %s"
        ad = (
            a,
            b,
        )
        mycursor.execute(sq, ad)
        myresult = mycursor.fetchall()
        dataBase.commit()
        dataBase.close()
        c = mycursor.rowcount
        try:
            if len(a) == 0:
                print("Enter username")
                pp.config(
                    text="                 ----- Enter Username ----- ",
                    bg="black",
                    fg="white",
                )

            elif len(b) == 0:
                print("Enter Password")
                pp.config(
                    text="                 ----- Enter Password ----- ",
                    bg="black",
                    fg="white",
                )

            elif c == 1:
                username = entry1.get()
                password = entry2.get()
                pp.config(
                    text="                 ----- login successful ----- ",
                    bg="black",
                    fg="green",
                )
                ro.destroy()
                main.w(username, password)

            elif c == 0:
                print("Invalid Login Credentials")
                pp.config(
                    text=" ----- Invalid Login Credentials ----- \n Wrong password or username.Try again or \nclick 'forgot password' to recover it",
                    bg="black",
                    fg="red",
                )
        except:
            print("something is wrong")


w()


def forgotpass():

    ro.destroy()
    ro2 = Tk()
    ro2.title("sign up")
    ro2.geometry("380x280")
    ro2.config(bg="black")
    con = False

    fg = Label(
        ro2,
        text="FORGOT PASSWORD",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=18,
    )
    fg.place(x=110, y=20)
    #   Label(ro2,text="RESET PASSWORD",font=("Arial", 10),bg="#FFE5B4",
    #         height=1,padx=2,pady=10,width=18).place(x=110,y=20)

    l1 = Label(
        ro2,
        text="Username",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    )
    l2 = Label(
        ro2,
        text="phone number",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    )

    _1entry1 = Entry(
        ro2, width=12, font=("Arial", 23), borderwidth=2, fg="black", bg="#e4c8e6"
    )
    _1entry2 = Entry(
        ro2, width=12, font=("Arial", 23), borderwidth=2, fg="black", bg="#e4c8e6"
    )

    pp2 = Label(
        ro2,
        text="                      ",
        bg="black",
        fg="white",
        cursor="hand2",
        font=("Arial", 12),
    )
    pp2.place(x=100, y=175)

    def defaultg():
        # grid for lables
        l1.place(x=20, y=81)
        l2.place(x=20, y=131)
        # l3.place(x=20,y=171)

        # grid for entries
        _1entry1.place(x=140, y=80)
        _1entry2.place(x=140, y=130)
        # _1entry3.place(x=140,y=170)

    defaultg()

    un = _1entry1.get()
    pn = _1entry2.get()

    # _1sp.place(x=140,y=330)

    # robo.place(x=120,y=270)

    cpass = Button(
        ro2,
        text="confirm",
        command=lambda: errph(),
        height=1,
        width=19,
        pady=5,
        padx=10,
    )
    cpass.place(x=110, y=210)

    def errph():
        pn = _1entry2.get()
        un = _1entry1.get()
        if un != "":
            pp2.place(x=100, y=175)
            pp2.config(text="")
            try:
                int(pn)
                cb = pn

                if len(cb) < 10:
                    pp2.config(text="--should be a 10 digit number--", fg="red")
                    return

                elif len(cb) > 10:
                    pp2.config(text="--should be a 10 digit number--", fg="red")
                    return

                elif len(cb) == 10:
                    pp2.after(200, lambda: pp2.config(text=".", fg="green"))
                    pp2.after(400, lambda: pp2.config(text="..", fg="green"))
                    pp2.after(600, lambda: pp2.config(text="....", fg="green"))
                    pp2.after(800, lambda: pp2.config(text=".....loading", fg="green"))
                    # pp2.after(1000,lambda:pp2.config(text="......successful",fg="green"))
                    pp2.after(3000, lambda: checkun())

            except:
                pp2.config(text="enter a valid phone number!", fg="red")
                return
        else:
            pp2.config(text="enter a username", fg="red")
            pp2.place(x=120, y=175)

    def checkun():
        un = _1entry1.get()
        dataBase = mysql.connector.connect(
            host=db_hs, user=db_us, passwd=db_pw, database=db_db
        )
        mycursor = dataBase.cursor()
        sq = " Select * FROM acc WHERE username = %s"
        ad = (un,)
        mycursor.execute(
            sq,
            ad,
        )
        myresult = mycursor.fetchall()
        dataBase.commit()
        dataBase.close()
        c1 = mycursor.rowcount

        if c1 == 1:
            # pp2.after(200,lambda:pp2.config(text=".",fg="green"))
            # pp2.after(400,lambda:pp2.config(text="..",fg="green"))
            # pp2.after(600,lambda:pp2.config(text="....",fg="green"))
            # pp2.after(800,lambda:pp2.config(text=".....loading",fg="green"))
            pp2.after(1000, lambda: pp2.config(text="......successful", fg="green"))
            checkphno()
            # ro.destroy()

        elif c1 == 0:
            pp2.config(
                text="dude? seriously?\n atleast type a right username -_-", fg="red"
            )
            pp2.place(x=60, y=175)
            ro2.geometry("380x280")
            cpass.place(x=110, y=225)

    def checkphno():
        un = _1entry1.get()
        pn = _1entry2.get()
        dataBase = mysql.connector.connect(
            host=db_hs, user=db_us, passwd=db_pw, database=db_db
        )
        mycursor = dataBase.cursor()

        sq = "SELECT * FROM acc WHERE username = %s and phno = %s"
        ad = (
            un,
            pn,
        )
        mycursor.execute(sq, ad)
        myresult = mycursor.fetchall()
        dataBase.commit()
        dataBase.close()
        c = mycursor.rowcount
        if c == 1:
            # print("correct password")
            pp2.place(x=60, y=170)
            pp2.after(
                1000,
                lambda: pp2.config(
                    text=" ----- phno matched! ----- ", bg="black", fg="green"
                ),
            )
            pp2.after(1000, lambda: changepass())
            # ro.destroy()
        elif c == 0:
            # print("password is incorrect")
            pp2.after(
                1000,
                lambda: pp2.config(
                    text="Are you sure thats your phone number? \n I guess not.\nCross check!",
                    fg="red",
                ),
            )
            pp2.place(x=60, y=190)
            pp2.config(
                text="Are you sure thats your phone number? \n I guess not.\nCross check!",
                fg="red",
            )
            # pp2.place(x=60,y=190)
            ro2.geometry("380x380")
            cpass.place(x=110, y=250)

    def changepass():
        global asd
        un = _1entry1.get()
        asd = un
        pn = _1entry2.get()

        ro2.geometry("380x250")

        l1.destroy()
        pp2.destroy()
        l2.destroy()
        _1entry2.destroy()
        _1entry1.destroy()
        cpass.destroy()

        res = Button(ro2, text="Change Password", command=lambda: clickcp()).place(
            x=130, y=170
        )
        pp3 = Label(
            ro2,
            text="                     ",
            bg="black",
            fg="white",
            cursor="hand2",
            font=("Arial", 12),
        )
        pp3.place(x=100, y=210)
        fg.config(text="RESET PASSWORD")
        _1entry3 = Entry(
            ro2,
            width=12,
            font=("Arial", 23),
            borderwidth=2,
            fg="black",
            bg="#e4c8e6",
            show="*",
        )

        _1entry3.place(x=80, y=80)

        c_v = IntVar(value=0)

        def my_show():
            if c_v.get() == 1:
                _1entry3.config(show="")
                _1entry3.after(1000, lambda: _1entry3.config(show="*"))
                _1entry3.after(1000, lambda: c1.deselect())

            else:
                _1entry3.config(show="*")

        c1 = Checkbutton(
            ro2,
            text="show password",
            font=("Arial", 10),
            height=1,
            variable=c_v,
            onvalue=1,
            offvalue=0,
            command=lambda: my_show(),
            bg="black",
            fg="white",
            activebackground="black",
            activeforeground="white",
            width=12,
            pady=0,
        )
        c1.place(x=80, y=130)

        bcp = _1entry3.get()

        def clickcp():
            global pb
            bcp = _1entry3.get()
            pb = bcp
            print(pb)

            def up_csv():
                # print("i am running")
                with open("acc.csv", mode="r") as cf:
                    reader = csv.reader(cf, delimiter=",")
                    for line in reader:
                        # print(line)
                        for i in line:
                            if i == asd:
                                x = line[0]
                                # print(x)
                                pddf = pd.read_csv("acc.csv")
                                # print(pddf)
                                pddf.loc[(int(x) - 1), "password"] = pb
                                pddf.to_csv("acc.csv", index=False)

                            else:
                                continue

            while True:
                try:
                    if len(pb) >= 4 and len(pb) <= 20:
                        pp3.after(200, lambda: pp3.config(text=".", fg="green"))
                        pp3.after(400, lambda: pp3.config(text="..", fg="green"))
                        pp3.after(600, lambda: pp3.config(text="....", fg="green"))
                        pp3.after(800, lambda: pp3.config(text=".....", fg="green"))
                        pp3.after(1000, lambda: pp3.config(text="......", fg="green"))
                        pp3.after(1200, lambda: pp3.config(text="........", fg="green"))
                        pp3.after(
                            1400, lambda: pp3.config(text="...........", fg="green")
                        )
                        pp3.after(
                            1600, lambda: pp3.config(text=".............", fg="green")
                        )
                        pp3.after(
                            1800,
                            lambda: pp3.config(
                                text="...............loading", fg="green"
                            ),
                        )
                        pp3.after(
                            2000,
                            lambda: pp3.config(
                                text="............password reset successful", fg="green"
                            ),
                        )

                        up_csv()
                        break
                    elif len(pb) == "":
                        pp3.config(text="         enter a password", fg="red")
                        pp3.after(1000, lambda: pp3.config(text="      "))
                        # print("Enter username")
                        return
                    else:
                        pp3.config(text="         enter a password", fg="red")
                        pp3.after(1000, lambda: pp3.config(text="      "))
                        return
                except ValueError:
                    print("Invalid! ...")
                    return
            dataBase = mysql.connector.connect(
                host=db_hs, user=db_us, passwd=db_pw, database=db_db
            )
            mycursor = dataBase.cursor()
            sql = "UPDATE acc SET pass = %s WHERE username = %s"
            val = (bcp, un)
            mycursor.execute(sql, val)
            dataBase.commit()
            pp3.after(2300, lambda: ro2.destroy())
            pp3.after(2300, lambda: w())


def signup():

    ro.destroy()
    ro1 = Tk()
    ro1.title("sign up")
    ro1.geometry("380x500")
    ro1.config(bg="black")

    Label(
        ro1,
        text="SIGN UP",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    ).place(x=140, y=20)

    l1 = Label(
        ro1,
        text="Username",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    )
    l2 = Label(
        ro1,
        text="phone number",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    )
    l3 = Label(
        ro1,
        text="password",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    )
    l4 = Label(
        ro1,
        text="confirm \npassword",
        font=("Arial", 10),
        bg="#FFE5B4",
        height=1,
        padx=2,
        pady=10,
        width=14,
    )

    _1entry1 = Entry(
        ro1, width=12, font=("Arial", 23), borderwidth=2, fg="black", bg="#e4c8e6"
    )
    _1entry2 = Entry(
        ro1, width=12, font=("Arial", 23), borderwidth=2, fg="black", bg="#e4c8e6"
    )
    _1entry3 = Entry(
        ro1,
        width=12,
        font=("Arial", 23),
        borderwidth=2,
        fg="black",
        bg="#e4c8e6",
        show="*",
    )
    _1entry4 = Entry(
        ro1,
        width=12,
        font=("Arial", 23),
        borderwidth=2,
        fg="black",
        bg="#e4c8e6",
        show="*",
    )

    # button

    _1sp = Button(
        ro1,
        text="sign up",
        font=("Helvetica", 8),
        height=1,
        width=12,
        bg="lightgray",
        activebackground="white",
        borderwidth=0,
        padx=9,
        pady=4,
        relief=GROOVE,
        command=lambda: click(),
    )
    # _1sp.place(x=140,y=330)
    _1sp.config(state=DISABLED)

    def en():
        _1sp.config(state=NORMAL)

    # show pass
    showme = IntVar(value=0)

    def showp():
        if showme.get() == 1:
            _1entry3.config(show="")
            _1entry4.config(show="")
            _1entry3.after(1000, lambda: _1entry3.config(show="*"))
            _1entry4.after(1000, lambda: _1entry4.config(show="*"))
            _1entry4.after(1000, lambda: show.deselect())

        else:
            _1entry3.config(show="*")
            _1entry4.config(show="*")

    show = Checkbutton(
        ro1,
        text="show password",
        font=("Arial", 10),
        height=1,
        variable=showme,
        onvalue=1,
        offvalue=0,
        command=lambda: showp(),
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        width=12,
    )

    # check humoon or not
    robo = Checkbutton(
        ro1,
        text="i am not a robot",
        font=("Arial", 10),
        height=2,
        width=14,
        command=lambda: en(),
    )
    # robo.place(x=120,y=270)

    def defaultg():
        # grid for lables
        l1.place(x=20, y=71)
        l2.place(x=20, y=121)
        l3.place(x=20, y=171)
        l4.place(x=20, y=221)
        # grid for entries
        _1entry1.place(x=140, y=70)
        _1entry2.place(x=140, y=120)
        _1entry3.place(x=140, y=170)
        _1entry4.place(x=140, y=220)
        show.place(x=20, y=270)
        _1sp.place(x=140, y=350)
        robo.place(x=120, y=290)

    defaultg()

    a1 = _1entry1.get()
    b1 = 0
    k = _1entry2.get()
    c1 = _1entry3.get()
    d1 = _1entry4.get()
    print(k)

    s = Label(ro1, text=" ", bg="black", fg="green", font=("Arial", 12))
    s.place(x=20, y=370)

    def addacc(a1, b1, c1):
        dataBase = mysql.connector.connect(
            host=db_hs, user=db_us, passwd=db_pw, database=db_db
        )
        cursorObject = dataBase.cursor()
        sql = "INSERT INTO acc (username, phno, pass) VALUES (%s, %s, %s)"
        val = (a1, b1, c1)
        cursorObject.execute(sql, val)
        dataBase.commit()
        dataBase.close()
        print("account created!!")
        s.after(200, lambda: s.config(text="sign up successful"))
        s.after(2000, lambda: s.destroy())
        ro1.destroy()
        w()

    def add_csv(a1, b1, c1):

        ff = open("acc.csv", mode="r")
        reader = csv.reader(ff, delimiter=",")
        # count_data= [i for i in reader]
        row_count = len(list(reader))

        ff.close()

        st = []
        with open("acc.csv", mode="a") as f:
            f = csv.writer(f, delimiter=",")
            st.append([int(row_count / 2), a1, b1, c1])
            f.writerow(st[0])

    def click():

        a1 = _1entry1.get()
        k = _1entry2.get()
        c1 = _1entry3.get()
        d1 = _1entry4.get()

        # user name
        while True:
            try:
                sca = "`~!#@$%^&*()-=+{}[]:|;'\<>?,/"
                dataBase = mysql.connector.connect(
                    host=db_hs, user=db_us, passwd=db_pw, database=db_db
                )
                mycursor = dataBase.cursor()
                cnt = 0
                s = "SELECT username FROM acc WHERE username = %s"
                ss = (a1,)
                mycursor.execute(s, ss)
                myresult = mycursor.fetchall()
                cnt = mycursor.rowcount
                dataBase.close()
                if a1.isspace():
                    print("your username cant be a blank space")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--your username cant be a blank space--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=121)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return
                elif len(a1) == 0:
                    print("Enter username")
                    robo.deselect()
                    _1sp.config(state=DISABLED)

                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--Enter username--",
                        bg="black",
                        fg="white",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=121)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return
                elif len(a1.split()) > 1:
                    print(
                        "username cannot have spaces \nusername can only contain alphanumeric characters and special characters such as ,_,."
                    )
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="username cannot have spaces \nusername can only contain alphanumeric characters and special characters such as ,_,.",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=20, y=121)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return
                elif len(a1) < 4:
                    print("Should be more than 4 characters ")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--Should be more than 4 characters--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=121)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return
                elif len(a1) > 20:
                    print("Should be less than 20 characters ")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--Should be less than 20 characters--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=121)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return

                elif any(i in sca for i in a1):
                    print(
                        "username cannot have spaces \nusername can only contain alphanumeric characters and special characters such as ,_,."
                    )
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="username cannot have spaces \nusername can only contain alphanumeric characters and special characters such as ,_,.",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=121)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return

                elif cnt == 1:
                    print("The username already exists")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    ran1 = " "
                    cont = 0
                    while True:
                        ran = str(randint(0, 9))
                        cont += 1
                        ran1 += ran
                        if cont == 3:
                            break
                        else:
                            continue
                    # ran2=randint(1,2)
                    a2 = a1 + ran1
                    a3 = ran1 + a1

                    h = Label(
                        ro1,
                        text="--The username already exists--"
                        "\n try adding numerics,_,." + a2 + "or" + a3,
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=20, y=121)
                    h.after(3000, lambda: h.destroy())
                    _1sp.after(3000, lambda: defaultg())

                    return
                elif cnt != 1 and len(a1) >= 4 and len(a1) <= 20:
                    break

                else:
                    print("wrong input")
                    robo.deselect()
                    _1sp.config(state=DISABLED)

                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)

                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)

                    _1sp.place(x=140, y=380)

                    robo.place(x=120, y=320)

                    h = Label(
                        ro1,
                        text="--wrong inout--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=121)

                    h.after(2000, lambda: h.destroy())

                    _1sp.after(2000, lambda: defaultg())

                    return

            except ValueError:
                print("Invalid username! ...")
        # phone number
        while True:
            try:
                int(k)
                # b1 = 0
                b1 = k
                # scb = "`~!@#$%^&*.-={}[]:|;'\<>?,/\""
                if b1 == "":
                    print("Enter your phone number")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--Enter your phone number--",
                        bg="black",
                        fg="white",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=171)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())

                    return

                elif len(b1.split()) > 1:
                    print(
                        "username cannot have spaces \nusername can only contain alphanumeric characters and special characters such as ,_,."
                    )
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="username cannot have spaces \nusername can only contain alphanumeric characters and special characters such as ,_,.",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=20, y=171)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return

                elif len(b1) < 10:
                    print("should be 10 digit number")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--should be 10 digit number--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=171)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return

                elif len(b1) > 10:
                    print("should be a 10 digit number")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--should be a 10 digit number--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=171)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return

                elif len(b1) == 10:
                    print("valid phone number")
                    break

                else:
                    print("something is wrong")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--something is wrong--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=171)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())

                    return

            except:
                print("Invalid number!\n make sure you entered a number ...")
                robo.deselect()
                _1sp.config(state=DISABLED)
                l3.place(x=20, y=221)
                l4.place(x=20, y=271)
                _1entry3.place(x=140, y=220)
                _1entry4.place(x=140, y=270)
                _1sp.place(x=140, y=380)
                robo.place(x=120, y=320)
                h = Label(
                    ro1,
                    text="--Invalid number!\n make sure you entered a number--",
                    bg="black",
                    fg="red",
                    cursor="hand2",
                    font=("Arial", 12),
                )
                h.place(x=60, y=171)
                h.after(2000, lambda: h.destroy())
                _1sp.after(2000, lambda: defaultg())

                return

        # password
        while True:
            try:
                if c1.isspace():
                    print("Try again!")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l2.place(x=20, y=171)
                    l3.place(x=20, y=221)
                    l4.place(x=20, y=271)
                    _1entry2.place(x=140, y=170)
                    _1entry3.place(x=140, y=220)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--Try again!--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=121)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return

                elif len(c1) == 0:
                    print("enter password")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    l4.place(x=20, y=271)
                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--Enter password!--",
                        bg="black",
                        fg="white",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=221)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())

                    return
                elif a1 == c1:
                    print("username cannot be the password")
                    robo.deselect()
                    _1sp.config(state=DISABLED)

                    l4.place(x=20, y=271)

                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--username cannot be the password--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=221)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return
                elif len(c1) >= 4 and len(c1) <= 20:
                    c1 = c1.replace(" ", "")
                    break
                else:
                    print("Cannot have more than 20 characters")
                    robo.deselect()
                    _1sp.config(state=DISABLED)

                    l4.place(x=20, y=271)

                    _1entry4.place(x=140, y=270)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--Cannot have more than 20 characters--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=221)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())

                    return

            except ValueError:
                print("Invalid! ...")

        # conform password
        while True:
            try:
                d1 = d1.replace(" ", "")
                print(c1)
                print(d1)
                if len(d1) == 0:
                    print("Enter the password again!")
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--Enter the password again--",
                        bg="black",
                        fg="white",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=271)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    return
                elif d1 == c1:
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--password matched--",
                        bg="black",
                        fg="green",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=271)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())
                    break

                else:
                    robo.deselect()
                    _1sp.config(state=DISABLED)
                    _1sp.place(x=140, y=380)
                    robo.place(x=120, y=320)
                    h = Label(
                        ro1,
                        text="--password dosent match--",
                        bg="black",
                        fg="red",
                        cursor="hand2",
                        font=("Arial", 12),
                    )
                    h.place(x=60, y=271)
                    h.after(2000, lambda: h.destroy())
                    _1sp.after(2000, lambda: defaultg())

                    return

            except ValueError:
                print("Invalid! ...")

        addacc(a1, b1, c1)
        add_csv(a1, b1, c1)


def run():
    bicreate()
    csvcreate()
    o = open("db.dat", "rb")
    q = pickle.load(o)
    o.close()
    db_pw = q["pass"]
    db_db = q["db"]
    db_us = q["user"]
    db_hs = q["host"]
    sqlcreate()
    w()
    # signup()


ro.mainloop()
