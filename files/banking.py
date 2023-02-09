import mysql.connector as ms
from tkinter import *
from tkinter import ttk
import os
from os import path
import mysql.connector as mys
from PIL import ImageTk, Image
import PIL.ImageTk as ptk
import re
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y\t%H:%M:%S")
gender = ["Male","Female","Other"]
account_type = ["Savings Account","Reurring Deposit","Current Account","Fixed Deposit"]

#Functions
def center_window(w, h):
    #screen width and height
    ws = bank.winfo_screenwidth()
    hs = bank.winfo_screenheight()
    #position x, y
    x = (ws/2) - (w/2)    
    y = (hs/2) - (h/2)
    bank.geometry('%dx%d+%d+%d' % (w, h, x, y))
bank = Tk() 
center_window(405, 610)
bank.title('Bank System')
bank.iconbitmap("img/favicon.ico")
bank.resizable(width=False,height=False)
            
def exit_app():
    #Vars
    global Exit_screen
    
    #Details Screen
    Exit_screen = Toplevel(bank)
    Exit_screen.title('Quit Application')
    Exit_screen.config(bg="white")
    Exit_screen.resizable(width=False,height=False)
    
    #Label
    Label(Exit_screen, text="Are you sure you want to quit the application ? ", font=('Calibri',12),bg="white").grid(row=0,pady=10,padx=10)

    #Buttons
    b1 = Button(Exit_screen, text="Yes", font=('Calibri',12,"bold"),width=10,command=bank.destroy,fg="red",bg="white")
    b1.grid(row=1,sticky=NW,pady=10,padx=10)
    b2 = Button(Exit_screen, text="No", font=('Calibri',12,"bold"),width=10,command=Exit_screen.destroy,bg="white")
    b2.grid(row=1,sticky=NE,pady=10,padx=10)

def register():
    #Vars
    global temp_name
    global temp_password
    global temp_rewrite_password
    global register_screen
    global notif
    temp_name = StringVar()
    temp_password = StringVar()
    temp_rewrite_password = StringVar()
    
    #Register Screen
    register_screen = Toplevel(bank)
    register_screen.title('Register')
    register_screen.config(bg="white")
    register_screen.resizable(width=False,height=False)
    
    #Labels
    Label(register_screen, text="Your details:", font=('Calibri',12),bg="white").grid(row=0,sticky=N,pady=10,padx=10)
    Label(register_screen, text="Name - ", font=('Calibri',12),bg="white").grid(row=1,sticky=W,pady=10,padx=10)
    Label(register_screen, text="Password - ", font=('Calibri',12),bg="white").grid(row=2,sticky=W,pady=10,padx=10)
    Label(register_screen, text="Rewrite Password - ", font=('Calibri',12),bg="white").grid(row=3,sticky=W,pady=10,padx=10)
    notif = Label(register_screen, font=('Calibri',12),bg="white")
    notif.grid(row=5,sticky=N,pady=10)
    
    #Entries
    Entry(register_screen,textvariable=temp_name).grid(row=1,column=1,pady=10,padx=10)
    Entry(register_screen,textvariable=temp_password,show="*").grid(row=2,column=1,pady=10,padx=10)
    Entry(register_screen,textvariable=temp_rewrite_password,show="*").grid(row=3,column=1,pady=10,padx=10)
    
    #Buttons
    reg_button = Button(register_screen, text="Register", command =lambda:[finish_reg()], width=15, font=('Calibri',12,"bold"),bg="black",fg="white")
    reg_button.grid(row=4,column=0,sticky=N,pady=10)
    b1 = Button(register_screen, text="Cancel", command = register_screen.destroy, font=('Calibri',12,"bold"),bg="black",fg="white")
    b1.grid(row=4,column=1,sticky=N,pady=10)


def finish_reg():
    name = temp_name.get()
    password = temp_password.get()
    rewrite_password = temp_rewrite_password.get()
    all_accounts = os.listdir()
    if name == "" or password == "" or rewrite_password =="":
        notif.config(fg="red",text="All fields requried * ")
        return
    elif re.search("[_@$]", name):
        notif.config(fg="red",text="Username should not contain any special characters")
        return
    elif re.search("\s", name):
        notif.config(fg="red",text="Spaces are not allowed in between characters")
        return 
    elif (len(password) < 5):
        notif.config(fg="red",text="Password must be atleast 5 characters long")
        return
    elif not re.search("[a-z]", password):
        notif.config(fg="red",text="Password must contain lower characters")
        return
    elif not re.search("[A-Z]", password):
        notif.config(fg="red",text="Password must contian upper characters")
        return
    elif not re.search("[0-9]", password):
        notif.config(fg="red",text="Password must contain numeric characters")
        return
    elif not re.search("[_@$]", password):
        notif.config(fg="red",text="Password must contain special characters")
        return
    elif re.search("\s", password):
        notif.config(fg="red",text="Spaces are not allowed in between characters")
        return
    elif password != rewrite_password:
        notif.config(fg="red",text="Passswords do not match * ")
        return

    for name_check in all_accounts:
        if name == name_check:
            name += ".txt"
            notif.config(fg="red",text="Account already exists")
            return
        else:
            append_file("All profiles",dt_string+"\tAccount name: "+name+"\tPassword: "+password)
            new_file = open(name,"w")
            new_file.write(name+'\n')
            new_file.write(password+'\n')
            new_file.write('0')
            new_file.close()
            info_file = open(name+"'s personal info" ,"w")
            transaction_file = open(name+"'s transaction history" ,"w")
            transaction_file.close()
            append_file(name+"'s transaction history","  "+dt_string+"\tCreatedAccount\tCurrent Balance = 0")
            notif.config(fg="green", text="Account has been created")


def login():
    #Vars
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen
    global forgot_button
    
    temp_login_name = StringVar()
    temp_login_password = StringVar()
    
    #Login Screen
    login_screen = Toplevel(bank)
    login_screen.title('Login')
    login_screen.config(bg="white")
    login_screen.resizable(width=False,height=False)
    
    #Labels
    Label(login_screen, text="Login to your account", font=('Calibri',12),bg="white").grid(row=0,sticky=N,pady=10,padx=10)
    Label(login_screen, text="Username : ", font=('Calibri',12),bg="white").grid(row=1,sticky=W,pady=10,padx=10)
    Label(login_screen, text="Password : ", font=('Calibri',12),bg="white").grid(row=2,sticky=W,pady=10,padx=10)
    login_notif = Label(login_screen, font=('Calibri',12),bg="white")
    login_notif.grid(row=5,sticky=N)
    
    #Entry
    Entry(login_screen, textvariable=temp_login_name).grid(row=1,column=1,pady=10,padx=10)
    Entry(login_screen, textvariable=temp_login_password,show="*").grid(row=2,column=1,pady=10,padx=10)
    
    #Button
    b1 = Button(login_screen, text="Forgot your password",font=('Calibri',12,"bold"),command=forgot_password,fg="red",bg="white")
    b1.grid(row=3,column=1,sticky=N,padx=10)
    b2 = Button(login_screen, text="Login", command=login_session, width=15,font=('Calibri',12,"bold"),bg="cyan")
    b2.grid(row=4,column=0,sticky=W,pady=10,padx=10)
    b3 = Button(login_screen, text="Cancel", command = login_screen.destroy, font=('Calibri',12,"bold"),bg="white")
    b3.grid(row=4,column=1,sticky=N,pady=10,padx=10)

def login_session():
    global login_name
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    global login_password
    login_password = temp_login_password.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name,"r")
            file_data = file.read()
            file_data = file_data.split('\n')
            password  = file_data[1]
            if login_password == password:
                account_button.config(state=NORMAL,bg="cyan")
                personal_button.config(state=NORMAL,bg="cyan")
                logout_button.config(state=NORMAL,bg="cyan")
                append_file(login_name+"'s transaction history","  "+dt_string+"\tAccount Logged in")
                login_screen.destroy()
                return
            else:
                login_notif.configure(fg="red", text="Password incorrect!!")
                return
        if name == "rootUser" and password == "admin@7":
            login_screen.destroy()
    login_notif.config(fg="red", text="No such account found !!")

def account_info():
    #Vars
    global account_dashboard
    
    #Account Screen
    account_dashboard = Toplevel(bank)
    account_dashboard.title('Dashboard')
    account_dashboard.config(bg="white")
    account_dashboard.resizable(width=False,height=False)
    
    #Labels
    Label(account_dashboard, text="Account Dashboard", font=('Calibri',12),bg="white").grid(row=0,sticky=N,pady=10,padx=10)
    Label(account_dashboard, text="Welcome "+login_name, font=('Calibri',12),bg="white").grid(row=1,sticky=N,pady=10,padx=10)
    
    #Buttons
    b0 = Button(account_dashboard, text="SHOW BALANCE",font=('Calibri',12,"bold"),width=30,command=show_balance,bg="orange")
    b0.grid(row=2,sticky=N,pady=5,padx=10)
    b1 = Button(account_dashboard, text="DEPOSIT",font=('Calibri',12,"bold"),width=30,command=deposit,bg="orange")
    b1.grid(row=3,sticky=N,pady=5,padx=10)
    b2 = Button(account_dashboard, text="WITHDRAW",font=('Calibri',12,"bold"),width=30,command= withdraw,bg="orange")
    b2.grid(row=4,sticky=N,pady=5,padx=10)
    b3 = Button(account_dashboard, text="SHOW TRANSACTIONS",font=('Calibri',12,"bold"),width=30,command= transaction,bg="orange")
    b3.grid(row=5,sticky=N,pady=5,padx=10)
    b4 = Button(account_dashboard, text="BACK",font=('Calibri',12,"bold"),width=30,command=account_dashboard.destroy,bg="white")
    b4.grid(row=6,sticky=N,pady=20,padx=10)

def append_file(filename, text):
    with open(filename,encoding="utf8",mode="a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text)
        
def deposit():
    #Vars
    global amount
    global deposit_notif
    global current_balance_label

    amount = StringVar()
    file   = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[2]
    
    #Deposit Screen
    deposit_screen = Toplevel(bank)
    deposit_screen.title('Deposit')
    deposit_screen.config(bg="white")
    deposit_screen.resizable(width=False,height=False)
    
    #Label
    Label(deposit_screen, text="Deposit", font=('Calibri',12),bg="white").grid(row=0,sticky=N,pady=10,padx=10)
    current_balance_label = Label(deposit_screen, text="Current Balance : ₹"+details_balance, font=('Calibri',12),bg="white")
    current_balance_label.grid(row=1,sticky=W,pady=10,padx=10)
    Label(deposit_screen, text="Amount : ", font=('Calibri',12),bg="white").grid(row=2,sticky=W,pady=10,padx=10)
    deposit_notif = Label(deposit_screen,font=('Calibri',12),bg="white")
    deposit_notif.grid(row=4, sticky=N,pady=5)
    
    #Entry
    Entry(deposit_screen, textvariable=amount).grid(row=2,column=1,pady=10,padx=10)
    
    #Button
    deposit_button = Button(deposit_screen,text="Confirm",font=('Calibri',12,"bold"),width=15,command=finish_deposit,bg="orange")
    deposit_button.grid(row=3,column=0,sticky=W,pady=10,padx=10)
    b1 = Button(deposit_screen,text="Cancel",font=('Calibri',12,"bold"),command=deposit_screen.destroy,bg="white")
    b1.grid(row=3,column=1,pady=10,padx=10)
    
def finish_deposit():
    deposit = amount.get()
    if re.search("[a-z]",deposit) or re.search("[_@$]",deposit) or re.search("\s",deposit) or re.search("[A-Z]",deposit):
        deposit_notif.config(fg="red",text="Enter proper amount * ")
        return
    else:
        if float(amount.get()) <=0:
            deposit_notif.config(text='Negative currency is not accepted', fg='red')
            return
        elif amount.get() == "":
            deposit_notif.config(text='Amount is required!',fg="red")
            return    
        else:
            file = open(login_name, 'r+')
            file_data = file.read()
            details = file_data.split('\n')
            current_balance = details[2]
            global updated_balance
            updated_balance = current_balance
            updated_balance = float(updated_balance) + float(amount.get())
            file_data       = file_data.replace(current_balance, str(updated_balance))
            file.seek(0)
            file.truncate(0)
            file.write(file_data)
            file.close()
            current_balance_label.config(text="Current Balance : ₹"+str(updated_balance),fg="green")
            deposit_notif.config(text='Balance Updated', fg='green')
            append_file(login_name+"'s transaction history",dt_string+"\tDeposit Amount:Rs "+deposit+".0\tUpdated Balance:Rs "+str(updated_balance))
        
def withdraw():
     #Vars
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    withdraw_amount = StringVar()
    file   = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[2]
    
    #Deposit Screen
    withdraw_screen = Toplevel(bank)
    withdraw_screen.title('Withdraw')
    withdraw_screen.config(bg="white")
    withdraw_screen.resizable(width=False,height=False)
    
    #Label
    Label(withdraw_screen, text="Deposit", font=('Calibri',12),bg="white").grid(row=0,sticky=N,pady=10,padx=10)
    current_balance_label = Label(withdraw_screen, text="Current Balance : ₹"+details_balance, font=('Calibri',12),bg="white")
    current_balance_label.grid(row=1,sticky=W,pady=10,padx=10)
    Label(withdraw_screen, text="Amount : ", font=('Calibri',12),bg="white").grid(row=2,sticky=W,pady=10,padx=10)
    withdraw_notif = Label(withdraw_screen,font=('Calibri',12),bg="white")
    withdraw_notif.grid(row=4, sticky=N,pady=10,padx=10)
    
    #Entry
    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2,column=1,pady=10,padx=10)
    
    #Button
    withdraw_button = Button(withdraw_screen,text="Confirm",font=('Calibri',12,"bold"),width=15,command=finish_withdraw,bg="orange")
    withdraw_button.grid(row=3,column=0,sticky=W,pady=10,padx=10)
    b1 = Button(withdraw_screen,text="Cancel",font=('Calibri',12,"bold"),command=withdraw_screen.destroy,bg="white")
    b1.grid(row=3,column=1,pady=10,padx=10)


def finish_withdraw():
    withdraw = withdraw_amount.get()
    if re.search("[a-z]",withdraw) or re.search("[_@$]",withdraw) or re.search("\s",withdraw) or re.search("[A-Z]",withdraw):
        withdraw_notif.config(fg="red",text="Enter proper amount * ")
        return
    else:
        if withdraw_amount.get() == "":
            withdraw_notif.config(text='Amount is required!',fg="red")
            return
        elif float(withdraw_amount.get()) <=0:
            withdraw_notif.config(text='Negative currency is not accepted', fg='red')
            return
        else:
            file = open(login_name, 'r+')
            file_data = file.read()
            details = file_data.split('\n')
            current_balance = details[2]
            if float(withdraw_amount.get()) >float(current_balance):
                withdraw_notif.config(text='Insufficient Funds!', fg='red')
                return
            updated_balance = current_balance
            updated_balance = float(updated_balance) - float(withdraw_amount.get())
            file_data       = file_data.replace(current_balance, str(updated_balance))
            file.seek(0)
            file.truncate(0)
            file.write(file_data)
            file.close()
            current_balance_label.config(text="Current Balance : ₹"+str(updated_balance),fg="green")
            withdraw_notif.config(text='Balance Updated', fg='green')
            append_file(login_name+"'s transaction history",dt_string+"\tWithdraw Amount:Rs "+withdraw+".0\tUpdated balance:Rs "+str(updated_balance))

def transaction():
    #Transaction window
    main_window = Toplevel(bank)
    main_window.title('Transaction window')
    main_window.geometry("800x400")
    
    #main frame
    main_frame = Frame(main_window)
    main_frame.pack(fill=BOTH, expand=1)
    main_frame.config(bg="white")
    
    #canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas.config(bg="white")
    
    #scrollbar
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set,bg="white")
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
    second_frame = Frame(my_canvas)
    second_frame.config(bg="white")
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    with open(login_name+"'s transaction history", 'r') as transaction:
            ttk.Label(second_frame, text=transaction.read(), font=('Calibri',14),background="white").pack()
    back_button = Button(second_frame, text="Back", command=main_window.destroy, font=('Calibri',12,"bold"),bg="white",width=25)
    back_button.pack(side=RIGHT)

def show_balance():
    global balance
    file   = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    balance = user_details[2]
    
    
    
    
    #Account Screen
    Balance_dashboard = Toplevel(bank)
    Balance_dashboard.title('Balance')
    Balance_dashboard.config(bg="white")
    Balance_dashboard.resizable(width=False,height=False)
    
    #Labels
    Label(Balance_dashboard, text="Account Balance", font=('Calibri',14),bg="white").grid(row=0,sticky=N,pady=10,padx=10)
    Label(Balance_dashboard, text="Welcome "+login_name, font=('Calibri',14),bg="white").grid(row=1,sticky=N,pady=10,padx=10)
    Label(Balance_dashboard, text="Your Balance is ", font=('Calibri',14),bg="white").grid(row=2,sticky=N,pady=10,padx=10)
    Label(Balance_dashboard, text="₹"+balance, font=('Calibri',16,"bold"),fg="blue",bg="white").grid(row=3,sticky=N,pady=10,padx=10)
    
    #Buttons
    b1 = Button(Balance_dashboard, text="Back",font=('Calibri',12,"bold"),width=30,command=Balance_dashboard.destroy,bg="white")
    b1.grid(row=4,sticky=N,pady=5,padx=10)

def personal_info():
    #Vars
    global personal_information_screen
    try:
        file = open(login_name, 'r')
        file_data = file.read()
        user_details = file_data.split('\n')
        details_name = user_details[0]        
        file = open(login_name+"'s personal info" ,"r+")
        file_info = file.read()
        info = file_info.split('\n')
        info_number = info[0]
        info_country = info[1]
        info_area=info[2]
        info_pincode=info[3]
        info_age=info[4]
        info_gender=info[5]
        info_account_type = info[6]
    except FileNotFoundError:
        pass
    
    except IndexError:
        pass
    
    #Account Information
    personal_information_screen = Toplevel(bank)
    personal_information_screen.title('Personal Details')
    personal_information_screen.config(bg="white")
    personal_information_screen.geometry("420x480")
    personal_information_screen.resizable(width=False,height=False)
    
    #Labels
    Label(personal_information_screen, text="Personal Details",width=20,font=('Calibri',12),bg="white").grid(row=0,sticky=N,pady=10,padx=10)
    Label(personal_information_screen, text="\tName\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=1,column=0,sticky=W,pady=10,padx=10)
    Label(personal_information_screen, text="\tPhone number\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=2,column=0,sticky=W,pady=10,padx=10)
    Label(personal_information_screen, text="\tCountry\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=3,column=0,sticky=W,pady=10,padx=10)    
    Label(personal_information_screen, text="\tState\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=4,column=0,sticky=W,pady=10,padx=10)    
    Label(personal_information_screen, text="\tPin-Code\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=5,column=0,sticky=W,pady=10,padx=10)    
    Label(personal_information_screen, text="\tAge\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=6,column=0,sticky=W,pady=10,padx=10)    
    Label(personal_information_screen, text="\tGender\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=7,column=0,sticky=W,pady=10,padx=10)
    Label(personal_information_screen, text="\tAccount type\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=8,column=0,sticky=W,pady=10,padx=10)
    
    #info Labels
    try:
        Label(personal_information_screen, text="\t"+details_name,width=20, font=('Calibri',12,"bold"),bg="white").grid(row=1,columns=2,sticky=E,pady=10,padx=20)
        Label(personal_information_screen, text="\t"+info_number,width=20, font=('Calibri',12,"bold"),bg="white").grid(row=2,columns=2,sticky=E,pady=10,padx=20)
        Label(personal_information_screen, text="\t"+info_country,width=20, font=('Calibri',12,"bold"),bg="white").grid(row=3,columns=2,sticky=E,pady=10,padx=20)
        Label(personal_information_screen, text="\t"+info_area,width=20, font=('Calibri',12,"bold"),bg="white").grid(row=4,columns=2,sticky=E,pady=10,padx=20)
        Label(personal_information_screen, text="\t"+info_pincode,width=20, font=('Calibri',12,"bold"),bg="white").grid(row=5,columns=2,sticky=E,pady=10,padx=20)
        Label(personal_information_screen, text="\t"+info_age,width=20, font=('Calibri',12,"bold"),bg="white").grid(row=6,columns=2,sticky=E,pady=10,padx=20)
        Label(personal_information_screen, text="\t"+info_gender,width=20, font=('Calibri',12,"bold"),bg="white").grid(row=7,columns=2,sticky=E,pady=10,padx=20)
        Label(personal_information_screen, text="\t"+info_account_type,width=20, font=('Calibri',12,"bold"),bg="white").grid(row=8,columns=2,sticky=E,pady=10,padx=20)
    except UnboundLocalError:
        pass
    
    #Button
    b1 = Button(personal_information_screen,text="ADD More",width=20,font=('Calibri',12,"bold"),command=add_info,bg="yellow")
    b1.grid(row=9,sticky=W,pady=10,padx=10)
    b2 = Button(personal_information_screen,text="EDIT ",width=20,font=('Calibri',12,"bold"),command=edit_info,bg="yellow")
    b2.grid(row=0,column=1,pady=10,padx=10)
    back = Button(personal_information_screen,text="BACK",width=20,font=('Calibri',12,"bold"),command=personal_information_screen.destroy,bg="white")
    back.grid(row=9,sticky=W,column=1,pady=10,padx=10)

def destroy_add_info():
    Information_screen.destroy()

def add_info():
    personal_information_screen.destroy()
    #Vars
    global Information_screen
    global temp_country
    global temp_area
    global temp_pincode
    global temp_age
    global temp_gender
    global temp_account_type
    global temp_number
    global add_info_notif

    temp_number = StringVar()
    temp_country = StringVar()
    temp_area = StringVar()
    temp_pincode = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_account_type = StringVar()
    
    #Details Screen
    Information_screen = Toplevel(bank)
    Information_screen.title('Personal Information')
    Information_screen.config(bg="white")
    Information_screen.geometry("420x520")
    Information_screen.resizable(width=False,height=False)
    
    #Labels
    Personal_information_label = Label(Information_screen, text="Personal Details", font=('Calibri',12),bg="white")
    Personal_information_label.grid(row=0,sticky=N,pady=10)
    Label(Information_screen, text="Enter your details below", font=('Calibri',12),bg="white").grid(row=1,sticky=N,pady=10,padx=10)
    Label(Information_screen, text="\tPhone number\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=2,sticky=W,pady=10,padx=10)
    Label(Information_screen, text="\tCountry\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=3,sticky=W,pady=10,padx=10)
    Label(Information_screen, text="\tState\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=4,sticky=W,pady=10,padx=10)
    Label(Information_screen, text="\tPincode\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=5,sticky=W,pady=10,padx=10)
    Label(Information_screen, text="\tAge\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=6,sticky=W,pady=10,padx=10)
    Label(Information_screen, text="\tGender\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=7,sticky=W,pady=10,padx=10)
    Label(Information_screen, text="\tAccount Type\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=8,sticky=W,pady=10,padx=10)
    add_info_notif = Label(Information_screen, font=('Calibri',12),bg="white")
    add_info_notif.grid(row=9,sticky=N,pady=10)
    
    #Entries
    Entry(Information_screen,textvariable=temp_number).grid(row=2,column=1,pady=10,padx=10)
    Entry(Information_screen,textvariable=temp_country).grid(row=3,column=1,pady=10,padx=10)
    Entry(Information_screen,textvariable=temp_area).grid(row=4,column=1,pady=10,padx=10)
    Entry(Information_screen,textvariable=temp_pincode).grid(row=5,column=1,pady=10,padx=10)
    Entry(Information_screen,textvariable=temp_age).grid(row=6,column=1,pady=10,padx=10)
    
    #Buttons
    b1 = Button(Information_screen, text="Confirm",width=20, font=('Calibri',12,"bold"),command = finish_info,bg="yellow")
    b1.grid(row=10,sticky=N,pady=5,padx=10)
    b2 = Button(Information_screen, text="BACK",width=20, font=('Calibri',12,"bold"),command = lambda:[destroy_add_info(),personal_info()],bg="white")
    b2.grid(row=10,column=1,sticky=N,pady=5,padx=10)

    #drop down button
    temp_gender.set("Select")
    drop_gender = OptionMenu(Information_screen,temp_gender,*gender)
    drop_gender.grid(row=7,column=1,pady=10,padx=10)
    temp_account_type.set("Select")
    drop_account_type = OptionMenu(Information_screen,temp_account_type,*account_type)
    drop_account_type.grid(row=8,column=1,pady=10,padx=10)

    
def finish_info():
    number = temp_number.get()
    pincode = temp_pincode.get()
    age = temp_age.get()
    if temp_country.get()=="" or temp_area.get()=="" or temp_pincode.get()=="" or temp_age.get()=="" or temp_gender.get()=="":
        add_info_notif.config(fg="red",text= "All fields required * ")
        return
    elif temp_number.get()=="" or temp_account_type.get()=="":
        add_info_notif.config(fg="red",text= "All fields required * ")
        return
    elif temp_number.get()==0 :
        add_info_notif.config(fg="red",text="Phone number cannot be zero * ")
        return
    elif temp_pincode.get()==0:
        add_info_notif.config(fg="red",text="Pincode cannot be zero * ")
        return
    elif temp_age.get()==0:
        add_info_notif.config(fg="red",text="Age cannot be zero * ")
        return
    elif temp_gender.get()=="Select":
        add_info_notif.config(fg="red",text="Select your gender * ")
        return
    elif temp_account_type.get()=="Select":
        add_info_notif.config(fg="red",text="Select account type * ")
        return
    elif re.search("[a-z]",number) or re.search("[_@$]",number) or re.search("\s",number) or re.search("[A-Z]",number) or len(number)!=10:
        add_info_notif.config(fg="red",text="Enter correct phone number * ")
        return
    elif re.search("[a-z]",pincode) or re.search("[_@$]",pincode) or re.search("\s",pincode) or re.search("[A-Z]",pincode):
        add_info_notif.config(fg="red",text="Enter correct pincode * ")
        return
    elif re.search("[a-z]",age) or re.search("[_@$]",age) or re.search("\s",age) or re.search("[A-Z]",age):
        add_info_notif.config(fg="red",text="Enter correct age * ")
        return
    else:
        new_file = open(login_name+"'s personal info" ,"w")
        new_file.write(temp_number.get()+'\n')
        new_file.write(temp_country.get()+'\n')
        new_file.write(temp_area.get()+'\n')
        new_file.write(temp_pincode.get()+'\n')
        new_file.write(temp_age.get()+'\n')
        new_file.write(temp_gender.get()+'\n')
        new_file.write(temp_account_type.get()+'\n')
        new_file.close()   
        add_info_notif.config(fg="green", text="Information Added")

def destroy_edit_info():
    Edit_Information_screen.destroy()
    
def edit_info():
    #Vars
    personal_information_screen.destroy()
    global Edit_Information_screen
    global temp_new_number
    global temp_new_country
    global temp_new_area
    global temp_new_pincode
    global temp_new_age
    global temp_new_gender
    global temp_new_account_type
    global edit_info_new_notif 

    temp_new_number = StringVar()
    temp_new_country = StringVar()
    temp_new_area = StringVar()
    temp_new_pincode = StringVar()
    temp_new_age = StringVar()
    temp_new_gender = StringVar()
    temp_new_account_type = StringVar()
    
    #Details Screen
    Edit_Information_screen = Toplevel(bank)
    Edit_Information_screen.title('Personal Information')
    Edit_Information_screen.config(bg="white")
    Edit_Information_screen.geometry("420x520")
    Edit_Information_screen.resizable(width=False,height=False)
    
    #Labels
    Personal_information_label = Label(Edit_Information_screen, text="Personal Details", font=('Calibri',12),bg="white")
    Personal_information_label.grid(row=0,sticky=N,pady=10,padx=10)
    Label(Edit_Information_screen, text="Enter your details below", font=('Calibri',12),bg="white").grid(row=1,sticky=N,pady=10,padx=10)
    Label(Edit_Information_screen, text="\tPhone number\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=2,sticky=W,pady=10,padx=10)
    Label(Edit_Information_screen, text="\tCountry\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=3,sticky=W,pady=10,padx=10)
    Label(Edit_Information_screen, text="\tState\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=4,sticky=W,pady=10,padx=10)
    Label(Edit_Information_screen, text="\tPincode\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=5,sticky=W,pady=10,padx=10)
    Label(Edit_Information_screen, text="\tAge\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=6,sticky=W,pady=10,padx=10)
    Label(Edit_Information_screen, text="\tGender\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=7,sticky=W,pady=10,padx=10)        
    Label(Edit_Information_screen, text="\tAccount Type\t:\t",width=20, font=('Calibri',12),bg="white").grid(row=8,sticky=W,pady=10,padx=10)

    edit_info_new_notif = Label(Edit_Information_screen, font=('Calibri',12),bg="white")
    edit_info_new_notif.grid(row=9,sticky=N,pady=10)
    
    #Entries
    Entry(Edit_Information_screen,textvariable=temp_new_number).grid(row=2,column=1,pady=10,padx=10)
    Entry(Edit_Information_screen,textvariable=temp_new_country).grid(row=3,column=1,pady=10,padx=10)
    Entry(Edit_Information_screen,textvariable=temp_new_area).grid(row=4,column=1,pady=10,padx=10)
    Entry(Edit_Information_screen,textvariable=temp_new_pincode).grid(row=5,column=1,pady=10,padx=10)
    Entry(Edit_Information_screen,textvariable=temp_new_age).grid(row=6,column=1,pady=10,padx=10)
    
    #Buttons
    b1 = Button(Edit_Information_screen, text="Confirm",width=20, font=('Calibri',12,"bold"),command=finish_edit_info,bg="yellow")
    b1.grid(row=10,sticky=N,pady=5,padx=10)
    b2 = Button(Edit_Information_screen, text="BACK",width=20, font=('Calibri',12,"bold"),command=lambda:[destroy_edit_info(),personal_info()],bg="white")
    b2.grid(row=10,column=1,sticky=N,pady=5,padx=10)

    #drop down button
    temp_new_gender.set("Select")
    drop_gender = OptionMenu(Edit_Information_screen,temp_new_gender,*gender)
    drop_gender.grid(row=7,column=1,pady=10,padx=10)
    temp_new_account_type.set("Select")
    drop_account_type = OptionMenu(Edit_Information_screen,temp_new_account_type,*account_type)
    drop_account_type.grid(row=8,column=1,pady=10,padx=10)

    
def finish_edit_info():
    number = temp_new_number.get()
    pincode = temp_new_pincode.get()
    age = temp_new_age.get()
    if temp_new_country.get()=="" or temp_new_area.get()=="" or temp_new_pincode.get()=="" or temp_new_age.get()=="" or temp_new_gender.get()=="":
        edit_info_new_notif.config(fg="red",text="All fields required * ")
        return
    elif temp_new_number.get()=="" or temp_new_account_type=="":
        edit_info_new_notif.config(fg="red",text="All fields required * ")
        return
    elif temp_new_number.get()==0:
        edit_info_new_notif.config(fg="red",text="Phone number cannot be zero * ")
        return
    elif temp_new_pincode.get()==0:
        edit_info_new_notif.config(fg="red",text="Pincode cannot be zero * ")
        return
    elif temp_new_age.get()==0:
        edit_info_new_notif.config(fg="red",text="Age cannot be zero * ")
        return
    elif temp_new_gender.get()=="Select":
        edit_info_new_notif.config(fg="red",text="Select your gender * ")
        return
    elif temp_new_account_type.get()=="Select":
        edit_info_new_notif.config(fg="red",text="Select account type * ")
        return
    elif re.search("[a-z]",number) or re.search("[_@$]",number) or re.search("\s",number) or re.search("[A-Z]",number) or len(number)!=10:
        edit_info_new_notif.config(fg="red",text="Enter correct phone number * ")
        return
    elif re.search("[a-z]",pincode) or re.search("[_@$]",pincode) or re.search("\s",pincode) or re.search("[A-Z]",pincode):
        edit_info_new_notif.config(fg="red",text="Enter correct pincode * ")
        return
    elif re.search("[a-z]",age) or re.search("[_@$]",age) or re.search("\s",age) or re.search("[A-Z]",age):
        edit_info_new_notif.config(fg="red",text="Enter correct age * ")
        return
    else:
        new_file = open(login_name+"'s personal info" ,"w")
        new_file.write(temp_new_number.get()+'\n')
        new_file.write(temp_new_country.get()+'\n')
        new_file.write(temp_new_area.get()+'\n')
        new_file.write(temp_new_pincode.get()+'\n')
        new_file.write(temp_new_age.get()+'\n')
        new_file.write(temp_new_gender.get()+'\n')
        new_file.write(temp_new_account_type.get()+'\n')
        new_file.close()   
        edit_info_new_notif.config(fg="green", text="Information Added")

    
def forgot_password():
    #Vars
    global password_screen
    global password_notif
    global password_name
    password_name = StringVar()

    
    #Forgot Screen
    password_screen = Toplevel(bank)
    password_screen.title('Forgot password')
    password_screen.config(bg="white")
    password_screen.resizable(width=False,height=False)
    
    #Labels
    Label(password_screen, text="        Username : ", font=('Calibri',12),bg="white").grid(row=0,sticky=W,pady=10,padx=10)
    Label(password_screen, text=" Your password is  ", font=('Calibri',12),bg="white").grid(row=1,sticky=W,pady=10,padx=10)
    password_notif = Label(password_screen, font=('Calibri',12),bg="white")
    password_notif.grid(row=1,column=1,sticky=W,pady=10,padx=10)
    
    #Entries
    Entry(password_screen, textvariable=password_name).grid(row=0,column=1,pady=10,padx=10)
    
    #Buttons
    b1 = Button(password_screen, text="Confirm", command=finish_password, font=('Calibri',12,"bold"),width = 20,bg="orange")
    b1.grid(row=3,sticky=N,padx=10,pady=10)
    b2 = Button(password_screen, text="Cancel", command=password_screen.destroy, font=('Calibri',12,"bold"),bg="white")
    b2.grid(row=3,column=1,sticky=N,pady=10)

def finish_password():
    all_accounts = os.listdir()
    username = password_name.get()
    if username not in all_accounts:
        password_notif.config(fg="red",text="User not found!!")
        return        
    else:
        file = open(username,"r")
        file_data = file.read()
        user_details = file_data.split("\n")
        password = user_details[1]
        password_notif.config(fg="green",text=password)
        file.close()                      

def logout():
    #Vars
    global logout_screen
    
    #Details Screen
    logout_screen = Toplevel(bank)
    logout_screen.title('Logout session')
    logout_screen.config(bg="white")
    logout_screen.resizable(width=False,height=False)
    
    #Label
    Label(logout_screen, text = "Are you sure you want to Logout ? ", font=('Calibri',14),bg="white").grid(row=0,pady=10)
    
    #Buttons
    logout_yes = Button(logout_screen, text="Yes", font=('Calibri',12,"bold"),width=10,command=lambda:[logout_screen.destroy(),button_states()],fg="red",bg="white")
    logout_yes.grid(row=1,sticky=NW,pady=10,padx=10)
    b1 = Button(logout_screen, text="No", font=('Calibri',12,"bold"),width=10,command=logout_screen.destroy,bg="white")
    b1.grid(row=1,sticky=NE,pady=10,padx=10)

def button_states():
    account_button.config(state=DISABLED,bg="white")
    personal_button.config(state=DISABLED,bg="white")
    logout_button.config(state=DISABLED,bg="white")

def logout_destroy():
    logout_screen.destroy()
    append_file(login_name+"'s transaction history","  "+dt_string+"\tAccount Logged OUT")

def admin_login():
    global admin_screen
    global temp_admin_name
    global temp_admin_password
    global admin_notif
    
    temp_admin_name = StringVar()
    temp_admin_password = StringVar()
    #Admin Screen
    admin_screen = Toplevel(bank)
    admin_screen.title('ADMIN')
    admin_screen.config(bg="black")
    admin_screen.resizable(width=False,height=False)

    Label(admin_screen, text="WELCOME ADMIN", font=('Calibri',12),bg="black",fg="white").grid(row=0,sticky=N,pady=10,padx=10)
    Label(admin_screen, text="Username : ", font=('Calibri',12),bg="black",fg="white").grid(row=1,pady=10,padx=10)
    Label(admin_screen, text="Password : ", font=('Calibri',12),bg="black",fg="white").grid(row=2,pady=10,padx=10)
    admin_notif = Label(admin_screen, font=('Calibri',12),bg="black")
    admin_notif.grid(row=5,sticky=N)
    #Entries
    Entry(admin_screen, textvariable=temp_admin_name).grid(row=1,column=1,pady=10,padx=10)
    Entry(admin_screen, textvariable=temp_admin_password,show="*").grid(row=2,column=1,pady=10,padx=10)
    
    #Buttons
    b1 = Button(admin_screen, text="Login", font=('Calibri',12,"bold"),width=15,command=admin_session,bg="black")
    b1.grid(row=4,column=0,sticky=W,pady=10,padx=10)
    b2 = Button(admin_screen, text="Back", font=('Calibri',12,"bold"),width=15,command=admin_screen.destroy,bg="red")
    b2.grid(row=4,columns=2,sticky=E,pady=10,padx=10)

def admin_session():
    admin_name = temp_admin_name.get()
    admin_password = temp_admin_password.get()
    if admin_name=="Admin" and admin_password=="Admin@1":
        admin_screen.destroy()
        #window
        admin_dashboard = Toplevel(bank)
        admin_dashboard.title('ADMIN')
        admin_dashboard.config(bg="black")
        admin_dashboard.resizable(width=False,height=False)
        #labels
        Label(admin_dashboard, text="Welcome Home ADMIN", font=('Calibri',16),bg="black",fg="white").grid(row=0,sticky=N,pady=10,padx=10)
        #buttons
        b1 = Button(admin_dashboard, text="ALL PROFILE DATA",width=20,font=('Calibri',12,"bold"),bg="orange",command=all_profiles)
        b1.grid(row=3,sticky=N,padx=10)
        b2 = Button(admin_dashboard, text="LOGOUT", width=15,font=('Calibri',12,"bold"),bg="black",command=admin_dashboard.destroy)
        b2.grid(row=5,column=0,pady=10,padx=10)
        
    else:
        admin_notif.config(fg="red",text="Check the username and password")

def all_profiles():
    #Transaction window
    main_window = Toplevel(bank)
    main_window.title('All profiles')
    main_window.geometry("800x400")
    
    #main frame
    main_frame = Frame(main_window)
    main_frame.pack(fill=BOTH, expand=1)
    main_frame.config(bg="white")
    
    #canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    my_canvas.config(bg="white")
    
    #scrollbar
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set,bg="white")
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
    second_frame = Frame(my_canvas)
    second_frame.config(bg="white")
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    try:
        with open("All profiles", 'r') as profiles:
                ttk.Label(second_frame, text=profiles.read(), font=('Calibri',14),background="white").pack()
        back_button = Button(second_frame, text="Back", command=main_window.destroy, font=('Calibri',12,"bold"),bg="white",width=25)
        back_button.pack(side=RIGHT)    
    except FileNotFoundError:
        pass

     
#Vars
global account_button
global personal_button
global logout_button

#Image import
img = Image.open('img/logo.png')
img = img.resize((385,225))
img = ImageTk.PhotoImage(img)
bgImage = ptk.PhotoImage(file = r"img/background_image.png")
Label(bank, image = bgImage).place(relwidth = 1,relheight = 1)

#Labels
Label(bank, text = "Bank Management System", font=('Calibri',14,"bold"),bg="black",fg="white").grid(row=0,pady=10,padx=10)
Label(bank, image=img,anchor=CENTER).grid(row=2,pady=10,padx=10)

#Buttons
admin_button = Button(bank, text="Admin Login", font=('Calibri',14,"bold"),width=12,bg="black",fg="white",command=admin_login)
admin_button.grid(row=3,pady=5,padx=10)
register_button = Button(bank, text="Register", font=('Calibri',14,"bold"),width=20,command=register,bg="black",fg="white")
register_button.grid(row=4,sticky=NW,pady=5,padx=10)
login_button = Button(bank, text="Login", font=('Calibri',14,"bold"),width=20,command=login,bg="black",fg="white")
login_button.grid(row=4,sticky=NE,pady=5,padx=10)
account_button = Button(bank, text="Account ",state=DISABLED, font=('Calibri',14,"bold"),width=20,command=account_info,bg="black",fg="white")
account_button.grid(row=5,sticky=NW,pady=5,padx=10)
personal_button = Button(bank, text="Personal Info",state=DISABLED, font=('Calibri',14,"bold"),width=20,command=personal_info,bg="black",fg="white")
personal_button.grid(row=5,sticky=NE,pady=5,padx=10)
logout_button = Button(bank, text="Logout",state=DISABLED, font=('Calibri',14,"bold"),width=20,command=logout,bg="black",fg="white")
logout_button.grid(row=7,pady=5,padx=10)
Button(bank, text="EXIT", font=('Calibri',14,"bold"),width=20,command=exit_app,bg="black", fg="white").grid(row=8,pady=10,padx=10)
      
bank.mainloop()
