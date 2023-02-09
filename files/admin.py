import functools
from tkinter import *
from tkinter import messagebox
import mysql.connector
import csv
import os
from random import randint
from datetime import datetime
from PIL import ImageTk, Image

booked_movies = []
booked_movies2 = []
names_booked_movies2 = []

book1 = []
dic = {}
pay = 0
time = 0


def ticketscountLUX1(a, b):
    daddy = "BCDEFGHIJKLM"
    if a + str(b) not in dic:
        if b > 6:
            dic[a + str(b)] = 0
        else:
            dic[a + str(b)] = 0

    # print(dic)
    # print(book1)

    def select():
        book1.append(a + str(b))
        if a == "A":
            row = 0
            if b > 6:
                Button(
                    sframe1,
                    text=str(b),
                    bg="green",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, "A", int(b)),
                ).grid(row=row, column=b)
            else:
                Button(
                    sframe1,
                    text=str(b),
                    bg="green",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, "A", int(b)),
                ).grid(row=row, column=b - 1)

        elif a in daddy:
            if b > 6:
                Button(
                    bframe1,
                    text=str(b),
                    bg="green",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, a, int(b)),
                ).grid(row=daddy.index(a), column=b)
            else:
                Button(
                    bframe1,
                    text=str(b),
                    bg="green",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, a, int(b)),
                ).grid(row=daddy.index(a), column=b - 1)
        dic[a + str(b)] = 1

    def deselect():
        book1.remove(a + str(b))
        if a == "A":
            row = 0
            if b > 6:
                Button(
                    sframe1,
                    text=str(b),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, "A", int(b)),
                ).grid(row=row, column=b)
            else:
                Button(
                    sframe1,
                    text=str(b),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, "A", int(b)),
                ).grid(row=row, column=b - 1)

        elif a in daddy:
            if b > 6:
                Button(
                    bframe1,
                    text=str(b),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, a, int(b)),
                ).grid(row=daddy.index(a), column=b)
            else:
                Button(
                    bframe1,
                    text=str(b),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, a, int(b)),
                ).grid(row=daddy.index(a), column=b - 1)
        dic[a + str(b)] = 0

    # select()
    if dic[a + str(b)] == 0:
        select()
    else:
        deselect()


def ticketscountLUX2(a, b, c):
    daddy = "BCDEFGHIJKLM"

    if c == bframe2:
        if a + str(b + 14) not in dic:
            dic[a + str(b + 14)] = 0
    else:
        if a + str(b) not in dic:
            dic[a + str(b)] = 0

    def select():
        if a == "A":
            row = 0
            Button(
                c,
                text=str(b),
                bg="green",
                fg="white",
                height=1,
                width=3,
                command=functools.partial(ticketscountLUX2, "A", int(b), c),
            ).grid(row=row, column=b - 1)
            book1.append(a + str(b))
            dic[a + str(b)] = 1

        elif a in daddy:
            if c == bframe1:
                Button(
                    c,
                    text=str(b),
                    bg="green",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX2, a, int(b), c),
                ).grid(row=daddy.index(a), column=b - 1)
                book1.append(a + str(b))
                dic[a + str(b)] = 1

            else:
                Button(
                    c,
                    text=str(b + 14),
                    bg="green",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX2, a, int(b), c),
                ).grid(row=daddy.index(a), column=b - 1)
                book1.append(a + str(b + 14))
                dic[a + str(b + 14)] = 1

        # print(dic)

    def deselect():
        if a == "A":
            row = 0
            Button(
                c,
                text=str(b),
                bg="black",
                fg="white",
                height=1,
                width=3,
                command=functools.partial(ticketscountLUX2, "A", int(b), c),
            ).grid(row=row, column=b - 1)
            book1.remove(a + str(b))
            dic[a + str(b)] = 0

        elif a in daddy:
            if c == bframe1:
                Button(
                    c,
                    text=str(b),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX2, a, int(b), c),
                ).grid(row=daddy.index(a), column=b - 1)
                book1.remove(a + str(b))
                dic[a + str(b)] = 0

            else:
                Button(
                    c,
                    text=str(b + 14),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX2, a, int(b), c),
                ).grid(row=daddy.index(a), column=b - 1)
                book1.remove(a + str(b + 14))
                dic[a + str(b + 14)] = 0

    # select()
    if c != bframe2:
        if dic[a + str(b)] == 0:
            select()
        else:
            deselect()
    else:
        if dic[a + str(b + 14)] == 0:
            select()
        else:
            deselect()


def csvcreate_movie():
    try:
        with open("admin_movie.csv", mode="r") as f:
            return

    except:
        with open("admin_movie.csv", mode="a") as f:
            f = csv.writer(f, delimiter=",")
            st = ["slno", "movie_name", "image_url"]
            f.writerow(st)


csvcreate_movie()


def movie_urls():
    st = []
    st1 = []
    count = 0
    count2 = 0
    with open("admin_movie.csv", mode="r") as cf:
        reader = csv.reader(cf, delimiter=",")
        for line in reader:
            count2 += 1
            if count2 > 1:
                st.append(line[-1])
                st1.append(line[-2])
                count += 1
                if count > 4:
                    break
    return st, st1


def movie1():
    global sframe1, bframe1, ro
    ro = Tk()
    ro.geometry("480x595")
    ro.title("BookMyShow.com")
    ro.config(bg="black")

    Label(ro, text="      ", width=70, height=2, borderwidth=5, bg="black").place(
        x=0, y=504
    )
    Label(ro, text="screen", width=65, height=1, borderwidth=5, bg="gray").place(
        x=5, y=511
    )
    but = Button(
        ro,
        text="Proceed to payment",
        width=65,
        height=1,
        borderwidth=5,
        bg="red",
        command=lambda: timecec(),
    )
    but.place(x=5, y=540)

    def timecec():
        if time == 0:
            messagebox.showinfo("showinfo", "PLEASE SELECT A TIME!")
        else:
            food()

    # time
    morningb = Button(
        text="Morning",
        bg="black",
        fg="#39ac56",
        borderwidth="2",
        relief=RAISED,
        command=lambda: morning(),
        disabledforeground="white",
        height=1,
        width=8,
        font=("ariel", 12, "bold"),
    )
    morningb.grid(row=0, column=1, sticky=W)

    eveningb = Button(
        text="Evening",
        bg="black",
        fg="#39ac56",
        borderwidth="2",
        relief=RAISED,
        command=lambda: evening(),
        disabledforeground="white",
        height=1,
        width=8,
        font=("ariel", 12, "bold"),
    )
    eveningb.grid(row=0, column=2, sticky=W)

    secoundb = Button(
        text="Second",
        bg="black",
        fg="#39ac56",
        borderwidth="2",
        relief=RAISED,
        command=lambda: secound(),
        disabledforeground="white",
        height=1,
        width=8,
        font=("ariel", 12, "bold"),
    )
    secoundb.grid(row=0, column=3, sticky=W)

    Button(
        text="Timing:",
        bg="black",
        fg="#39ac56",
        disabledforeground="#39ac56",
        borderwidth="2",
        relief=RAISED,
        height=1,
        width=8,
        font=("ariel", 12, "bold"),
        state=DISABLED,
    ).grid(row=0, column=0, sticky=W)
    # Button(text="Timing:",bg="black",fg="#39ac56",disabledforeground="#39ac56",borderwidth="2",relief=RAISED,height=1,width=8,font=("ariel",12,"bold"),command=lambda:B1()).grid(row=0,column=0,sticky=W)

    def morning():
        global time
        morningb.config(bg="#39ac56")
        morningb.config(state=DISABLED)
        eveningb.config(state=NORMAL)
        secoundb.config(state=NORMAL)
        eveningb.config(bg="black")
        secoundb.config(bg="black")
        time = 1
        return

    def evening():
        global time
        eveningb.config(bg="#39ac56")
        morningb.config(state=NORMAL)
        eveningb.config(state=DISABLED)
        secoundb.config(state=NORMAL)
        morningb.config(bg="BLACK")
        secoundb.config(bg="black")
        time = 2
        return

    def secound():
        global time
        secoundb.config(bg="#39ac56")
        morningb.config(state=NORMAL)
        eveningb.config(state=NORMAL)
        secoundb.config(state=DISABLED)
        morningb.config(bg="BLACK")
        eveningb.config(bg="black")
        time = 3
        return

    # frame
    frame = Frame(ro, bg="black", width=500, height=470)
    frame.grid(row=1, column=0, columnspan=18)
    sframe1 = Frame(frame, bg="black", width=440, height=25)
    sframe1.place(x="40", y="40")
    bframe1 = Frame(frame, bg="black", width=440, height=440)
    bframe1.place(x="40", y="110")

    def b1():
        daddy = "BCDEFGHIJKLM"
        for row in daddy:
            for coulmn in range(13):
                if coulmn > 6:
                    Button(
                        bframe1,
                        text=str(coulmn),
                        bg="black",
                        fg="white",
                        height=1,
                        width=3,
                        command=functools.partial(ticketscountLUX1, row, int(coulmn)),
                    ).grid(row=daddy.index(row), column=coulmn)
                elif coulmn == 6:
                    Button(
                        bframe1,
                        text="   stairs    ",
                        bg="black",
                        fg="gray",
                        height=1,
                        width=8,
                        state=DISABLED,
                    ).grid(row=daddy.index(row), column=coulmn)
                else:
                    Button(
                        bframe1,
                        text=str(coulmn + 1),
                        bg="black",
                        fg="white",
                        height=1,
                        width=3,
                        command=functools.partial(
                            ticketscountLUX1, row, int(coulmn + 1)
                        ),
                    ).grid(row=daddy.index(row), column=coulmn)

    nameingframe = Frame(frame, bg="black", width=30, height=470)
    nameingframe.place(x="3", y="40")
    nameingframe1 = Frame(frame, bg="black", width=30, height=470)
    nameingframe1.place(x="3", y="110")

    def s1():
        a = "A"
        row = 0
        for coulmn in range(13):
            if coulmn > 6:
                Button(
                    sframe1,
                    text=str(coulmn),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, "A", int(coulmn)),
                ).grid(row=row, column=coulmn)
            elif coulmn == 6:
                Button(
                    sframe1,
                    text="   stairs    ",
                    bg="black",
                    fg="gray",
                    height=1,
                    width=8,
                    state=DISABLED,
                ).grid(row=row, column=coulmn)
            else:
                Button(
                    sframe1,
                    text=str(coulmn + 1),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(ticketscountLUX1, "A", int(coulmn + 1)),
                ).grid(row=row, column=coulmn)

    def naming():
        daddy = "BCDEFGHIJKLM"
        Button(
            nameingframe, text="A", state=DISABLED, bg="black", fg="white", height=1
        ).pack(fill="x")
        for i in daddy:
            Button(
                nameingframe1, text=i, state=DISABLED, bg="black", fg="white", height=1
            ).pack(fill="x")

    naming()
    s1()
    b1()
    Label(
        ro,
        text="Exclusive-Rs:250",
        width=12,
        height=1,
        borderwidth=5,
        bg="black",
        fg="gray",
    ).place(x=3, y=44)
    Label(
        ro,
        text="Normal-Rs:200",
        width=12,
        height=1,
        borderwidth=5,
        bg="black",
        fg="gray",
    ).place(x=3, y=110)

    ro.mainloop()


def movie2():

    global sframe1, bframe1, bframe2, ro
    ro = Tk()
    ro.geometry("650x590")
    ro.title("BookMyShow.com")
    ro.config(bg="black")

    def timecec():
        if time == 0:
            messagebox.showinfo("showinfo", "PLEASE SELECT A TIME!")
        else:
            if len(book1) > 1:
                food()
            else:
                messagebox.showinfo(
                    "showinfo", "Want to check out without selecting a seat?"
                )

    # time
    morningb = Button(
        text="Morning",
        bg="black",
        fg="#39ac56",
        borderwidth="2",
        relief=RAISED,
        command=lambda: morning(),
        disabledforeground="white",
        height=1,
        width=8,
        font=("ariel", 12, "bold"),
    )
    morningb.grid(row=0, column=1, sticky=W)

    eveningb = Button(
        text="Evening",
        bg="black",
        fg="#39ac56",
        borderwidth="2",
        relief=RAISED,
        command=lambda: evening(),
        disabledforeground="white",
        height=1,
        width=8,
        font=("ariel", 12, "bold"),
    )
    eveningb.grid(row=0, column=2, sticky=W)

    secoundb = Button(
        text="Second",
        bg="black",
        fg="#39ac56",
        borderwidth="2",
        relief=RAISED,
        command=lambda: secound(),
        disabledforeground="white",
        height=1,
        width=8,
        font=("ariel", 12, "bold"),
    )
    secoundb.grid(row=0, column=3, sticky=W)

    Button(
        text="Timing:",
        bg="black",
        fg="#39ac56",
        disabledforeground="#39ac56",
        borderwidth="2",
        relief=RAISED,
        height=1,
        width=8,
        font=("ariel", 12, "bold"),
        state=DISABLED,
    ).grid(row=0, column=0, sticky=W)

    def morning():
        global time
        morningb.config(bg="#39ac56")
        morningb.config(state=DISABLED)
        eveningb.config(state=NORMAL)
        secoundb.config(state=NORMAL)
        eveningb.config(bg="black")
        secoundb.config(bg="black")
        time = 1

        return

    def evening():
        global time
        eveningb.config(bg="#39ac56")
        morningb.config(state=NORMAL)
        eveningb.config(state=DISABLED)
        secoundb.config(state=NORMAL)
        morningb.config(bg="BLACK")
        secoundb.config(bg="black")
        time = 2

        return

    def secound():
        global time
        secoundb.config(bg="#39ac56")
        morningb.config(state=NORMAL)
        eveningb.config(state=NORMAL)
        secoundb.config(state=DISABLED)
        morningb.config(bg="BLACK")
        eveningb.config(bg="black")
        time = 3

        return

    frame = Frame(ro, bg="black", width=650, height=470)
    frame.grid(row=1, column=0, columnspan=18)

    nameingframe1 = Frame(frame, bg="black", width=30, height=470)
    nameingframe1.place(x="3", y="40")
    nameingframe2 = Frame(frame, bg="black", width=30, height=470)
    nameingframe2.place(x="3", y="129")

    def naming1():
        daddy = "BCDEFGHIJKL"

        b1 = Button(
            nameingframe1, text="A", state=DISABLED, bg="black", fg="white", height=1
        ).pack(fill="x")

        for i in daddy:
            Button(
                nameingframe2, text=i, state=DISABLED, bg="black", fg="white", height=1
            ).pack(fill="x")

    naming1()

    sframe1 = Frame(frame, bg="black", width=440, height=25)
    sframe1.place(x=169, y="40")

    def s1():

        a = "A"
        while True:
            row = 0
            for coulmn in range(15):
                Button(
                    sframe1,
                    text=str(coulmn + 1),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(
                        ticketscountLUX2, a, int(coulmn + 1), sframe1
                    ),
                ).grid(row=row, column=coulmn)
            if coulmn == 14:
                break

    s1()

    bframe1 = Frame(frame, bg="black", width=435, height=311)
    bframe1.place(x="50", y="129")

    def b1():
        daddy = "BCDEFGHIJKL"
        for row in daddy:
            for coulmn in range(14):
                Button(
                    bframe1,
                    text=str(coulmn + 1),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(
                        ticketscountLUX2, row, int(coulmn + 1), bframe1
                    ),
                ).grid(row=daddy.index(row), column=coulmn)

    b1()

    bframe2 = Frame(frame, bg="black", width=90, height=311)
    bframe2.place(x=545, y="129")

    def b2():
        daddy = "BCDEFGHIJKL"
        for row in daddy:
            for coulmn in range(3):
                Button(
                    bframe2,
                    text=str(coulmn + 15),
                    bg="black",
                    fg="white",
                    height=1,
                    width=3,
                    command=functools.partial(
                        ticketscountLUX2, row, int(coulmn + 1), bframe2
                    ),
                ).grid(row=daddy.index(row), column=coulmn)

    b2()

    Label(
        ro,
        text="Royal-Rs:250",
        width=12,
        height=1,
        borderwidth=5,
        bg="black",
        fg="gray",
    ).place(x=3, y=44)
    Label(
        ro,
        text="Normal-Rs:200",
        width=12,
        height=1,
        borderwidth=5,
        bg="black",
        fg="gray",
    ).place(x=3, y=133)

    Label(ro, text="      ", width=70, height=2, borderwidth=5, bg="black").place(
        x=0, y=504
    )
    Label(ro, text="screen", width=69, height=1, borderwidth=5, bg="gray").place(
        x=70, y=511
    )

    Button(
        ro,
        text="Proceed to payment",
        width=68,
        height=1,
        borderwidth=5,
        bg="red",
        command=lambda: timecec(),
    ).place(x=70, y=540)

    ro.mainloop()


# movie2()


def food():
    global cartlist
    # bevrage dump
    selectedcl = ["coffee: \n"]
    selectedsl = ["Smoothie: \n"]
    selectedsml = ["Mils Shakes: \n"]
    selectedrl = ["Refresher: \n"]
    selectedcbl = ["Chocolate bliss: \n"]
    selectedsdl = {}

    # fastfood dump
    selectedchickenl = ["chicken: \n"]
    selectedtacol = ["taco \n"]
    selectedfrieslist = ["fries \n"]
    selected_sandwitchlist = ["sandwitch \n"]
    selectedburgerlist = ["burger \n"]
    selectedpizzalist = ["pizza \n"]
    selectedpastrieslist = ["pastries \n"]
    selectedicecreamlist = ["icecream \n"]

    # dump
    cartlist = []
    selectedsnacksl = ["Snacks: \n"]

    hop = Tk()
    hop.geometry("300x180")
    hop.title("order food")
    hop.config(bg="black")

    Label(hop, text="                  ", bg="black").pack()
    Label(hop, text="Do you want to add on food?").pack()
    Label(hop, text="                  ", bg="black").pack()
    Button(hop, text="Yes", command=lambda: yes()).pack()
    Label(hop, text="                  ", bg="black").pack()
    Button(hop, text="No", command=lambda: [nope(), ticketbill()]).pack()

    def nope():
        try:
            ro.destroy()
            hop.destroy()
            # ticketbill()
        except:
            try:
                hop.destroy()
            except:
                try:
                    cart.destroy()
                except:
                    try:
                        hop1.destroy()
                    except:
                        try:
                            hop2.destroy()
                        except:
                            pass

    def yes():
        global hop1
        nope()

        hop1 = Tk()
        hop1.geometry("400x350")
        hop1.title("oder food")
        hop1.config(bg="black")

        Label(
            hop1,
            text="BookMyShow.food.com",
            height=2,
            font=("Algerian", 20, "bold"),
            bg="black",
            fg="white",
        ).pack()
        Label(hop1, text="        ", bg="black").pack()
        Button(hop1, text="Dessert", width=15, command=lambda: dessert()).pack()
        Button(hop1, text="Fast Food", width=15, command=lambda: fastfood()).pack()
        Button(hop1, text="Desi Snacks", width=15, command=lambda: desisnacks()).pack()
        Button(hop1, text="Beverage", width=15, command=lambda: beverage()).pack()
        Label(hop1, text="        ", bg="black").pack()
        Button(hop1, text="Go To Cart", command=lambda: cart(), width=25).pack()
        Label(hop1, text="        ", bg="black").pack()
        Button(
            hop1, text="Cancel", bg="red", command=lambda: [nope(), food()], width=25
        ).pack()

        def dessert():
            global hop2
            nope()
            hop2 = Tk()
            hop2.geometry("400x300")
            hop2.title("oder Desert")
            hop2.config(bg="black")
            Label(
                hop2,
                text="Choose Your Choice!",
                height=2,
                font=("Helvetica", 12, "bold"),
                bg="black",
                fg="white",
            ).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Icecream", width=15, command=lambda: icecream()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Pastries", width=15, command=lambda: pastries()).pack()
            Label(hop2, text="        ", bg="black").pack()

            def icecream():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x310")
                hop2.title("order Icecream")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="Icecream",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                icecreamlist = [
                    ["Butterscotch icecream", 129],
                    ["Chocolate icecream", 149],
                    ["Vanilla icecream", 110],
                    ["Strawberry icecream", 139],
                    ["Mint chocolate chip icecream", 149],
                    ["Cookies n' Cream incecream", 169],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedicecreamlist.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedicecreamlist.remove(s)

                def fucCon():
                    print(selectedicecreamlist)

                for item in icecreamlist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], icecreamlist.index(item)
                        ),
                    ).grid(row=icecreamlist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=icecreamlist.index(item), column=1)

                for item in icecreamlist:
                    for item1 in selectedicecreamlist:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], icecreamlist.index(item)
                                ),
                            ).grid(row=icecreamlist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=icecreamlist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), fastfood()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def pastries():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x285")
                hop2.title("order Pastries")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="pastry",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                pastrieslist = [
                    ["Pineapple pastry", 119],
                    ["Butterscotch pastry", 149],
                    ["Chocolate pastry", 139],
                    ["Red velvet pastry", 149],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedpastrieslist.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedpastrieslist.remove(s)

                def fucCon():
                    print(selectedpastrieslist)

                for item in pastrieslist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], pastrieslist.index(item)
                        ),
                    ).grid(row=pastrieslist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=pastrieslist.index(item), column=1)

                for item in pastrieslist:
                    for item1 in selectedpastrieslist:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], pastrieslist.index(item)
                                ),
                            ).grid(row=pastrieslist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=pastrieslist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), fastfood()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            Button(hop2, text="Go To Cart", width=25, command=lambda: cart()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(
                hop2, text="Cancel", bg="red", command=lambda: nope(), width=25
            ).pack()
            Button(
                hop2,
                text="<-- back",
                bg="black",
                fg="white",
                command=lambda: [nope(), yes()],
                width=15,
            ).pack(side=LEFT)

        def fastfood():
            global hop2
            nope()
            hop2 = Tk()
            hop2.geometry("400x500")
            hop2.title("oder Fast Food")
            hop2.config(bg="black")
            Label(
                hop2,
                text="Choose Your Choice!",
                height=2,
                font=("Helvetica", 12, "bold"),
                bg="black",
                fg="white",
            ).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Burgers", width=15, command=lambda: burger()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Pizza", width=15, command=lambda: pizza()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Taco", width=15, command=lambda: taco()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Sandwitch", width=15, command=lambda: sandwitch()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(
                hop2, text="Fries", width=15, command=lambda: fries()
            ).pack()  # make sure to put tea asshole
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="KFC", width=15, command=lambda: chicken()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Go To Cart", width=25, command=lambda: cart()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(
                hop2, text="Cancel", bg="red", command=lambda: nope(), width=25
            ).pack()
            Button(
                hop2,
                text="<-- back",
                bg="black",
                fg="white",
                command=lambda: [nope(), yes()],
                width=15,
            ).pack(side=LEFT)

            def burger():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x400")
                hop2.title("order Burger")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="Burger",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                burgerlist = [
                    ["Aaloo patty", 269],
                    ["vegie cheese", 299],
                    ["Aaloo Paneer patty", 170],
                    ["American chicken(non veg)", 399],
                    ["Chicken burger(non veg)", 349],
                    ["Veg zinger burger", 320],
                    ["Classic zinger(non veg)", 360],
                    ["Chicken crisp(non veg)", 420],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=24,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedburgerlist.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=24,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedburgerlist.remove(s)

                def fucCon():
                    print(selectedburgerlist)

                for item in burgerlist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=24,
                        command=functools.partial(
                            fuc, item[0], item[1], burgerlist.index(item)
                        ),
                    ).grid(row=burgerlist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=burgerlist.index(item), column=1)

                for item in burgerlist:
                    for item1 in selectedburgerlist:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=24,
                                command=functools.partial(
                                    deselect, item[0], item[1], burgerlist.index(item)
                                ),
                            ).grid(row=burgerlist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=burgerlist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=24
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), fastfood()],
                    width=24,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def pizza():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x310")
                hop2.title("order Pizza")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="Pizza",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                pizzalist = [
                    ["Onion pizza", 199],
                    ["Paneer pizza", 229],
                    ["Plane cheese pizza", 149],
                    ["Chicken pizza(non veg)", 299],
                    ["Extra cheese chicken pizza(non veg)", 399],
                    ["Chicken lasyn", 399],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedpizzalist.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedpizzalist.remove(s)

                def fucCon():
                    print(selectedpizzalist)

                for item in pizzalist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], pizzalist.index(item)
                        ),
                    ).grid(row=pizzalist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=pizzalist.index(item), column=1)

                for item in pizzalist:
                    for item1 in selectedpizzalist:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], pizzalist.index(item)
                                ),
                            ).grid(row=pizzalist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=pizzalist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), fastfood()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def sandwitch():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x285")
                hop2.title("order fast food")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="Tacos",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                sandwichlist = [
                    ["Veg sandwich", 179],
                    ["Double cheese(veg)", 249],
                    ["Chicken sandwich(non veg)", 299],
                    ["Grilled chicken(non veg)", 319],
                    ["Italian sandwich", 210],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=25,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selected_sandwitchlist.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=25,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selected_sandwitchlist.remove(s)

                def fucCon():
                    print(selected_sandwitchlist)

                for item in sandwichlist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=25,
                        command=functools.partial(
                            fuc, item[0], item[1], sandwichlist.index(item)
                        ),
                    ).grid(row=sandwichlist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=sandwichlist.index(item), column=1)

                for item in sandwichlist:
                    for item1 in selected_sandwitchlist:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=25,
                                command=functools.partial(
                                    deselect, item[0], item[1], sandwichlist.index(item)
                                ),
                            ).grid(row=sandwichlist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=sandwichlist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=25
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), fastfood()],
                    width=25,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def fries():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x285")
                hop2.title("fries")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="Tacos",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                frieslist = [
                    ["Peri Peri fries", 299],
                    ["Shezwaan fries", 350],
                    ["Masala fries", 289],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedfrieslist.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedfrieslist.remove(s)

                def fucCon():
                    print(selectedfrieslist)

                for item in frieslist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], frieslist.index(item)
                        ),
                    ).grid(row=frieslist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=frieslist.index(item), column=1)

                for item in frieslist:
                    for item1 in selectedfrieslist:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], frieslist.index(item)
                                ),
                            ).grid(row=frieslist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=frieslist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), fastfood()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def taco():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x285")
                hop2.title("order taco")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="Tacos",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                tacolist = [
                    ["Soft taco", "139"],
                    ["Soft Taco supreme", "209"],
                    ["Crunchy taco", "139"],
                    ["Nacho Cheese", "199"],
                    ["Dorito Supreme x6", "281"],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedtacol.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedtacol.remove(s)

                def fucCon():
                    print(selectedtacol)

                for item in tacolist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], tacolist.index(item)
                        ),
                    ).grid(row=tacolist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=tacolist.index(item), column=1)

                for item in tacolist:
                    for item1 in selectedtacol:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], tacolist.index(item)
                                ),
                            ).grid(row=tacolist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=tacolist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), fastfood()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def chicken():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x285")
                hop2.title("order KFC")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="KFC",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                chickenlist = [
                    ["Boneless Strips x8", "249"],
                    ["Hotwings x6", "249"],
                    ["Hot & Crispy Wings x8", "469"],
                    ["Grilled x6", "281"],
                    ["Nugget x6", "281"],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedchickenl.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedchickenl.remove(s)

                def fucCon():
                    print(selectedchickenl)

                for item in chickenlist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], chickenlist.index(item)
                        ),
                    ).grid(row=chickenlist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=chickenlist.index(item), column=1)

                for item in chickenlist:
                    for item1 in selectedchickenl:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], chickenlist.index(item)
                                ),
                            ).grid(row=chickenlist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=chickenlist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), fastfood()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

        def desisnacks():
            global hop2
            nope()
            hop2 = Tk()
            hop2.geometry("500x390")
            hop2.title("oder Snacks")
            hop2.config(bg="black")
            Label(
                hop2,
                text="                       ",
                height=1,
                font=("Helvetica", 14, "bold"),
                bg="black",
                fg="white",
            ).pack()
            Label(
                hop2,
                text="MENU",
                height=1,
                font=("Helvetica", 20, "bold", "underline"),
                bg="black",
                fg="white",
            ).pack()
            Label(
                hop2,
                text="DESI INDIAN SNACKS",
                height=1,
                font=("Helvetica", 14, "bold"),
                bg="black",
                fg="white",
            ).pack()
            Label(
                hop2,
                text="                       ",
                height=1,
                font=("Helvetica", 14, "bold"),
                bg="black",
                fg="white",
            ).pack()

            snackslist = [
                ["Samosa", "69"],
                ["Samosa chat", "79"],
                ["Bhel chat", "89"],
                ["vada pav", "99"],
                ["Dahi Vada", "119"],
                ["Pav bhaji", "119"],
            ]

            frame3 = Frame(hop2, bg="white", width=200, height=100)
            frame3.pack()
            canvas1 = Canvas(frame3, bg="white", width=200, height=100)
            frame1 = Frame(canvas1, bg="white")

            def fuc(a, b, c):
                s = []
                s.append(a)
                s.append(b)
                Button(
                    frame1,
                    text=a,
                    bg="green",
                    fg="white",
                    width=20,
                    command=lambda: deselect(a, b, c),
                ).grid(row=c, column=0)
                Button(
                    frame1,
                    text=b,
                    bg="green",
                    disabledforeground="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=c, column=1)
                selectedsnacksl.append(s)

            def deselect(a, b, c):
                s = []
                s.append(a)
                s.append(b)
                Button(
                    frame1,
                    text=a,
                    bg="black",
                    fg="white",
                    width=20,
                    command=functools.partial(fuc, a, b, c),
                ).grid(row=c, column=0)
                Button(
                    frame1,
                    text=b,
                    bg="black",
                    disabledforeground="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=c, column=1)
                selectedsnacksl.remove(s)

            for item in snackslist:
                Button(
                    frame1,
                    text=item[0],
                    bg="black",
                    fg="white",
                    width=20,
                    command=functools.partial(
                        fuc, item[0], item[1], snackslist.index(item)
                    ),
                ).grid(row=snackslist.index(item), column=0)
                Button(
                    frame1,
                    text=item[1],
                    bg="black",
                    disabledforeground="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=snackslist.index(item), column=1)

            for item in snackslist:
                for item1 in selectedsnacksl:
                    if item == item1:
                        Button(
                            frame1,
                            text=item[0],
                            bg="green",
                            fg="white",
                            width=20,
                            command=functools.partial(
                                deselect, item[0], item[1], snackslist.index(item)
                            ),
                        ).grid(row=snackslist.index(item), column=0)
                        Button(
                            frame1,
                            text=item[1],
                            bg="green",
                            disabledforeground="white",
                            width=15,
                            state=DISABLED,
                        ).grid(row=snackslist.index(item), column=1)

            frame3.pack()
            canvas1.grid(row=0, column=0, columnspan=2)
            frame1.pack()
            Button(
                frame3, text="Go To Cart", bg="red", command=lambda: cart(), width=20
            ).grid(row=11, column=0)
            Button(
                frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
            ).grid(row=11, column=1)

            Button(
                frame3,
                text="<-- back",
                bg="black",
                fg="white",
                command=lambda: [nope(), yes()],
                width=20,
            ).grid(row=12, column=0)
            Button(
                frame3,
                text="        ",
                bg="black",
                fg="white",
                width=15,
                state=DISABLED,
            ).grid(row=12, column=1)

        def beverage():

            global hop2
            nope()
            hop2 = Tk()
            hop2.geometry("400x500")
            hop2.title("oder Beverage")
            hop2.config(bg="black")
            Label(
                hop2,
                text="Choose Your Choice!",
                height=2,
                font=("Helvetica", 12, "bold"),
                bg="black",
                fg="white",
            ).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Soft drinks", width=15, command=lambda: soft()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Coffee", width=15, command=lambda: coffee()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(
                hop2, text="Milk Shakes", width=15, command=lambda: milkshakes()
            ).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Smoothie", width=15, command=lambda: smoothie()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(
                hop2, text="Refreshers", width=15, command=lambda: refresh()
            ).pack()  # make sure to put tea asshole
            Label(hop2, text="        ", bg="black").pack()
            Button(
                hop2, text="Chocolate Bliss", width=15, command=lambda: chocolatebliss()
            ).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(hop2, text="Go To Cart", width=25, command=lambda: cart()).pack()
            Label(hop2, text="        ", bg="black").pack()
            Button(
                hop2, text="Cancel", bg="red", command=lambda: nope(), width=25
            ).pack()
            Button(
                hop2,
                text="<-- back",
                bg="black",
                fg="white",
                command=lambda: [nope(), yes()],
                width=15,
            ).pack(side=LEFT)

            def soft():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("335x400")
                hop2.title("oder Beverage")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="SOFT DRINKS",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()
                frame1 = Frame(hop2, bg="black", width=200, height=200)
                frame1.pack(side=LEFT)
                frame2 = Frame(hop2, bg="black", width=200, height=200)
                frame2.pack(side=RIGHT)
                Label(
                    frame1,
                    text="Item",
                    width=15,
                    pady=4,
                    padx=3,
                    bg="black",
                    fg="white",
                    borderwidth=1,
                ).grid(row=0, column=0)

                def fuc1(a, b):
                    s = {}
                    s[a] = b
                    selectedsdl[softdrinkslist.index(b)] = s
                    print(selectedsdl)
                    select()

                Label(
                    frame2,
                    text="Small",
                    width=9,
                    pady=4,
                    padx=3,
                    bg="black",
                    fg="white",
                    borderwidth=1,
                ).grid(row=0, column=0)
                Label(
                    frame2,
                    text="Medium",
                    width=9,
                    pady=4,
                    padx=3,
                    bg="black",
                    fg="white",
                    borderwidth=1,
                ).grid(row=0, column=1)
                Label(
                    frame2,
                    text="Big",
                    width=9,
                    pady=4,
                    padx=3,
                    bg="black",
                    fg="white",
                    borderwidth=1,
                ).grid(row=0, column=2)
                softdrinkslist = [
                    ["Coke", 45, 75, 99],
                    ["Pepsi", 45, 75, 99],
                    ["Fanta", 45, 75, 99],
                    ["Sprite", 45, 75, 99],
                    ["Mountain Due", 45, 75, 99],
                    ["Blue Berry", 45, 75, 99],
                    ["Prime", 45, 75, 99],
                ]
                for item in softdrinkslist:
                    Button(frame1, text=item[0], width=15, state=DISABLED).grid(
                        row=softdrinkslist.index(item) + 1, column=0
                    )
                    Button(
                        frame2,
                        text=item[1],
                        width=9,
                        command=functools.partial(fuc1, item[1], item),
                    ).grid(row=softdrinkslist.index(item) + 1, column=0)
                    Button(
                        frame2,
                        text=item[2],
                        width=9,
                        command=functools.partial(fuc1, item[2], item),
                    ).grid(row=softdrinkslist.index(item) + 1, column=1)
                    Button(
                        frame2,
                        text=item[3],
                        width=9,
                        command=functools.partial(fuc1, item[3], item),
                    ).grid(row=softdrinkslist.index(item) + 1, column=2)

                def select():
                    for item in softdrinkslist:
                        for j in selectedsdl.values():
                            # print(j)
                            if item in j.values():
                                Button(
                                    frame1,
                                    text=item[0],
                                    width=15,
                                    state=DISABLED,
                                    background="black",
                                    disabledforeground="white",
                                ).grid(row=softdrinkslist.index(item) + 1, column=0)
                                Button(
                                    frame2,
                                    text=item[1],
                                    width=9,
                                    command=functools.partial(fuc1, item[1], item),
                                    background="black",
                                    foreground="white",
                                ).grid(row=softdrinkslist.index(item) + 1, column=0)
                                Button(
                                    frame2,
                                    text=item[2],
                                    width=9,
                                    command=functools.partial(fuc1, item[2], item),
                                    background="black",
                                    foreground="white",
                                ).grid(row=softdrinkslist.index(item) + 1, column=1)
                                Button(
                                    frame2,
                                    text=item[3],
                                    width=9,
                                    command=functools.partial(fuc1, item[3], item),
                                    background="black",
                                    foreground="white",
                                ).grid(row=softdrinkslist.index(item) + 1, column=2)
                                for item1 in j.keys():
                                    if item1 == item[1]:
                                        Button(
                                            frame2,
                                            text=item[1],
                                            width=9,
                                            command=functools.partial(
                                                fuc1, item[1], item
                                            ),
                                            background="green",
                                            foreground="white",
                                        ).grid(
                                            row=softdrinkslist.index(item) + 1, column=0
                                        )
                                    elif item1 == item[2]:
                                        Button(
                                            frame2,
                                            text=item[2],
                                            width=9,
                                            command=functools.partial(
                                                fuc1, item[2], item
                                            ),
                                            background="green",
                                            foreground="white",
                                        ).grid(
                                            row=softdrinkslist.index(item) + 1, column=1
                                        )
                                    else:
                                        Button(
                                            frame2,
                                            text=item[3],
                                            width=9,
                                            command=functools.partial(
                                                fuc1, item[3], item
                                            ),
                                            background="green",
                                            foreground="white",
                                        ).grid(
                                            row=softdrinkslist.index(item) + 1, column=2
                                        )

                select()

                Button(
                    frame1, text="Confirm", bg="red", command=lambda: fucCon(), width=15
                ).grid(row=11, column=0)
                Button(
                    frame2, text="Cancel", bg="red", command=lambda: nope(), width=30
                ).grid(row=11, column=0, columnspan=3)

                Button(
                    frame1,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), beverage()],
                    width=15,
                ).grid(row=12, column=0)
                Button(
                    frame2,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=30,
                    state=DISABLED,
                ).grid(row=12, column=0, columnspan=3)

                def fucCon():
                    print(selectedsdl)
                    cartlist.append(selectedsdl)

            def coffee():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x480")
                hop2.title("oder Beverage")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="COFFEE",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                coffeelist = [
                    ["Filter Coffee", "69"],
                    ["Cold coffee", "79"],
                    ["Cappuccino", "89"],
                    ["Flat White", "139"],
                    ["Soya Cappuccino", "119"],
                    ["Inverted Cappuccino", "119"],
                    ["Honey Cinnamon", "119"],
                    ["Cafee Latte", "119"],
                    ["Vanilla Cappuccino", "119"],
                    ["Vanilla Latte", "119"],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedcl.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedcl.remove(s)

                def fucCon():
                    print(selectedcl)
                    cartlist.append(selectedcl)

                for item in coffeelist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], coffeelist.index(item)
                        ),
                    ).grid(row=coffeelist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=coffeelist.index(item), column=1)

                for item in coffeelist:
                    for item1 in selectedcl:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], coffeelist.index(item)
                                ),
                            ).grid(row=coffeelist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=coffeelist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), beverage()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def milkshakes():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x700")
                hop2.title("oder Beverage")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="MILK SHAKES",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                shakeslist = [
                    ["Vanilla Milkshake", "150"],
                    ["Mango Milkshake", "150"],
                    ["Banana Milkshake", "150"],
                    ["Chocolate Milkshake", "150"],
                    ["Caramel Milkshake", "160"],
                    ["Oreo Milkshake", "160"],
                    ["Kit Kat Milkshake", "160"],
                    ["Bubblegum Milkshake", "160"],
                    ["Choco Milkshake", "160"],
                    ["Blueberry Milkshake", "160"],
                    ["Nutella Milkshake", "160"],
                    ["Brownie Milkshake", "170"],
                    ["Brownie Mint Milkshake", "170"],
                    ["Choco Banana Milkshake", "170"],
                    ["Death by Chocolate", "190"],
                    ["Swedo Choco Chip", "190"],
                    ["Ferro Hazelnut", "220"],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                scrol = Scrollbar(frame3, orient=VERTICAL, command=canvas1.yview)
                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedsl.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedsl.remove(s)

                def fucCon():
                    print(selectedsl)
                    cartlist.append(selectedsl)

                for item in shakeslist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], shakeslist.index(item)
                        ),
                    ).grid(row=shakeslist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=shakeslist.index(item), column=1)

                for item in shakeslist:
                    for item1 in selectedsl:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], shakeslist.index(item)
                                ),
                            ).grid(row=shakeslist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=shakeslist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), beverage()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def smoothie():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x280")
                hop2.title("oder Beverage")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="SMOOTIE",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                smoothielist = [
                    ["Strawberry smoothie", "150"],
                    ["Mango Smoothie", "150"],
                    ["Banana Smoothie", "150"],
                    ["Blue Berry Smoothie", "150"],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                scrol = Scrollbar(frame3, orient=VERTICAL, command=canvas1.yview)
                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedsml.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedsml.remove(s)

                def fucCon():
                    print(selectedsml)
                    cartlist.append(selectedsml)

                for item in smoothielist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], smoothielist.index(item)
                        ),
                    ).grid(row=smoothielist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=smoothielist.index(item), column=1)

                for item in smoothielist:
                    for item1 in selectedsml:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], smoothielist.index(item)
                                ),
                            ).grid(row=smoothielist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=smoothielist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), beverage()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def refresh():

                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x280")
                hop2.title("oder Beverage")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="REFRESHERS",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                refreshlist = [
                    ["Lemonade", "181"],
                    ["Berry", "181"],
                    ["Strawberry Breeze", "181"],
                    ["Watermelon", "181"],
                    ["Green Tea", "181"],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                scrol = Scrollbar(frame3, orient=VERTICAL, command=canvas1.yview)
                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=20,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedrl.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedrl.remove(s)

                def fucCon():
                    print(selectedrl)
                    cartlist.append(selectedrl)

                for item in refreshlist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=20,
                        command=functools.partial(
                            fuc, item[0], item[1], refreshlist.index(item)
                        ),
                    ).grid(row=refreshlist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=refreshlist.index(item), column=1)

                for item in refreshlist:
                    for item1 in selectedrl:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect, item[0], item[1], refreshlist.index(item)
                                ),
                            ).grid(row=refreshlist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=refreshlist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=20
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), beverage()],
                    width=20,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

            def chocolatebliss():
                global hop2
                nope()
                hop2 = Tk()
                hop2.geometry("500x280")
                hop2.title("oder Beverage")
                hop2.config(bg="black")
                Label(
                    hop2,
                    text="MENU",
                    height=1,
                    font=("Helvetica", 20, "bold", "underline"),
                    bg="black",
                    fg="white",
                ).pack()
                Label(
                    hop2,
                    text="REFRESHERS",
                    height=1,
                    font=("Helvetica", 14, "bold"),
                    bg="black",
                    fg="white",
                ).pack()

                chocolateblisslist = [
                    ["Gourment Belgian Hot Chocolte", "240"],
                    ["Gourment Belgian Cold Chocolte", "233"],
                    ["Chocolate Overload Drink", "243"],
                ]

                frame3 = Frame(hop2, bg="white", width=200, height=100)

                canvas1 = Canvas(frame3, bg="white", width=200, height=100)

                frame1 = Frame(canvas1, bg="white")

                scrol = Scrollbar(frame3, orient=VERTICAL, command=canvas1.yview)
                canvas1.create_window((0, 0), window=frame1, anchor="nw")

                def fuc(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="green",
                        fg="white",
                        width=25,
                        command=lambda: deselect(a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="green",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedcbl.append(s)

                def deselect(a, b, c):
                    s = []
                    s.append(a)
                    s.append(b)
                    Button(
                        frame1,
                        text=a,
                        bg="black",
                        fg="white",
                        width=25,
                        command=functools.partial(fuc, a, b, c),
                    ).grid(row=c, column=0)
                    Button(
                        frame1,
                        text=b,
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=c, column=1)
                    selectedcbl.remove(s)

                def fucCon():
                    print(selectedcbl)
                    cartlist.append(selectedcbl)

                for item in chocolateblisslist:
                    Button(
                        frame1,
                        text=item[0],
                        bg="black",
                        fg="white",
                        width=25,
                        command=functools.partial(
                            fuc, item[0], item[1], chocolateblisslist.index(item)
                        ),
                    ).grid(row=chocolateblisslist.index(item), column=0)
                    Button(
                        frame1,
                        text=item[1],
                        bg="black",
                        disabledforeground="white",
                        width=15,
                        state=DISABLED,
                    ).grid(row=chocolateblisslist.index(item), column=1)

                for item in chocolateblisslist:
                    for item1 in selectedcbl:
                        if item == item1:
                            Button(
                                frame1,
                                text=item[0],
                                bg="green",
                                fg="white",
                                width=20,
                                command=functools.partial(
                                    deselect,
                                    item[0],
                                    item[1],
                                    chocolateblisslist.index(item),
                                ),
                            ).grid(row=chocolateblisslist.index(item), column=0)
                            Button(
                                frame1,
                                text=item[1],
                                bg="green",
                                disabledforeground="white",
                                width=15,
                                state=DISABLED,
                            ).grid(row=chocolateblisslist.index(item), column=1)

                frame3.pack()
                canvas1.grid(row=0, column=0, columnspan=2)
                frame1.pack()
                Button(
                    frame3, text="Confirm", bg="red", command=lambda: fucCon(), width=25
                ).grid(row=11, column=0)
                Button(
                    frame3, text="Cancel", bg="red", command=lambda: nope(), width=15
                ).grid(row=11, column=1)

                Button(
                    frame3,
                    text="<-- back",
                    bg="black",
                    fg="white",
                    command=lambda: [nope(), yes(), beverage()],
                    width=25,
                ).grid(row=12, column=0)
                Button(
                    frame3,
                    text="        ",
                    bg="black",
                    fg="white",
                    width=15,
                    state=DISABLED,
                ).grid(row=12, column=1)

        def cart():
            try:
                cartlist.pop(0)
                cartlist[0] = selectedcbl
                cartlist.pop(1)
                cartlist[1] = selectedcl
                cartlist.pop(2)
                cartlist[2] = selectedrl
                cartlist.pop(3)
                cartlist[3] = selectedsl
                cartlist.pop(4)
                cartlist[4] = selectedsml
                cartlist.pop(5)
                cartlist[5] = selectedsdl.values()

                cartlist.pop(6)
                cartlist[6] = selectedsnacksl

                cartlist.pop(7)
                cartlist[7] = selectedchickenl
                cartlist.pop(8)
                cartlist[8] = selectedtacol
                cartlist.pop(9)
                cartlist[9] = selectedfrieslist
                cartlist.pop(10)
                cartlist[10] = selected_sandwitchlist
                cartlist.pop(11)
                cartlist[11] = selectedburgerlist
                cartlist.pop(12)
                cartlist[12] = selectedpastrieslist
                cartlist.pop(13)
                cartlist[13] = selectedpizzalist
                cartlist.pop(14)
                cartlist[14] = selectedicecreamlist

            except:
                cartlist.append(selectedcbl)
                cartlist.append(selectedcl)
                cartlist.append(selectedrl)
                cartlist.append(selectedsl)
                cartlist.append(selectedsml)
                cartlist.append(selectedsdl.values())

                cartlist.append(selectedsnacksl)

                cartlist.append(selectedchickenl)
                cartlist.append(selectedtacol)
                cartlist.append(selectedfrieslist)
                cartlist.append(selected_sandwitchlist)
                cartlist.append(selectedburgerlist)
                cartlist.append(selectedpastrieslist)
                cartlist.append(selectedpizzalist)
                cartlist.append(selectedicecreamlist)

            rcart()
            """ 
            for i in cartlist:
                if 1 < len(i):
                    for j in i:
                        print(j)
            
            print("\n\n\n")
            print(cartlist)
           payment()

        def payment():
            global totalcost
            totalcost=0
            print(cartlist)
            for i in cartlist:
                if 1 < len(i):
                    if i is list:
                        for j in i:
                            totalcost += 1
                            if j != i[0]:
                                try:
                                    totalcost += j[1]
                                except:
                                    totalcost += int(j[1])

                    if i is not list:
                        for j in i:
                            for k in j:
                                try:
                                    totalcost += k
                                except:
                                    totalcost += int(k)
                            
            print(totalcost)
            """

        def rcart():
            global frame, cart
            # cartlist1=[['Chocolate bliss:'], ['coffee:', ['Flat White', '139'], ['Honey Cinnamon', '119'], ['Cafee Latte', '119'], ['Soya Cappuccino', '119'], ['Inverted Cappuccino', '119']], ['Refresher: '], ['Smoothie: '], ['Chocolate bliss: '], ['coffee: ', ['Flat White', '139'], ['Honey Cinnamon', '119'], ['Cafee Latte', '119'], ['Soya Cappuccino', '119'], ['Inverted Cappuccino', '119']], ['Refresher: '], ['Smoothie: '], ['Mils Shakes: '], ['Snacks: ', ['Samosa chat', '79'], ['Bhel chat', '89'], ['Dahi Vada', '119']], ['chicken: \n'], ['taco \n']]

            nope()
            cartlist1 = cartlist
            for i in cartlist1:
                if len(i) > 1:  # and i is list:
                    for j in i:
                        if j != i[0]:
                            j.append(1)
            cart = Tk()
            cart.geometry("400x280")
            cart.title("cart")
            cart.config(bg="black")
            cart1 = Frame(cart, bg="black")
            cart1.pack()

            Button(
                cart1,
                text="<-",
                bg="black",
                fg="white",
                height=3,
                command=lambda: [nope(), yes()],
            ).grid(row=0, column=0)
            Label(cart1, text="   ", bg="black", fg="white", height=3, width=8).grid(
                row=0, column=1
            )

            Button(
                cart1,
                text="CHECKOUT",
                height=1,
                font=("Helvetica", 20, "bold", "underline"),
                bg="black",
                fg="white",
                command=lambda: payment(),
            ).grid(row=0, column=2)

            # creating a main frame

            main_frame = Frame(cart, bg="black")
            main_frame.pack(fill=BOTH, expand=1)

            # create a canvas

            main_canvas = Canvas(main_frame, bg="black")
            main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            # create a scroll bar and configuring

            scroll = Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
            scroll.pack(side=RIGHT, fill=Y)

            main_canvas.configure(yscrollcommand=scroll.set)

            main_canvas.bind(
                "<Configure>",
                lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")),
            )

            # another frame and adding to the canvas window
            frame = Frame(main_canvas, bg="black")

            main_canvas.create_window((0, 0), window=frame, anchor=NW)

            def adds(a, b, c):
                a += 1
                cartlist1[b][c][1] = (int(cartlist1[b][c][1]) / cartlist1[b][c][2]) * a
                cartlist1[b][c][2] = a
                checklist_check()
                print("running")
                print(cartlist1[b][c][1])

            def subs(a, b, c):
                a -= 1
                cartlist1[b][c][1] = (int(cartlist1[b][c][1]) / cartlist1[b][c][2]) * a
                cartlist1[b][c][2] = a
                print("running")
                print(cartlist1)

                checklist_check()

            def dels(b, c):
                cartlist1[b].remove(cartlist1[b][c])
                checklist_check()

            def checklist_check():
                global frame
                frame.destroy()
                frame = Frame(main_canvas, bg="black")
                main_canvas.create_window((0, 0), window=frame, anchor=NW)

                for i in cartlist1:
                    if len(i) > 1:  # and i is list:
                        b = Label(
                            frame,
                            text=i[0],
                            bg="black",
                            fg="white",
                            font=("Helvetica", 12, "bold", "underline"),
                            height=1,
                            width=15,
                            pady=5,
                        )
                        b.pack()
                        a = Frame(frame)
                        a.pack()
                        aa = Frame(a, background="black")
                        aa.pack()
                        Label(
                            aa, text="item", bg="black", foreground="white", width=21
                        ).grid(row=0, column=0)
                        Label(aa, text="", bg="white", fg="white", height=2).grid(
                            row=0, column=1
                        )
                        Label(aa, text="cost", bg="black", fg="white", width=10).grid(
                            row=0, column=2
                        )
                        Label(aa, text="", bg="white", fg="white", height=2).grid(
                            row=0, column=3
                        )
                        Label(
                            aa, text="quantity", bg="black", fg="white", width=12
                        ).grid(row=0, column=4)
                        # Label(aa,text="===="*100,bg="white",fg="white",width=47,pady=0).grid(row=1,column=0,columnspan=5)

                        for j in i:
                            if j != i[0]:
                                a1 = Frame(a, bg="black")
                                a1.pack()
                                Button(
                                    a1,
                                    text="❌",
                                    bg="black",
                                    fg="white",
                                    width=2,
                                    command=functools.partial(
                                        dels, cartlist1.index(i), i.index(j)
                                    ),
                                    border=0,
                                ).grid(row=0, column=0)
                                Label(
                                    a1, text=j[0], bg="black", fg="white", width=18
                                ).grid(row=0, column=1)
                                Label(
                                    a1, text="", bg="white", fg="white", height=2
                                ).grid(row=0, column=2)
                                Label(
                                    a1, text=int(j[1]), bg="black", fg="white", width=10
                                ).grid(row=0, column=3)
                                Label(
                                    a1, text="", bg="white", fg="white", height=2
                                ).grid(row=0, column=4)

                                Label(
                                    a1, text=j[2], bg="black", fg="white", width=7
                                ).grid(row=0, column=6)

                                if j[2] != 1:
                                    Button(
                                        a1,
                                        text="-",
                                        bg="black",
                                        fg="white",
                                        width=1,
                                        command=functools.partial(
                                            subs, j[2], cartlist1.index(i), i.index(j)
                                        ),
                                    ).grid(row=0, column=5)
                                else:
                                    Button(
                                        a1,
                                        text="-",
                                        bg="black",
                                        fg="white",
                                        width=1,
                                        command=functools.partial(
                                            subs, j[2], cartlist1.index(i), i.index(j)
                                        ),
                                        state=DISABLED,
                                    ).grid(row=0, column=5)

                                Button(
                                    a1,
                                    text="+",
                                    bg="black",
                                    fg="white",
                                    width=1,
                                    command=functools.partial(
                                        adds, j[2], cartlist1.index(i), i.index(j)
                                    ),
                                ).grid(row=0, column=7)

            checklist_check()

            def payment():
                global pay
                pay = 0
                for b in cartlist1:
                    if len(b) > 1:
                        for c in b:
                            if c != b[0]:
                                pay += int(cartlist1[cartlist1.index(b)][b.index(c)][1])
                print(pay)
                nope()
                ticketbill()

            # payment()

            cart.mainloop()

            # soft()
            # coffee()
            # milkshakes()

        # beverage()
        # rcart()

    # yes()
    hop.mainloop()


# food()


def book(a, b):
    # main.root.destroy()
    global moviename, movieimage
    mi = Image.open(b)
    # mi2 = mi.resize((75,75))
    movieimage = mi.resize((75, 75))
    # print(movieimage)
    moviename = a
    hopb = Tk()
    hopb.geometry("300x180")
    hopb.title("Theatre")
    hopb.config(bg="black")

    Label(hopb, text="                  ", bg="black").pack()
    Label(hopb, text="CHOOSE YOUR THEATRE!").pack()
    Label(hopb, text="                  ", bg="black").pack()
    Button(
        hopb, text="INOX", command=lambda: [des(), movie1()], fg="blue", font=("bold")
    ).pack()
    Label(hopb, text="                  ", bg="black").pack()
    Button(
        hopb,
        text="PVR",
        command=lambda: [des(), movie2()],
        fg="yellow",
        bg="gray",
        font=("bold"),
    ).pack()

    def des():
        hopb.destroy()

    hopb.mainloop()


def ticketbill():
    bill = Tk()
    bill.geometry("400x250")
    main_frame = Frame(bill, bg="black")
    main_frame.pack(fill=BOTH, expand=1)

    # create a canvas

    main_canvas = Canvas(main_frame, bg="black")
    main_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # create a scroll bar and configuring

    scroll = Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
    scroll.pack(side=RIGHT, fill=Y)

    main_canvas.configure(yscrollcommand=scroll.set)

    main_canvas.bind(
        "<Configure>",
        lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")),
    )

    # another frame and adding to the canvas window
    frame1 = Frame(main_canvas, bg="black")

    main_canvas.create_window((0, 0), window=frame1, anchor=NW)
    if time == 1:
        time1 = "morning"
    elif time == 2:
        time1 = "evening"
    else:
        time1 = "second"
    price = 0
    image = Image.open("img\qrcode.png")
    image1 = image.resize((75, 75))
    test = ImageTk.PhotoImage(image1)
    Label(
        frame1, text="Make sure to take some screenshots!!", bg="white", width=46
    ).pack(anchor="w")

    mi2 = ImageTk.PhotoImage(movieimage)

    for i in book1:
        frame = Frame(frame1, bg="black")
        frame.pack(fill=BOTH, expand=1)

        # Label(frame,text="                                        ",bg="white",width=36).grid(row=1,column=0)

        if i[0] == "A":
            Label(
                frame,
                text=f"Eclusive Ticket(Rs.250)",
                bg="black",
                fg="white",
                font=("Helvetica", 12, "bold", "underline"),
                height=1,
                width=23,
                pady=5,
            ).grid(row=0, column=0)
            price += 250
        else:
            Label(
                frame,
                text=f"Normal Ticket(RS.200)",
                bg="black",
                fg="white",
                font=("Helvetica", 12, "bold", "underline"),
                height=1,
                width=23,
                pady=5,
                padx=30,
            ).grid(
                row=0, column=0
            )  # .place(x=0,y=0)
            price += 200

        Label(
            frame,
            text="                                        ",
            bg="black",
            height=6,
            width=28,
        ).grid(row=1, column=0)
        Label(
            frame,
            text=f"Seat No: {i}",
            bg="black",
            fg="white",
            font=("Helvetica", 12),
            height=1,
            width=10,
        ).place(x=0, y=35)
        Label(
            frame,
            text=f"Time: {time1}",
            bg="black",
            fg="white",
            font=("Helvetica", 12),
            height=1,
            width=11,
        ).place(x=0, y=60)
        Label(
            frame,
            text=f"Movie: {moviename}",
            bg="black",
            fg="white",
            font=("Helvetica", 12),
            height=1,
        ).place(x=0, y=85)
        Label(
            frame,
            text=f"Movie: {moviename}",
            bg="black",
            fg="white",
            font=("Helvetica", 12),
            height=1,
        ).place(x=0, y=85)
        ho = Label(frame, image=test)
        ho.place(x=245, y=35)
        ho.image = test

        hola = Label(frame, image=mi2)
        hola.place(x=160, y=35)
        hola.image = mi2

        Label(
            frame1,
            text="                                        ",
            bg="white",
            width=46,
        ).pack(anchor="w")

    Button(
        frame1,
        text="Done",
        bg="black",
        fg="white",
        width=36,
        command=lambda: transaction(),
    ).pack(anchor="w")

    def transaction():
        bill.destroy()
        hopb = Tk()
        hopb.geometry("300x180")
        hopb.title("order food")
        hopb.config(bg="black")
        Label(hopb, text=f"tickets bill :{price}", bg="black", fg="white").pack()
        Label(hopb, text=f"food bill :{pay}", bg="black", fg="white").pack()

        Label(hopb, text="                  ", bg="black").pack()
        Button(
            hopb,
            text="confirm",
            command=lambda: transaction1(),
            fg="black",
            font=("bold"),
        ).pack()
        Label(hopb, text="                  ", bg="black").pack()

        def transaction1():

            totalcost = pay + price
            master = Tk()
            master.geometry("600x580+200+20")
            # frames

            top = Frame(master, height=140, bg="white")
            top.pack(fill=X)

            bottom = Frame(master, height=530, bg="#fd161b")
            bottom.pack(fill=X)

            heading = Label(top, text="PAYMENT", font="arial 15 bold", bg="white")
            heading.place(x=270, y=30)
            heading = Label(
                top, text="Bank Management System", font="arial 19 bold", bg="white"
            )
            heading.place(x=180, y=90)

            # Lable and Enteries

            user_lbl = Label(
                bottom, text="ACCOUNT NO : ", bg="white", font="arial 15 bold"
            )
            user_lbl.place(x=100, y=100)

            pass_lbl = Label(
                bottom, text="PASSWORD : ", bg="white", font="arial 15 bold"
            )
            pass_lbl.place(x=100, y=180)

            e_user = Entry(bottom, width="40")
            e_user.place(x=240, y=105)

            e_pass = Entry(bottom, show="*", width="40")
            e_pass.place(x=240, y=185)
            submit1 = Button(
                bottom, text=">", font="arial 15 bold", command=lambda: dab()
            )
            submit1.place(x=500, y=185)

            heading1 = Label(
                bottom, text=f"INVOICE: {totalcost}", font="arial 19 bold", bg="white"
            )
            heading1.place(x=290, y=205)
            login_notif = Label(bottom, font="arial 19 bold", bg="red", fg="black")
            login_notif.place(x=270, y=235)
            path = os.getcwd()
            all_accounts = os.listdir(path)
            # global login_name
            submit = Button(
                bottom,
                text=" Pay Now!! ",
                font="arial 15 bold",
                width="30",
                command=lambda: sub(),
                state=DISABLED,
            )
            submit.place(x=105, y=335)

            def dab():
                global login_name, login_password, bal
                for name in all_accounts:
                    # print(name)
                    login_name = e_user.get()
                    login_password = e_pass.get()
                    # print(login_name)
                    # login_notif.config(fg="black", text="login successful")
                    if name == login_name:
                        # print(name)
                        # print("working")
                        file = open(name, "r")
                        file_data = file.read()
                        # print(file_data)
                        file_data = file_data.split()
                        # print(file_data)
                        password = file_data[1]
                        # print(password)
                        if login_password == password:
                            # append_file(login_name+"'s transaction history","  "+dt_string+"\tAccount Logged in")
                            login_notif.config(fg="black", text="login successful!!!")
                            submit.config(state=NORMAL)
                            bal = float(file_data[2])
                            # print(bal)
                            if bal > totalcost:
                                bal = bal - totalcost
                            else:
                                login_notif.configure(
                                    fg="black", text="Insufficient balance"
                                )
                                submit.config(state=DISABLED)

                            return
                        else:
                            login_notif.configure(
                                fg="black", text="Password incorrect!!"
                            )
                            return

                login_notif.config(fg="black", text="login unsuccessful")

            # sub=print(totalcost)
            # submit
            # sub()

            def sub():
                global login_name
                for name in all_accounts:
                    # print(name)
                    login_name = e_user.get()
                    login_password = e_pass.get()
                    if name == login_name:
                        # print("working")
                        file = open(name, "w")
                        file.write(login_name)
                        file.write("\n")
                        file.write(login_password)
                        file.write("\n")
                        file.write(str(bal))
                        submit.config(state=DISABLED)
                        login_notif.place(x=230, y=235)
                        login_notif.config(fg="black", text="TRANSACTION successful!!!")
                        file.close()
                        with open(
                            login_name + "'s transaction history", "a+"
                        ) as transaction:
                            now = datetime.now()
                            dt_string = now.strftime("\t%d/%m/%Y\t%H:%M:%S")
                            transaction.write(
                                f"\n{dt_string}\tbookmyshow.com-{totalcost}\tUpdated Balance:{bal}"
                            )
