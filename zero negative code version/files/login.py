_d='phone number'
_c='something is wrong'
_b='Enter username'
_a='                      '
_Z='host'
_Y='user'
_X='pass'
_W='Invalid! ...'
_V='--should be a 10 digit number--'
_U='lightgray'
_T='Helvetica'
_S='show password'
_R='Username'
_Q='rb'
_P='db.dat'
_O='sign up'
_N='password'
_M=','
_L=True
_K=' '
_J='acc.csv'
_I='#e4c8e6'
_H='#FFE5B4'
_G='*'
_F='green'
_E='white'
_D='hand2'
_C='red'
_B='black'
_A='Arial'
from tkinter import *
import mysql.connector,csv
from random import randint
import pandas as pd,pickle,DB_config as db,main
def bicreate():
	try:
		with open(_P,_Q)as o:return
	except:db.run()
bicreate()
o=open(_P,_Q)
q=pickle.load(o)
o.close()
db_pw=q[_X]
db_db=q['db']
db_us=q[_Y]
db_hs=q[_Z]
def csvcreate():
	try:
		with open(_J,mode='r')as f:return
	except:
		with open(_J,mode='w')as f:f=csv.writer(f,delimiter=_M);st=['slno','username','phno',_N];f.writerow(st)
csvcreate()
def sqlcreate():
	try:dataBase=mysql.connector.connect(host=db_hs,user=db_us,passwd=db_pw,database=db_db)
	except:dataBase=mysql.connector.connect(host=db_hs,user=db_us,passwd=db_pw);mc=dataBase.cursor();mc.execute(f"create database {db_db};");mc.execute(f"use {db_db}");mc.execute('CREATE TABLE acc (username VARCHAR(255) PRIMARY KEY, phno VARCHAR(255), pass VARCHAR(255))ENGINE=InnoDB DEFAULT CHARSET=latin1');mc.execute('desc acc;')
print('Correct password')
def w():
	A='login';global ro,pp;ro=Tk();ro.title(A);ro.geometry('380x400');ro.config(bg=_B);Label(ro,text='LOGIN IN',font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14).place(x=140,y=20);Label(ro,text=_R,font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14).place(x=20,y=71);Label(ro,text=_N,font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14).place(x=20,y=121);entry1=Entry(ro,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I);entry2=Entry(ro,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I,show=_G);entry1.place(x=140,y=70);entry2.place(x=140,y=120);pp=Label(ro,text=_a,bg=_B,fg=_E,cursor=_D,font=(_A,12));pp.place(x=30,y=300);showme=IntVar(value=0)
	def showp():
		if showme.get()==1:entry2.config(show='');entry2.after(1000,lambda:entry2.config(show=_G));entry2.after(1000,lambda:show.deselect())
		else:entry2.config(show=_G)
	show=Checkbutton(ro,text=_S,font=(_A,10),height=1,variable=showme,onvalue=1,offvalue=0,command=lambda:showp(),bg=_B,fg=_E,activebackground=_B,activeforeground=_E,width=12,pady=0);show.place(x=20,y=170);t=Label(ro,text='forgot password?',bg=_B,fg='blue',cursor=_D,font=(_A,10));t.place(x=20,y=190);t.bind('<Button-1>',lambda x:forgotpass());lb=Button(ro,text=A,font=(_T,8),height=1,width=12,bg=_U,activebackground=_E,borderwidth=0,padx=9,pady=4,relief=GROOVE,command=lambda:checkpass(a,b)).place(x=140,y=210);Label(ro,text='did not sign up yet?',font=(_A,8),bg=_B,fg=_E,height=1,padx=2,pady=10,width=20).place(x=125,y=240);sp=Button(ro,text=_O,font=(_T,8),height=1,width=12,bg=_U,activebackground=_E,borderwidth=0,padx=9,pady=4,relief=GROOVE,command=lambda:signup()).place(x=140,y=270);a=entry1.get();b=entry2.get()
	def checkpass(a,b):
		global pp;a=entry1.get();b=entry2.get();a=a.replace(_K,'');b=b.replace(_K,'');dataBase=mysql.connector.connect(host=db_hs,user=db_us,passwd=db_pw,database=db_db);mycursor=dataBase.cursor();sq='SELECT * FROM acc WHERE username = %s and pass = %s';ad=a,b;mycursor.execute(sq,ad);myresult=mycursor.fetchall();dataBase.commit();dataBase.close();c=mycursor.rowcount
		try:
			if len(a)==0:print(_b);pp.config(text='                 ----- Enter Username ----- ',bg=_B,fg=_E)
			elif len(b)==0:print('Enter Password');pp.config(text='                 ----- Enter Password ----- ',bg=_B,fg=_E)
			elif c==1:username=entry1.get();password=entry2.get();pp.config(text='                 ----- login successful ----- ',bg=_B,fg=_F);ro.destroy();main.w(username,password)
			elif c==0:print('Invalid Login Credentials');pp.config(text=" ----- Invalid Login Credentials ----- \n Wrong password or username.Try again or \nclick 'forgot password' to recover it",bg=_B,fg=_C)
		except:print(_c)
w()
def forgotpass():
	E='....';D='..';C='.';B=False;A='380x280';ro.destroy();ro2=Tk();ro2.title(_O);ro2.geometry(A);ro2.config(bg=_B);con=B;fg=Label(ro2,text='FORGOT PASSWORD',font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=18);fg.place(x=110,y=20);l1=Label(ro2,text=_R,font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14);l2=Label(ro2,text=_d,font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14);_1entry1=Entry(ro2,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I);_1entry2=Entry(ro2,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I);pp2=Label(ro2,text=_a,bg=_B,fg=_E,cursor=_D,font=(_A,12));pp2.place(x=100,y=175)
	def defaultg():l1.place(x=20,y=81);l2.place(x=20,y=131);_1entry1.place(x=140,y=80);_1entry2.place(x=140,y=130)
	defaultg();un=_1entry1.get();pn=_1entry2.get();cpass=Button(ro2,text='confirm',command=lambda:errph(),height=1,width=19,pady=5,padx=10);cpass.place(x=110,y=210)
	def errph():
		pn=_1entry2.get();un=_1entry1.get()
		if un!='':
			pp2.place(x=100,y=175);pp2.config(text='')
			try:
				int(pn);cb=pn
				if len(cb)<10:pp2.config(text=_V,fg=_C);return
				elif len(cb)>10:pp2.config(text=_V,fg=_C);return
				elif len(cb)==10:pp2.after(200,lambda:pp2.config(text=C,fg=_F));pp2.after(400,lambda:pp2.config(text=D,fg=_F));pp2.after(600,lambda:pp2.config(text=E,fg=_F));pp2.after(800,lambda:pp2.config(text='.....loading',fg=_F));pp2.after(3000,lambda:checkun())
			except:pp2.config(text='enter a valid phone number!',fg=_C);return
		else:pp2.config(text='enter a username',fg=_C);pp2.place(x=120,y=175)
	def checkun():
		un=_1entry1.get();dataBase=mysql.connector.connect(host=db_hs,user=db_us,passwd=db_pw,database=db_db);mycursor=dataBase.cursor();sq=' Select * FROM acc WHERE username = %s';ad=un,;mycursor.execute(sq,ad);myresult=mycursor.fetchall();dataBase.commit();dataBase.close();c1=mycursor.rowcount
		if c1==1:pp2.after(1000,lambda:pp2.config(text='......successful',fg=_F));checkphno()
		elif c1==0:pp2.config(text='dude? seriously?\n atleast type a right username -_-',fg=_C);pp2.place(x=60,y=175);ro2.geometry(A);cpass.place(x=110,y=225)
	def checkphno():
		A='Are you sure thats your phone number? \n I guess not.\nCross check!';un=_1entry1.get();pn=_1entry2.get();dataBase=mysql.connector.connect(host=db_hs,user=db_us,passwd=db_pw,database=db_db);mycursor=dataBase.cursor();sq='SELECT * FROM acc WHERE username = %s and phno = %s';ad=un,pn;mycursor.execute(sq,ad);myresult=mycursor.fetchall();dataBase.commit();dataBase.close();c=mycursor.rowcount
		if c==1:pp2.place(x=60,y=170);pp2.after(1000,lambda:pp2.config(text=' ----- phno matched! ----- ',bg=_B,fg=_F));pp2.after(1000,lambda:changepass())
		elif c==0:pp2.after(1000,lambda:pp2.config(text=A,fg=_C));pp2.place(x=60,y=190);pp2.config(text=A,fg=_C);ro2.geometry('380x380');cpass.place(x=110,y=250)
	def changepass():
		global asd;un=_1entry1.get();asd=un;pn=_1entry2.get();ro2.geometry('380x250');l1.destroy();pp2.destroy();l2.destroy();_1entry2.destroy();_1entry1.destroy();cpass.destroy();res=Button(ro2,text='Change Password',command=lambda:clickcp()).place(x=130,y=170);pp3=Label(ro2,text='                     ',bg=_B,fg=_E,cursor=_D,font=(_A,12));pp3.place(x=100,y=210);fg.config(text='RESET PASSWORD');_1entry3=Entry(ro2,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I,show=_G);_1entry3.place(x=80,y=80);c_v=IntVar(value=0)
		def my_show():
			if c_v.get()==1:_1entry3.config(show='');_1entry3.after(1000,lambda:_1entry3.config(show=_G));_1entry3.after(1000,lambda:c1.deselect())
			else:_1entry3.config(show=_G)
		c1=Checkbutton(ro2,text=_S,font=(_A,10),height=1,variable=c_v,onvalue=1,offvalue=0,command=lambda:my_show(),bg=_B,fg=_E,activebackground=_B,activeforeground=_E,width=12,pady=0);c1.place(x=80,y=130);bcp=_1entry3.get()
		def clickcp():
			F='      ';A='         enter a password';global pb;bcp=_1entry3.get();pb=bcp;print(pb)
			def up_csv():
				with open(_J,mode='r')as cf:
					reader=csv.reader(cf,delimiter=_M)
					for line in reader:
						for i in line:
							if i==asd:x=line[0];pddf=pd.read_csv(_J);pddf.loc[(int(x)-1,_N)]=pb;pddf.to_csv(_J,index=B)
							else:continue
			while _L:
				try:
					if len(pb)>=4 and len(pb)<=20:pp3.after(200,lambda:pp3.config(text=C,fg=_F));pp3.after(400,lambda:pp3.config(text=D,fg=_F));pp3.after(600,lambda:pp3.config(text=E,fg=_F));pp3.after(800,lambda:pp3.config(text='.....',fg=_F));pp3.after(1000,lambda:pp3.config(text='......',fg=_F));pp3.after(1200,lambda:pp3.config(text='........',fg=_F));pp3.after(1400,lambda:pp3.config(text='...........',fg=_F));pp3.after(1600,lambda:pp3.config(text='.............',fg=_F));pp3.after(1800,lambda:pp3.config(text='...............loading',fg=_F));pp3.after(2000,lambda:pp3.config(text='............password reset successful',fg=_F));up_csv();break
					elif len(pb)=='':pp3.config(text=A,fg=_C);pp3.after(1000,lambda:pp3.config(text=F));return
					else:pp3.config(text=A,fg=_C);pp3.after(1000,lambda:pp3.config(text=F));return
				except ValueError:print(_W);return
			dataBase=mysql.connector.connect(host=db_hs,user=db_us,passwd=db_pw,database=db_db);mycursor=dataBase.cursor();sql='UPDATE acc SET pass = %s WHERE username = %s';val=bcp,un;mycursor.execute(sql,val);dataBase.commit();pp3.after(2300,lambda:ro2.destroy());pp3.after(2300,lambda:w())
def signup():
	ro.destroy();ro1=Tk();ro1.title(_O);ro1.geometry('380x500');ro1.config(bg=_B);Label(ro1,text='SIGN UP',font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14).place(x=140,y=20);l1=Label(ro1,text=_R,font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14);l2=Label(ro1,text=_d,font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14);l3=Label(ro1,text=_N,font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14);l4=Label(ro1,text='confirm \npassword',font=(_A,10),bg=_H,height=1,padx=2,pady=10,width=14);_1entry1=Entry(ro1,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I);_1entry2=Entry(ro1,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I);_1entry3=Entry(ro1,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I,show=_G);_1entry4=Entry(ro1,width=12,font=(_A,23),borderwidth=2,fg=_B,bg=_I,show=_G);_1sp=Button(ro1,text=_O,font=(_T,8),height=1,width=12,bg=_U,activebackground=_E,borderwidth=0,padx=9,pady=4,relief=GROOVE,command=lambda:click());_1sp.config(state=DISABLED)
	def en():_1sp.config(state=NORMAL)
	showme=IntVar(value=0)
	def showp():
		if showme.get()==1:_1entry3.config(show='');_1entry4.config(show='');_1entry3.after(1000,lambda:_1entry3.config(show=_G));_1entry4.after(1000,lambda:_1entry4.config(show=_G));_1entry4.after(1000,lambda:show.deselect())
		else:_1entry3.config(show=_G);_1entry4.config(show=_G)
	show=Checkbutton(ro1,text=_S,font=(_A,10),height=1,variable=showme,onvalue=1,offvalue=0,command=lambda:showp(),bg=_B,fg=_E,activebackground=_B,activeforeground=_E,width=12);robo=Checkbutton(ro1,text='i am not a robot',font=(_A,10),height=2,width=14,command=lambda:en())
	def defaultg():l1.place(x=20,y=71);l2.place(x=20,y=121);l3.place(x=20,y=171);l4.place(x=20,y=221);_1entry1.place(x=140,y=70);_1entry2.place(x=140,y=120);_1entry3.place(x=140,y=170);_1entry4.place(x=140,y=220);show.place(x=20,y=270);_1sp.place(x=140,y=350);robo.place(x=120,y=290)
	defaultg();a1=_1entry1.get();b1=0;k=_1entry2.get();c1=_1entry3.get();d1=_1entry4.get();print(k);s=Label(ro1,text=_K,bg=_B,fg=_F,font=(_A,12));s.place(x=20,y=370)
	def addacc(a1,b1,c1):dataBase=mysql.connector.connect(host=db_hs,user=db_us,passwd=db_pw,database=db_db);cursorObject=dataBase.cursor();sql='INSERT INTO acc (username, phno, pass) VALUES (%s, %s, %s)';val=a1,b1,c1;cursorObject.execute(sql,val);dataBase.commit();dataBase.close();print('account created!!');s.after(200,lambda:s.config(text='sign up successful'));s.after(2000,lambda:s.destroy());ro1.destroy();w()
	def add_csv(a1,b1,c1):
		ff=open(_J,mode='r');reader=csv.reader(ff,delimiter=_M);row_count=len(list(reader));ff.close();st=[]
		with open(_J,mode='a')as f:f=csv.writer(f,delimiter=_M);st.append([int(row_count/2),a1,b1,c1]);f.writerow(st[0])
	def click():
		A='username cannot have spaces \nusername can only contain alphanumeric characters and special characters such as ,_,.';a1=_1entry1.get();k=_1entry2.get();c1=_1entry3.get();d1=_1entry4.get()
		while _L:
			try:
				sca="`~!#@$%^&*()-=+{}[]:|;'\\<>?,/";dataBase=mysql.connector.connect(host=db_hs,user=db_us,passwd=db_pw,database=db_db);mycursor=dataBase.cursor();cnt=0;s='SELECT username FROM acc WHERE username = %s';ss=a1,;mycursor.execute(s,ss);myresult=mycursor.fetchall();cnt=mycursor.rowcount;dataBase.close()
				if a1.isspace():print('your username cant be a blank space');robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--your username cant be a blank space--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=121);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(a1)==0:print(_b);robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Enter username--',bg=_B,fg=_E,cursor=_D,font=(_A,12));h.place(x=60,y=121);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(a1.split())>1:print(A);robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text=A,bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=20,y=121);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(a1)<4:print('Should be more than 4 characters ');robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Should be more than 4 characters--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=121);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(a1)>20:print('Should be less than 20 characters ');robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Should be less than 20 characters--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=121);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif any((i in sca for i in a1)):print(A);robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text=A,bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=121);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif cnt==1:
					print('The username already exists');robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);ran1=_K;cont=0
					while _L:
						ran=str(randint(0,9));cont+=1;ran1+=ran
						if cont==3:break
						else:continue
					a2=a1+ran1;a3=ran1+a1;h=Label(ro1,text='--The username already exists--\n try adding numerics,_,.'+a2+'or'+a3,bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=20,y=121);h.after(3000,lambda:h.destroy());_1sp.after(3000,lambda:defaultg());return
				elif cnt!=1 and len(a1)>=4 and len(a1)<=20:break
				else:print('wrong input');robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--wrong inout--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=121);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
			except ValueError:print('Invalid username! ...')
		while _L:
			try:
				int(k);b1=k
				if b1=='':print('Enter your phone number');robo.deselect();_1sp.config(state=DISABLED);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Enter your phone number--',bg=_B,fg=_E,cursor=_D,font=(_A,12));h.place(x=60,y=171);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(b1.split())>1:print(A);robo.deselect();_1sp.config(state=DISABLED);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text=A,bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=20,y=171);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(b1)<10:print('should be 10 digit number');robo.deselect();_1sp.config(state=DISABLED);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--should be 10 digit number--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=171);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(b1)>10:print('should be a 10 digit number');robo.deselect();_1sp.config(state=DISABLED);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text=_V,bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=171);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(b1)==10:print('valid phone number');break
				else:print(_c);robo.deselect();_1sp.config(state=DISABLED);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--something is wrong--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=171);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
			except:print('Invalid number!\n make sure you entered a number ...');robo.deselect();_1sp.config(state=DISABLED);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Invalid number!\n make sure you entered a number--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=171);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
		while _L:
			try:
				if c1.isspace():print('Try again!');robo.deselect();_1sp.config(state=DISABLED);l2.place(x=20,y=171);l3.place(x=20,y=221);l4.place(x=20,y=271);_1entry2.place(x=140,y=170);_1entry3.place(x=140,y=220);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Try again!--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=121);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(c1)==0:print('enter password');robo.deselect();_1sp.config(state=DISABLED);l4.place(x=20,y=271);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Enter password!--',bg=_B,fg=_E,cursor=_D,font=(_A,12));h.place(x=60,y=221);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif a1==c1:print('username cannot be the password');robo.deselect();_1sp.config(state=DISABLED);l4.place(x=20,y=271);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--username cannot be the password--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=221);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif len(c1)>=4 and len(c1)<=20:c1=c1.replace(_K,'');break
				else:print('Cannot have more than 20 characters');robo.deselect();_1sp.config(state=DISABLED);l4.place(x=20,y=271);_1entry4.place(x=140,y=270);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Cannot have more than 20 characters--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=221);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
			except ValueError:print(_W)
		while _L:
			try:
				d1=d1.replace(_K,'');print(c1);print(d1)
				if len(d1)==0:print('Enter the password again!');robo.deselect();_1sp.config(state=DISABLED);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--Enter the password again--',bg=_B,fg=_E,cursor=_D,font=(_A,12));h.place(x=60,y=271);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
				elif d1==c1:robo.deselect();_1sp.config(state=DISABLED);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--password matched--',bg=_B,fg=_F,cursor=_D,font=(_A,12));h.place(x=60,y=271);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());break
				else:robo.deselect();_1sp.config(state=DISABLED);_1sp.place(x=140,y=380);robo.place(x=120,y=320);h=Label(ro1,text='--password dosent match--',bg=_B,fg=_C,cursor=_D,font=(_A,12));h.place(x=60,y=271);h.after(2000,lambda:h.destroy());_1sp.after(2000,lambda:defaultg());return
			except ValueError:print(_W)
		addacc(a1,b1,c1);add_csv(a1,b1,c1)
def run():bicreate();csvcreate();o=open(_P,_Q);q=pickle.load(o);o.close();db_pw=q[_X];db_db=q['db'];db_us=q[_Y];db_hs=q[_Z];sqlcreate();w()
ro.mainloop()