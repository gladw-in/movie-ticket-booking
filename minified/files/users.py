T='rb'
S='db.dat'
R=open
E='123456'
B='*'
A=print
import mysql.connector,pickle as M,DB_config as N
while True:
	try:L=R(S,T)
	except FileNotFoundError:N.run()
	L=R(S,T);J=M.load(L);L.close();G=J['pass'];K=J['db'];H=J['user'];I=J['host'];A('1 to show database');A('2 to create moviebooking database');A('3 to drop table');A('4 to add acc table');A('5 to insert random users');A('6 to delete database');A('7 to exit');D=input('Your choice ');D=D.lower()
	try:
		if D=='1'or D=='one':
			C=mysql.connector.connect(host=I,user=H,passwd=G);F=C.cursor();F.execute('show databases');A(B*25)
			for O in F:A(O)
			A(B*25);C.close()
		elif D=='2'or D=='two':
			try:C=mysql.connector.connect(host=I,user=H,passwd=G);F=C.cursor();F.execute(f"create database {K}");C.close();A(B*25);A('moviebooking database created');A(B*25)
			except mysql.connector.errors.DatabaseError:A(B*25);A('database already exists');A(B*25)
		elif D=='3'or D=='three':
			try:C=mysql.connector.connect(host=I,user=H,passwd=G,database=K);F=C.cursor();F.execute('DROP TABLE IF EXISTS acc');C.close();A(B*25);A('Table dropped');A(B*25)
			except mysql.connector.errors.ProgrammingError:A(B*25);A('database doesnt exist');A(B*25)
		elif D=='4'or D=='four':
			try:C=mysql.connector.connect(host=I,user=H,passwd=G,database=K);F=C.cursor();F.execute('CREATE TABLE acc (username VARCHAR(255) PRIMARY KEY, phno VARCHAR(255), pass VARCHAR(255))ENGINE=InnoDB DEFAULT CHARSET=latin1');C.commit();C.close();A(B*25);A('acc table created');A(B*25)
			except mysql.connector.errors.ProgrammingError:A(B*25);A('Aleady created or Database deosnt exist');A(B*25)
		elif D=='5'or D=='five':
			try:C=mysql.connector.connect(host=I,user=H,passwd=G,database=K);F=C.cursor();P='INSERT INTO acc VALUES(%s,%s,%s)';Q=[('Peter','9822284582',E),('Joshua','9822245582',E),('Vidhya','9822245829',E),('Dhruv','9822724582 ',E),('Mrinal','9822245822',E),('Tnok','9872224582',E),('Tanishk','9820229482',E),('Abhik','9822924582',E),('William','9820224582',E),('Pranit','9892224582',E),('Rashmi','9821224582',E),('Harshith','9821924582',E),('Glad432','9902671253',E),('Admin','9821024582',E)];F.executemany(P,Q);C.commit();C.close();A(B*25);A('Values Added');A(B*25)
			except mysql.connector.errors.IntegrityError:A(B*25);A('Values Already added');A(B*25)
			except mysql.connector.errors.ProgrammingError:A(B*25);A('database or table doesnt exist');A(B*25)
		elif D=='6'or D=='six':
			try:C=mysql.connector.connect(host=I,user=H,passwd=G);F=C.cursor();F.execute('drop database movie_ticketbooking');A(B*25);A('Database deleted');A(B*25);C.close()
			except mysql.connector.errors.DatabaseError:A(B*25);A('Database doesnt exist');A(B*25)
		elif D=='7'or D=='seven'or D=='quit'or D=='exit':break
		else:A(B*25);A('Wrong try again!!');A(B*25)
	except mysql.connector.errors.InterfaceError:A(B*25);A('problem with MYSQL server');A(B*25)