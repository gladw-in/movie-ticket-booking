_AD='ADMIN'
_AC='Information Added'
_AB='Enter correct age * '
_AA='Enter correct pincode * '
_A9='Enter correct phone number * '
_A8='Select account type * '
_A7='Select your gender * '
_A6='Age cannot be zero * '
_A5='Pincode cannot be zero * '
_A4='Phone number cannot be zero * '
_A3='\tAccount Type\t:\t'
_A2='\tPincode\t:\t'
_A1='Enter your details below'
_A0='420x520'
_z='Personal Information'
_y='all'
_x='<Configure>'
_w='800x400'
_v='Balance Updated'
_u='Amount is required!'
_t='Negative currency is not accepted'
_s='Enter proper amount * '
_r='Amount : '
_q='Welcome '
_p='Password : '
_o='Username : '
_n='Yes'
_m='\tGender\t:\t'
_l='\tAge\t:\t'
_k='\tState\t:\t'
_j='\tCountry\t:\t'
_i='\tPhone number\t:\t'
_h='r+'
_g='Deposit'
_f='  '
_e='All profiles'
_d='Register'
_c='All fields required * '
_b='yellow'
_a='Personal Details'
_Z='Back'
_Y='Current Balance : ₹'
_X='BACK'
_W='cyan'
_V='Login'
_U="'s personal info"
_T='*'
_S='Confirm'
_R='w'
_Q='Cancel'
_P="'s transaction history"
_O='Select'
_N='orange'
_M='r'
_L='green'
_K='[A-Z]'
_J='[a-z]'
_I='\\s'
_H='[_@$]'
_G='black'
_F='\n'
_E=False
_D='red'
_C='bold'
_B='Calibri'
_A='white'
import mysql.connector as ms
from tkinter import *
from tkinter import ttk
import os
from os import path
import mysql.connector as mys
from PIL import ImageTk,Image
import PIL.ImageTk as ptk,re
from datetime import datetime
now=datetime.now()
dt_string=now.strftime('%d/%m/%Y\t%H:%M:%S')
gender=['Male','Female','Other']
account_type=['Savings Account','Reurring Deposit','Current Account','Fixed Deposit']
def center_window(w,h):ws=bank.winfo_screenwidth();hs=bank.winfo_screenheight();x=ws/2-w/2;y=hs/2-h/2;bank.geometry('%dx%d+%d+%d'%(w,h,x,y))
bank=Tk()
center_window(405,610)
bank.title('Bank System')
bank.iconbitmap('img/favicon.ico')
bank.resizable(width=_E,height=_E)
def exit_app():global Exit_screen;Exit_screen=Toplevel(bank);Exit_screen.title('Quit Application');Exit_screen.config(bg=_A);Exit_screen.resizable(width=_E,height=_E);Label(Exit_screen,text='Are you sure you want to quit the application ? ',font=(_B,12),bg=_A).grid(row=0,pady=10,padx=10);b1=Button(Exit_screen,text=_n,font=(_B,12,_C),width=10,command=bank.destroy,fg=_D,bg=_A);b1.grid(row=1,sticky=NW,pady=10,padx=10);b2=Button(Exit_screen,text='No',font=(_B,12,_C),width=10,command=Exit_screen.destroy,bg=_A);b2.grid(row=1,sticky=NE,pady=10,padx=10)
def register():global temp_name;global temp_password;global temp_rewrite_password;global register_screen;global notif;temp_name=StringVar();temp_password=StringVar();temp_rewrite_password=StringVar();register_screen=Toplevel(bank);register_screen.title(_d);register_screen.config(bg=_A);register_screen.resizable(width=_E,height=_E);Label(register_screen,text='Your details:',font=(_B,12),bg=_A).grid(row=0,sticky=N,pady=10,padx=10);Label(register_screen,text='Name - ',font=(_B,12),bg=_A).grid(row=1,sticky=W,pady=10,padx=10);Label(register_screen,text='Password - ',font=(_B,12),bg=_A).grid(row=2,sticky=W,pady=10,padx=10);Label(register_screen,text='Rewrite Password - ',font=(_B,12),bg=_A).grid(row=3,sticky=W,pady=10,padx=10);notif=Label(register_screen,font=(_B,12),bg=_A);notif.grid(row=5,sticky=N,pady=10);Entry(register_screen,textvariable=temp_name).grid(row=1,column=1,pady=10,padx=10);Entry(register_screen,textvariable=temp_password,show=_T).grid(row=2,column=1,pady=10,padx=10);Entry(register_screen,textvariable=temp_rewrite_password,show=_T).grid(row=3,column=1,pady=10,padx=10);reg_button=Button(register_screen,text=_d,command=lambda:[finish_reg()],width=15,font=(_B,12,_C),bg=_G,fg=_A);reg_button.grid(row=4,column=0,sticky=N,pady=10);b1=Button(register_screen,text=_Q,command=register_screen.destroy,font=(_B,12,_C),bg=_G,fg=_A);b1.grid(row=4,column=1,sticky=N,pady=10)
def finish_reg():
	A='Spaces are not allowed in between characters';name=temp_name.get();password=temp_password.get();rewrite_password=temp_rewrite_password.get();all_accounts=os.listdir()
	if name==''or password==''or rewrite_password=='':notif.config(fg=_D,text='All fields requried * ');return
	elif re.search(_H,name):notif.config(fg=_D,text='Username should not contain any special characters');return
	elif re.search(_I,name):notif.config(fg=_D,text=A);return
	elif len(password)<5:notif.config(fg=_D,text='Password must be atleast 5 characters long');return
	elif not re.search(_J,password):notif.config(fg=_D,text='Password must contain lower characters');return
	elif not re.search(_K,password):notif.config(fg=_D,text='Password must contian upper characters');return
	elif not re.search('[0-9]',password):notif.config(fg=_D,text='Password must contain numeric characters');return
	elif not re.search(_H,password):notif.config(fg=_D,text='Password must contain special characters');return
	elif re.search(_I,password):notif.config(fg=_D,text=A);return
	elif password!=rewrite_password:notif.config(fg=_D,text='Passswords do not match * ');return
	for name_check in all_accounts:
		if name==name_check:name+='.txt';notif.config(fg=_D,text='Account already exists');return
		else:append_file(_e,dt_string+'\tAccount name: '+name+'\tPassword: '+password);new_file=open(name,_R);new_file.write(name+_F);new_file.write(password+_F);new_file.write('0');new_file.close();info_file=open(name+_U,_R);transaction_file=open(name+_P,_R);transaction_file.close();append_file(name+_P,_f+dt_string+'\tCreatedAccount\tCurrent Balance = 0');notif.config(fg=_L,text='Account has been created')
def login():global temp_login_name;global temp_login_password;global login_notif;global login_screen;global forgot_button;temp_login_name=StringVar();temp_login_password=StringVar();login_screen=Toplevel(bank);login_screen.title(_V);login_screen.config(bg=_A);login_screen.resizable(width=_E,height=_E);Label(login_screen,text='Login to your account',font=(_B,12),bg=_A).grid(row=0,sticky=N,pady=10,padx=10);Label(login_screen,text=_o,font=(_B,12),bg=_A).grid(row=1,sticky=W,pady=10,padx=10);Label(login_screen,text=_p,font=(_B,12),bg=_A).grid(row=2,sticky=W,pady=10,padx=10);login_notif=Label(login_screen,font=(_B,12),bg=_A);login_notif.grid(row=5,sticky=N);Entry(login_screen,textvariable=temp_login_name).grid(row=1,column=1,pady=10,padx=10);Entry(login_screen,textvariable=temp_login_password,show=_T).grid(row=2,column=1,pady=10,padx=10);b1=Button(login_screen,text='Forgot your password',font=(_B,12,_C),command=forgot_password,fg=_D,bg=_A);b1.grid(row=3,column=1,sticky=N,padx=10);b2=Button(login_screen,text=_V,command=login_session,width=15,font=(_B,12,_C),bg=_W);b2.grid(row=4,column=0,sticky=W,pady=10,padx=10);b3=Button(login_screen,text=_Q,command=login_screen.destroy,font=(_B,12,_C),bg=_A);b3.grid(row=4,column=1,sticky=N,pady=10,padx=10)
def login_session():
	global login_name;all_accounts=os.listdir();login_name=temp_login_name.get();global login_password;login_password=temp_login_password.get()
	for name in all_accounts:
		if name==login_name:
			file=open(name,_M);file_data=file.read();file_data=file_data.split(_F);password=file_data[1]
			if login_password==password:account_button.config(state=NORMAL,bg=_W);personal_button.config(state=NORMAL,bg=_W);logout_button.config(state=NORMAL,bg=_W);append_file(login_name+_P,_f+dt_string+'\tAccount Logged in');login_screen.destroy();return
			else:login_notif.configure(fg=_D,text='Password incorrect!!');return
		if name=='rootUser'and password=='admin@7':login_screen.destroy()
	login_notif.config(fg=_D,text='No such account found !!')
def account_info():global account_dashboard;account_dashboard=Toplevel(bank);account_dashboard.title('Dashboard');account_dashboard.config(bg=_A);account_dashboard.resizable(width=_E,height=_E);Label(account_dashboard,text='Account Dashboard',font=(_B,12),bg=_A).grid(row=0,sticky=N,pady=10,padx=10);Label(account_dashboard,text=_q+login_name,font=(_B,12),bg=_A).grid(row=1,sticky=N,pady=10,padx=10);b0=Button(account_dashboard,text='SHOW BALANCE',font=(_B,12,_C),width=30,command=show_balance,bg=_N);b0.grid(row=2,sticky=N,pady=5,padx=10);b1=Button(account_dashboard,text='DEPOSIT',font=(_B,12,_C),width=30,command=deposit,bg=_N);b1.grid(row=3,sticky=N,pady=5,padx=10);b2=Button(account_dashboard,text='WITHDRAW',font=(_B,12,_C),width=30,command=withdraw,bg=_N);b2.grid(row=4,sticky=N,pady=5,padx=10);b3=Button(account_dashboard,text='SHOW TRANSACTIONS',font=(_B,12,_C),width=30,command=transaction,bg=_N);b3.grid(row=5,sticky=N,pady=5,padx=10);b4=Button(account_dashboard,text=_X,font=(_B,12,_C),width=30,command=account_dashboard.destroy,bg=_A);b4.grid(row=6,sticky=N,pady=20,padx=10)
def append_file(filename,text):
	with open(filename,encoding='utf8',mode='a+')as file_object:
		file_object.seek(0);data=file_object.read(100)
		if len(data)>0:file_object.write(_F)
		file_object.write(text)
def deposit():global amount;global deposit_notif;global current_balance_label;amount=StringVar();file=open(login_name,_M);file_data=file.read();user_details=file_data.split(_F);details_balance=user_details[2];deposit_screen=Toplevel(bank);deposit_screen.title(_g);deposit_screen.config(bg=_A);deposit_screen.resizable(width=_E,height=_E);Label(deposit_screen,text=_g,font=(_B,12),bg=_A).grid(row=0,sticky=N,pady=10,padx=10);current_balance_label=Label(deposit_screen,text=_Y+details_balance,font=(_B,12),bg=_A);current_balance_label.grid(row=1,sticky=W,pady=10,padx=10);Label(deposit_screen,text=_r,font=(_B,12),bg=_A).grid(row=2,sticky=W,pady=10,padx=10);deposit_notif=Label(deposit_screen,font=(_B,12),bg=_A);deposit_notif.grid(row=4,sticky=N,pady=5);Entry(deposit_screen,textvariable=amount).grid(row=2,column=1,pady=10,padx=10);deposit_button=Button(deposit_screen,text=_S,font=(_B,12,_C),width=15,command=finish_deposit,bg=_N);deposit_button.grid(row=3,column=0,sticky=W,pady=10,padx=10);b1=Button(deposit_screen,text=_Q,font=(_B,12,_C),command=deposit_screen.destroy,bg=_A);b1.grid(row=3,column=1,pady=10,padx=10)
def finish_deposit():
	deposit=amount.get()
	if re.search(_J,deposit)or re.search(_H,deposit)or re.search(_I,deposit)or re.search(_K,deposit):deposit_notif.config(fg=_D,text=_s);return
	elif float(amount.get())<=0:deposit_notif.config(text=_t,fg=_D);return
	elif amount.get()=='':deposit_notif.config(text=_u,fg=_D);return
	else:file=open(login_name,_h);file_data=file.read();details=file_data.split(_F);current_balance=details[2];global updated_balance;updated_balance=current_balance;updated_balance=float(updated_balance)+float(amount.get());file_data=file_data.replace(current_balance,str(updated_balance));file.seek(0);file.truncate(0);file.write(file_data);file.close();current_balance_label.config(text=_Y+str(updated_balance),fg=_L);deposit_notif.config(text=_v,fg=_L);append_file(login_name+_P,dt_string+'\tDeposit Amount:Rs '+deposit+'.0\tUpdated Balance:Rs '+str(updated_balance))
def withdraw():global withdraw_amount;global withdraw_notif;global current_balance_label;withdraw_amount=StringVar();file=open(login_name,_M);file_data=file.read();user_details=file_data.split(_F);details_balance=user_details[2];withdraw_screen=Toplevel(bank);withdraw_screen.title('Withdraw');withdraw_screen.config(bg=_A);withdraw_screen.resizable(width=_E,height=_E);Label(withdraw_screen,text=_g,font=(_B,12),bg=_A).grid(row=0,sticky=N,pady=10,padx=10);current_balance_label=Label(withdraw_screen,text=_Y+details_balance,font=(_B,12),bg=_A);current_balance_label.grid(row=1,sticky=W,pady=10,padx=10);Label(withdraw_screen,text=_r,font=(_B,12),bg=_A).grid(row=2,sticky=W,pady=10,padx=10);withdraw_notif=Label(withdraw_screen,font=(_B,12),bg=_A);withdraw_notif.grid(row=4,sticky=N,pady=10,padx=10);Entry(withdraw_screen,textvariable=withdraw_amount).grid(row=2,column=1,pady=10,padx=10);withdraw_button=Button(withdraw_screen,text=_S,font=(_B,12,_C),width=15,command=finish_withdraw,bg=_N);withdraw_button.grid(row=3,column=0,sticky=W,pady=10,padx=10);b1=Button(withdraw_screen,text=_Q,font=(_B,12,_C),command=withdraw_screen.destroy,bg=_A);b1.grid(row=3,column=1,pady=10,padx=10)
def finish_withdraw():
	withdraw=withdraw_amount.get()
	if re.search(_J,withdraw)or re.search(_H,withdraw)or re.search(_I,withdraw)or re.search(_K,withdraw):withdraw_notif.config(fg=_D,text=_s);return
	elif withdraw_amount.get()=='':withdraw_notif.config(text=_u,fg=_D);return
	elif float(withdraw_amount.get())<=0:withdraw_notif.config(text=_t,fg=_D);return
	else:
		file=open(login_name,_h);file_data=file.read();details=file_data.split(_F);current_balance=details[2]
		if float(withdraw_amount.get())>float(current_balance):withdraw_notif.config(text='Insufficient Funds!',fg=_D);return
		updated_balance=current_balance;updated_balance=float(updated_balance)-float(withdraw_amount.get());file_data=file_data.replace(current_balance,str(updated_balance));file.seek(0);file.truncate(0);file.write(file_data);file.close();current_balance_label.config(text=_Y+str(updated_balance),fg=_L);withdraw_notif.config(text=_v,fg=_L);append_file(login_name+_P,dt_string+'\tWithdraw Amount:Rs '+withdraw+'.0\tUpdated balance:Rs '+str(updated_balance))
def transaction():
	main_window=Toplevel(bank);main_window.title('Transaction window');main_window.geometry(_w);main_frame=Frame(main_window);main_frame.pack(fill=BOTH,expand=1);main_frame.config(bg=_A);my_canvas=Canvas(main_frame);my_canvas.pack(side=LEFT,fill=BOTH,expand=1);my_canvas.config(bg=_A);my_scrollbar=ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview);my_scrollbar.pack(side=RIGHT,fill=Y);my_canvas.configure(yscrollcommand=my_scrollbar.set,bg=_A);my_canvas.bind(_x,lambda e:my_canvas.configure(scrollregion=my_canvas.bbox(_y)));second_frame=Frame(my_canvas);second_frame.config(bg=_A);my_canvas.create_window((0,0),window=second_frame,anchor='nw')
	with open(login_name+_P,_M)as transaction:ttk.Label(second_frame,text=transaction.read(),font=(_B,14),background=_A).pack()
	back_button=Button(second_frame,text=_Z,command=main_window.destroy,font=(_B,12,_C),bg=_A,width=25);back_button.pack(side=RIGHT)
def show_balance():global balance;file=open(login_name,_M);file_data=file.read();user_details=file_data.split(_F);balance=user_details[2];Balance_dashboard=Toplevel(bank);Balance_dashboard.title('Balance');Balance_dashboard.config(bg=_A);Balance_dashboard.resizable(width=_E,height=_E);Label(Balance_dashboard,text='Account Balance',font=(_B,14),bg=_A).grid(row=0,sticky=N,pady=10,padx=10);Label(Balance_dashboard,text=_q+login_name,font=(_B,14),bg=_A).grid(row=1,sticky=N,pady=10,padx=10);Label(Balance_dashboard,text='Your Balance is ',font=(_B,14),bg=_A).grid(row=2,sticky=N,pady=10,padx=10);Label(Balance_dashboard,text='₹'+balance,font=(_B,16,_C),fg='blue',bg=_A).grid(row=3,sticky=N,pady=10,padx=10);b1=Button(Balance_dashboard,text=_Z,font=(_B,12,_C),width=30,command=Balance_dashboard.destroy,bg=_A);b1.grid(row=4,sticky=N,pady=5,padx=10)
def personal_info():
	A='\t';global personal_information_screen
	try:file=open(login_name,_M);file_data=file.read();user_details=file_data.split(_F);details_name=user_details[0];file=open(login_name+_U,_h);file_info=file.read();info=file_info.split(_F);info_number=info[0];info_country=info[1];info_area=info[2];info_pincode=info[3];info_age=info[4];info_gender=info[5];info_account_type=info[6]
	except FileNotFoundError:pass
	except IndexError:pass
	personal_information_screen=Toplevel(bank);personal_information_screen.title(_a);personal_information_screen.config(bg=_A);personal_information_screen.geometry('420x480');personal_information_screen.resizable(width=_E,height=_E);Label(personal_information_screen,text=_a,width=20,font=(_B,12),bg=_A).grid(row=0,sticky=N,pady=10,padx=10);Label(personal_information_screen,text='\tName\t:\t',width=20,font=(_B,12),bg=_A).grid(row=1,column=0,sticky=W,pady=10,padx=10);Label(personal_information_screen,text=_i,width=20,font=(_B,12),bg=_A).grid(row=2,column=0,sticky=W,pady=10,padx=10);Label(personal_information_screen,text=_j,width=20,font=(_B,12),bg=_A).grid(row=3,column=0,sticky=W,pady=10,padx=10);Label(personal_information_screen,text=_k,width=20,font=(_B,12),bg=_A).grid(row=4,column=0,sticky=W,pady=10,padx=10);Label(personal_information_screen,text='\tPin-Code\t:\t',width=20,font=(_B,12),bg=_A).grid(row=5,column=0,sticky=W,pady=10,padx=10);Label(personal_information_screen,text=_l,width=20,font=(_B,12),bg=_A).grid(row=6,column=0,sticky=W,pady=10,padx=10);Label(personal_information_screen,text=_m,width=20,font=(_B,12),bg=_A).grid(row=7,column=0,sticky=W,pady=10,padx=10);Label(personal_information_screen,text='\tAccount type\t:\t',width=20,font=(_B,12),bg=_A).grid(row=8,column=0,sticky=W,pady=10,padx=10)
	try:Label(personal_information_screen,text=A+details_name,width=20,font=(_B,12,_C),bg=_A).grid(row=1,columns=2,sticky=E,pady=10,padx=20);Label(personal_information_screen,text=A+info_number,width=20,font=(_B,12,_C),bg=_A).grid(row=2,columns=2,sticky=E,pady=10,padx=20);Label(personal_information_screen,text=A+info_country,width=20,font=(_B,12,_C),bg=_A).grid(row=3,columns=2,sticky=E,pady=10,padx=20);Label(personal_information_screen,text=A+info_area,width=20,font=(_B,12,_C),bg=_A).grid(row=4,columns=2,sticky=E,pady=10,padx=20);Label(personal_information_screen,text=A+info_pincode,width=20,font=(_B,12,_C),bg=_A).grid(row=5,columns=2,sticky=E,pady=10,padx=20);Label(personal_information_screen,text=A+info_age,width=20,font=(_B,12,_C),bg=_A).grid(row=6,columns=2,sticky=E,pady=10,padx=20);Label(personal_information_screen,text=A+info_gender,width=20,font=(_B,12,_C),bg=_A).grid(row=7,columns=2,sticky=E,pady=10,padx=20);Label(personal_information_screen,text=A+info_account_type,width=20,font=(_B,12,_C),bg=_A).grid(row=8,columns=2,sticky=E,pady=10,padx=20)
	except UnboundLocalError:pass
	b1=Button(personal_information_screen,text='ADD More',width=20,font=(_B,12,_C),command=add_info,bg=_b);b1.grid(row=9,sticky=W,pady=10,padx=10);b2=Button(personal_information_screen,text='EDIT ',width=20,font=(_B,12,_C),command=edit_info,bg=_b);b2.grid(row=0,column=1,pady=10,padx=10);back=Button(personal_information_screen,text=_X,width=20,font=(_B,12,_C),command=personal_information_screen.destroy,bg=_A);back.grid(row=9,sticky=W,column=1,pady=10,padx=10)
def destroy_add_info():Information_screen.destroy()
def add_info():personal_information_screen.destroy();global Information_screen;global temp_country;global temp_area;global temp_pincode;global temp_age;global temp_gender;global temp_account_type;global temp_number;global add_info_notif;temp_number=StringVar();temp_country=StringVar();temp_area=StringVar();temp_pincode=StringVar();temp_age=StringVar();temp_gender=StringVar();temp_account_type=StringVar();Information_screen=Toplevel(bank);Information_screen.title(_z);Information_screen.config(bg=_A);Information_screen.geometry(_A0);Information_screen.resizable(width=_E,height=_E);Personal_information_label=Label(Information_screen,text=_a,font=(_B,12),bg=_A);Personal_information_label.grid(row=0,sticky=N,pady=10);Label(Information_screen,text=_A1,font=(_B,12),bg=_A).grid(row=1,sticky=N,pady=10,padx=10);Label(Information_screen,text=_i,width=20,font=(_B,12),bg=_A).grid(row=2,sticky=W,pady=10,padx=10);Label(Information_screen,text=_j,width=20,font=(_B,12),bg=_A).grid(row=3,sticky=W,pady=10,padx=10);Label(Information_screen,text=_k,width=20,font=(_B,12),bg=_A).grid(row=4,sticky=W,pady=10,padx=10);Label(Information_screen,text=_A2,width=20,font=(_B,12),bg=_A).grid(row=5,sticky=W,pady=10,padx=10);Label(Information_screen,text=_l,width=20,font=(_B,12),bg=_A).grid(row=6,sticky=W,pady=10,padx=10);Label(Information_screen,text=_m,width=20,font=(_B,12),bg=_A).grid(row=7,sticky=W,pady=10,padx=10);Label(Information_screen,text=_A3,width=20,font=(_B,12),bg=_A).grid(row=8,sticky=W,pady=10,padx=10);add_info_notif=Label(Information_screen,font=(_B,12),bg=_A);add_info_notif.grid(row=9,sticky=N,pady=10);Entry(Information_screen,textvariable=temp_number).grid(row=2,column=1,pady=10,padx=10);Entry(Information_screen,textvariable=temp_country).grid(row=3,column=1,pady=10,padx=10);Entry(Information_screen,textvariable=temp_area).grid(row=4,column=1,pady=10,padx=10);Entry(Information_screen,textvariable=temp_pincode).grid(row=5,column=1,pady=10,padx=10);Entry(Information_screen,textvariable=temp_age).grid(row=6,column=1,pady=10,padx=10);b1=Button(Information_screen,text=_S,width=20,font=(_B,12,_C),command=finish_info,bg=_b);b1.grid(row=10,sticky=N,pady=5,padx=10);b2=Button(Information_screen,text=_X,width=20,font=(_B,12,_C),command=lambda:[destroy_add_info(),personal_info()],bg=_A);b2.grid(row=10,column=1,sticky=N,pady=5,padx=10);temp_gender.set(_O);drop_gender=OptionMenu(Information_screen,temp_gender,*gender);drop_gender.grid(row=7,column=1,pady=10,padx=10);temp_account_type.set(_O);drop_account_type=OptionMenu(Information_screen,temp_account_type,*account_type);drop_account_type.grid(row=8,column=1,pady=10,padx=10)
def finish_info():
	number=temp_number.get();pincode=temp_pincode.get();age=temp_age.get()
	if temp_country.get()==''or temp_area.get()==''or temp_pincode.get()==''or temp_age.get()==''or temp_gender.get()=='':add_info_notif.config(fg=_D,text=_c);return
	elif temp_number.get()==''or temp_account_type.get()=='':add_info_notif.config(fg=_D,text=_c);return
	elif temp_number.get()==0:add_info_notif.config(fg=_D,text=_A4);return
	elif temp_pincode.get()==0:add_info_notif.config(fg=_D,text=_A5);return
	elif temp_age.get()==0:add_info_notif.config(fg=_D,text=_A6);return
	elif temp_gender.get()==_O:add_info_notif.config(fg=_D,text=_A7);return
	elif temp_account_type.get()==_O:add_info_notif.config(fg=_D,text=_A8);return
	elif re.search(_J,number)or re.search(_H,number)or re.search(_I,number)or re.search(_K,number)or len(number)!=10:add_info_notif.config(fg=_D,text=_A9);return
	elif re.search(_J,pincode)or re.search(_H,pincode)or re.search(_I,pincode)or re.search(_K,pincode):add_info_notif.config(fg=_D,text=_AA);return
	elif re.search(_J,age)or re.search(_H,age)or re.search(_I,age)or re.search(_K,age):add_info_notif.config(fg=_D,text=_AB);return
	else:new_file=open(login_name+_U,_R);new_file.write(temp_number.get()+_F);new_file.write(temp_country.get()+_F);new_file.write(temp_area.get()+_F);new_file.write(temp_pincode.get()+_F);new_file.write(temp_age.get()+_F);new_file.write(temp_gender.get()+_F);new_file.write(temp_account_type.get()+_F);new_file.close();add_info_notif.config(fg=_L,text=_AC)
def destroy_edit_info():Edit_Information_screen.destroy()
def edit_info():personal_information_screen.destroy();global Edit_Information_screen;global temp_new_number;global temp_new_country;global temp_new_area;global temp_new_pincode;global temp_new_age;global temp_new_gender;global temp_new_account_type;global edit_info_new_notif;temp_new_number=StringVar();temp_new_country=StringVar();temp_new_area=StringVar();temp_new_pincode=StringVar();temp_new_age=StringVar();temp_new_gender=StringVar();temp_new_account_type=StringVar();Edit_Information_screen=Toplevel(bank);Edit_Information_screen.title(_z);Edit_Information_screen.config(bg=_A);Edit_Information_screen.geometry(_A0);Edit_Information_screen.resizable(width=_E,height=_E);Personal_information_label=Label(Edit_Information_screen,text=_a,font=(_B,12),bg=_A);Personal_information_label.grid(row=0,sticky=N,pady=10,padx=10);Label(Edit_Information_screen,text=_A1,font=(_B,12),bg=_A).grid(row=1,sticky=N,pady=10,padx=10);Label(Edit_Information_screen,text=_i,width=20,font=(_B,12),bg=_A).grid(row=2,sticky=W,pady=10,padx=10);Label(Edit_Information_screen,text=_j,width=20,font=(_B,12),bg=_A).grid(row=3,sticky=W,pady=10,padx=10);Label(Edit_Information_screen,text=_k,width=20,font=(_B,12),bg=_A).grid(row=4,sticky=W,pady=10,padx=10);Label(Edit_Information_screen,text=_A2,width=20,font=(_B,12),bg=_A).grid(row=5,sticky=W,pady=10,padx=10);Label(Edit_Information_screen,text=_l,width=20,font=(_B,12),bg=_A).grid(row=6,sticky=W,pady=10,padx=10);Label(Edit_Information_screen,text=_m,width=20,font=(_B,12),bg=_A).grid(row=7,sticky=W,pady=10,padx=10);Label(Edit_Information_screen,text=_A3,width=20,font=(_B,12),bg=_A).grid(row=8,sticky=W,pady=10,padx=10);edit_info_new_notif=Label(Edit_Information_screen,font=(_B,12),bg=_A);edit_info_new_notif.grid(row=9,sticky=N,pady=10);Entry(Edit_Information_screen,textvariable=temp_new_number).grid(row=2,column=1,pady=10,padx=10);Entry(Edit_Information_screen,textvariable=temp_new_country).grid(row=3,column=1,pady=10,padx=10);Entry(Edit_Information_screen,textvariable=temp_new_area).grid(row=4,column=1,pady=10,padx=10);Entry(Edit_Information_screen,textvariable=temp_new_pincode).grid(row=5,column=1,pady=10,padx=10);Entry(Edit_Information_screen,textvariable=temp_new_age).grid(row=6,column=1,pady=10,padx=10);b1=Button(Edit_Information_screen,text=_S,width=20,font=(_B,12,_C),command=finish_edit_info,bg=_b);b1.grid(row=10,sticky=N,pady=5,padx=10);b2=Button(Edit_Information_screen,text=_X,width=20,font=(_B,12,_C),command=lambda:[destroy_edit_info(),personal_info()],bg=_A);b2.grid(row=10,column=1,sticky=N,pady=5,padx=10);temp_new_gender.set(_O);drop_gender=OptionMenu(Edit_Information_screen,temp_new_gender,*gender);drop_gender.grid(row=7,column=1,pady=10,padx=10);temp_new_account_type.set(_O);drop_account_type=OptionMenu(Edit_Information_screen,temp_new_account_type,*account_type);drop_account_type.grid(row=8,column=1,pady=10,padx=10)
def finish_edit_info():
	number=temp_new_number.get();pincode=temp_new_pincode.get();age=temp_new_age.get()
	if temp_new_country.get()==''or temp_new_area.get()==''or temp_new_pincode.get()==''or temp_new_age.get()==''or temp_new_gender.get()=='':edit_info_new_notif.config(fg=_D,text=_c);return
	elif temp_new_number.get()==''or temp_new_account_type=='':edit_info_new_notif.config(fg=_D,text=_c);return
	elif temp_new_number.get()==0:edit_info_new_notif.config(fg=_D,text=_A4);return
	elif temp_new_pincode.get()==0:edit_info_new_notif.config(fg=_D,text=_A5);return
	elif temp_new_age.get()==0:edit_info_new_notif.config(fg=_D,text=_A6);return
	elif temp_new_gender.get()==_O:edit_info_new_notif.config(fg=_D,text=_A7);return
	elif temp_new_account_type.get()==_O:edit_info_new_notif.config(fg=_D,text=_A8);return
	elif re.search(_J,number)or re.search(_H,number)or re.search(_I,number)or re.search(_K,number)or len(number)!=10:edit_info_new_notif.config(fg=_D,text=_A9);return
	elif re.search(_J,pincode)or re.search(_H,pincode)or re.search(_I,pincode)or re.search(_K,pincode):edit_info_new_notif.config(fg=_D,text=_AA);return
	elif re.search(_J,age)or re.search(_H,age)or re.search(_I,age)or re.search(_K,age):edit_info_new_notif.config(fg=_D,text=_AB);return
	else:new_file=open(login_name+_U,_R);new_file.write(temp_new_number.get()+_F);new_file.write(temp_new_country.get()+_F);new_file.write(temp_new_area.get()+_F);new_file.write(temp_new_pincode.get()+_F);new_file.write(temp_new_age.get()+_F);new_file.write(temp_new_gender.get()+_F);new_file.write(temp_new_account_type.get()+_F);new_file.close();edit_info_new_notif.config(fg=_L,text=_AC)
def forgot_password():global password_screen;global password_notif;global password_name;password_name=StringVar();password_screen=Toplevel(bank);password_screen.title('Forgot password');password_screen.config(bg=_A);password_screen.resizable(width=_E,height=_E);Label(password_screen,text='        Username : ',font=(_B,12),bg=_A).grid(row=0,sticky=W,pady=10,padx=10);Label(password_screen,text=' Your password is  ',font=(_B,12),bg=_A).grid(row=1,sticky=W,pady=10,padx=10);password_notif=Label(password_screen,font=(_B,12),bg=_A);password_notif.grid(row=1,column=1,sticky=W,pady=10,padx=10);Entry(password_screen,textvariable=password_name).grid(row=0,column=1,pady=10,padx=10);b1=Button(password_screen,text=_S,command=finish_password,font=(_B,12,_C),width=20,bg=_N);b1.grid(row=3,sticky=N,padx=10,pady=10);b2=Button(password_screen,text=_Q,command=password_screen.destroy,font=(_B,12,_C),bg=_A);b2.grid(row=3,column=1,sticky=N,pady=10)
def finish_password():
	all_accounts=os.listdir();username=password_name.get()
	if username not in all_accounts:password_notif.config(fg=_D,text='User not found!!');return
	else:file=open(username,_M);file_data=file.read();user_details=file_data.split(_F);password=user_details[1];password_notif.config(fg=_L,text=password);file.close()
def logout():global logout_screen;logout_screen=Toplevel(bank);logout_screen.title('Logout session');logout_screen.config(bg=_A);logout_screen.resizable(width=_E,height=_E);Label(logout_screen,text='Are you sure you want to Logout ? ',font=(_B,14),bg=_A).grid(row=0,pady=10);logout_yes=Button(logout_screen,text=_n,font=(_B,12,_C),width=10,command=lambda:[logout_screen.destroy(),button_states()],fg=_D,bg=_A);logout_yes.grid(row=1,sticky=NW,pady=10,padx=10);b1=Button(logout_screen,text='No',font=(_B,12,_C),width=10,command=logout_screen.destroy,bg=_A);b1.grid(row=1,sticky=NE,pady=10,padx=10)
def button_states():account_button.config(state=DISABLED,bg=_A);personal_button.config(state=DISABLED,bg=_A);logout_button.config(state=DISABLED,bg=_A)
def logout_destroy():logout_screen.destroy();append_file(login_name+_P,_f+dt_string+'\tAccount Logged OUT')
def admin_login():global admin_screen;global temp_admin_name;global temp_admin_password;global admin_notif;temp_admin_name=StringVar();temp_admin_password=StringVar();admin_screen=Toplevel(bank);admin_screen.title(_AD);admin_screen.config(bg=_G);admin_screen.resizable(width=_E,height=_E);Label(admin_screen,text='WELCOME ADMIN',font=(_B,12),bg=_G,fg=_A).grid(row=0,sticky=N,pady=10,padx=10);Label(admin_screen,text=_o,font=(_B,12),bg=_G,fg=_A).grid(row=1,pady=10,padx=10);Label(admin_screen,text=_p,font=(_B,12),bg=_G,fg=_A).grid(row=2,pady=10,padx=10);admin_notif=Label(admin_screen,font=(_B,12),bg=_G);admin_notif.grid(row=5,sticky=N);Entry(admin_screen,textvariable=temp_admin_name).grid(row=1,column=1,pady=10,padx=10);Entry(admin_screen,textvariable=temp_admin_password,show=_T).grid(row=2,column=1,pady=10,padx=10);b1=Button(admin_screen,text=_V,font=(_B,12,_C),width=15,command=admin_session,bg=_G);b1.grid(row=4,column=0,sticky=W,pady=10,padx=10);b2=Button(admin_screen,text=_Z,font=(_B,12,_C),width=15,command=admin_screen.destroy,bg=_D);b2.grid(row=4,columns=2,sticky=E,pady=10,padx=10)
def admin_session():
	admin_name=temp_admin_name.get();admin_password=temp_admin_password.get()
	if admin_name=='Admin'and admin_password=='Admin@1':admin_screen.destroy();admin_dashboard=Toplevel(bank);admin_dashboard.title(_AD);admin_dashboard.config(bg=_G);admin_dashboard.resizable(width=_E,height=_E);Label(admin_dashboard,text='Welcome Home ADMIN',font=(_B,16),bg=_G,fg=_A).grid(row=0,sticky=N,pady=10,padx=10);b1=Button(admin_dashboard,text='ALL PROFILE DATA',width=20,font=(_B,12,_C),bg=_N,command=all_profiles);b1.grid(row=3,sticky=N,padx=10);b2=Button(admin_dashboard,text='LOGOUT',width=15,font=(_B,12,_C),bg=_G,command=admin_dashboard.destroy);b2.grid(row=5,column=0,pady=10,padx=10)
	else:admin_notif.config(fg=_D,text='Check the username and password')
def all_profiles():
	main_window=Toplevel(bank);main_window.title(_e);main_window.geometry(_w);main_frame=Frame(main_window);main_frame.pack(fill=BOTH,expand=1);main_frame.config(bg=_A);my_canvas=Canvas(main_frame);my_canvas.pack(side=LEFT,fill=BOTH,expand=1);my_canvas.config(bg=_A);my_scrollbar=ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview);my_scrollbar.pack(side=RIGHT,fill=Y);my_canvas.configure(yscrollcommand=my_scrollbar.set,bg=_A);my_canvas.bind(_x,lambda e:my_canvas.configure(scrollregion=my_canvas.bbox(_y)));second_frame=Frame(my_canvas);second_frame.config(bg=_A);my_canvas.create_window((0,0),window=second_frame,anchor='nw')
	try:
		with open(_e,_M)as profiles:ttk.Label(second_frame,text=profiles.read(),font=(_B,14),background=_A).pack()
		back_button=Button(second_frame,text=_Z,command=main_window.destroy,font=(_B,12,_C),bg=_A,width=25);back_button.pack(side=RIGHT)
	except FileNotFoundError:pass
global account_button
global personal_button
global logout_button
img=Image.open('img/logo.png')
img=img.resize((385,225))
img=ImageTk.PhotoImage(img)
bgImage=ptk.PhotoImage(file='img/background_image.png')
Label(bank,image=bgImage).place(relwidth=1,relheight=1)
Label(bank,text='Bank Management System',font=(_B,14,_C),bg=_G,fg=_A).grid(row=0,pady=10,padx=10)
Label(bank,image=img,anchor=CENTER).grid(row=2,pady=10,padx=10)
admin_button=Button(bank,text='Admin Login',font=(_B,14,_C),width=12,bg=_G,fg=_A,command=admin_login)
admin_button.grid(row=3,pady=5,padx=10)
register_button=Button(bank,text=_d,font=(_B,14,_C),width=20,command=register,bg=_G,fg=_A)
register_button.grid(row=4,sticky=NW,pady=5,padx=10)
login_button=Button(bank,text=_V,font=(_B,14,_C),width=20,command=login,bg=_G,fg=_A)
login_button.grid(row=4,sticky=NE,pady=5,padx=10)
account_button=Button(bank,text='Account ',state=DISABLED,font=(_B,14,_C),width=20,command=account_info,bg=_G,fg=_A)
account_button.grid(row=5,sticky=NW,pady=5,padx=10)
personal_button=Button(bank,text='Personal Info',state=DISABLED,font=(_B,14,_C),width=20,command=personal_info,bg=_G,fg=_A)
personal_button.grid(row=5,sticky=NE,pady=5,padx=10)
logout_button=Button(bank,text='Logout',state=DISABLED,font=(_B,14,_C),width=20,command=logout,bg=_G,fg=_A)
logout_button.grid(row=7,pady=5,padx=10)
Button(bank,text='EXIT',font=(_B,14,_C),width=20,command=exit_app,bg=_G,fg=_A).grid(row=8,pady=10,padx=10)
bank.mainloop()
