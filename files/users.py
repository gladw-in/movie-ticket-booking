import mysql.connector
import pickle
import DB_config as db

while True:
    try:
        o = open("db.dat", "rb")

    except FileNotFoundError:
        db.run()
    o = open("db.dat", "rb")
    q = pickle.load(o)
    o.close()
    pass_ = q["pass"]
    db_ = q["db"]
    user_ = q["user"]
    host_ = q["host"]

    print("1 to show database")
    print("2 to create moviebooking database")
    print("3 to drop table")
    print("4 to add acc table")
    print("5 to insert random users")
    print("6 to delete database")
    print("7 to exit")
    ch = input("Your choice ")
    ch = ch.lower()

    try:
        if ch == "1" or ch == "one":
            dataBase = mysql.connector.connect(host=host_, user=user_, passwd=pass_)
            mycursor = dataBase.cursor()
            mycursor.execute("show databases")
            print("*" * 25)

            for x in mycursor:
                print(x)
            print("*" * 25)

            dataBase.close()

        elif ch == "2" or ch == "two":
            try:
                dataBase = mysql.connector.connect(host=host_, user=user_, passwd=pass_)
                mycursor = dataBase.cursor()
                mycursor.execute(f"create database {db_}")
                dataBase.close()
                print("*" * 25)
                print("moviebooking database created")
                print("*" * 25)

            except mysql.connector.errors.DatabaseError:
                print("*" * 25)
                print("database already exists")
                print("*" * 25)

        elif ch == "3" or ch == "three":
            try:
                dataBase = mysql.connector.connect(
                    host=host_, user=user_, passwd=pass_, database=db_
                )
                mycursor = dataBase.cursor()
                mycursor.execute("DROP TABLE IF EXISTS acc")
                dataBase.close()
                print("*" * 25)
                print("Table dropped")
                print("*" * 25)
            except mysql.connector.errors.ProgrammingError:
                print("*" * 25)
                print("database doesnt exist")
                print("*" * 25)

        elif ch == "4" or ch == "four":
            try:
                dataBase = mysql.connector.connect(
                    host=host_, user=user_, passwd=pass_, database=db_
                )
                mycursor = dataBase.cursor()

                mycursor.execute(
                    "CREATE TABLE acc (username VARCHAR(255) PRIMARY KEY, phno VARCHAR(255), pass VARCHAR(255))ENGINE=InnoDB DEFAULT CHARSET=latin1"
                )
                dataBase.commit()

                dataBase.close()
                print("*" * 25)
                print("acc table created")
                print("*" * 25)
            except mysql.connector.errors.ProgrammingError:
                print("*" * 25)
                print("Aleady created or Database deosnt exist")
                print("*" * 25)

        elif ch == "5" or ch == "five":
            try:
                dataBase = mysql.connector.connect(
                    host=host_, user=user_, passwd=pass_, database=db_
                )
                mycursor = dataBase.cursor()
                s = "INSERT INTO acc VALUES(%s,%s,%s)"
                v = [
                    ("Peter", "9822284582", "123456"),
                    ("Joshua", "9822245582", "123456"),
                    ("Vidhya", "9822245829", "123456"),
                    ("Dhruv", "9822724582 ", "123456"),
                    ("Mrinal", "9822245822", "123456"),
                    ("Tnok", "9872224582", "123456"),
                    ("Tanishk", "9820229482", "123456"),
                    ("Abhik", "9822924582", "123456"),
                    ("William", "9820224582", "123456"),
                    ("Pranit", "9892224582", "123456"),
                    ("Rashmi", "9821224582", "123456"),
                    ("Harshith", "9821924582", "123456"),
                    ("Glad432", "9902671253", "123456"),
                    ("Admin", "9821024582", "123456"),
                ]
                mycursor.executemany(s, v)
                dataBase.commit()
                dataBase.close()
                print("*" * 25)
                print("Values Added")
                print("*" * 25)
            except mysql.connector.errors.IntegrityError:
                print("*" * 25)
                print("Values Already added")
                print("*" * 25)
            except mysql.connector.errors.ProgrammingError:
                print("*" * 25)
                print("database or table doesnt exist")
                print("*" * 25)
        elif ch == "6" or ch == "six":
            try:
                dataBase = mysql.connector.connect(host=host_, user=user_, passwd=pass_)
                mycursor = dataBase.cursor()
                mycursor.execute("drop database movie_ticketbooking")
                print("*" * 25)
                print("Database deleted")
                print("*" * 25)
                dataBase.close()
            except mysql.connector.errors.DatabaseError:
                print("*" * 25)
                print("Database doesnt exist")
                print("*" * 25)
        elif ch == "7" or ch == "seven" or ch == "quit" or ch == "exit":
            break
        else:
            print("*" * 25)
            print("Wrong try again!!")
            print("*" * 25)
    except mysql.connector.errors.InterfaceError:
        print("*" * 25)
        print("problem with MYSQL server")
        print("*" * 25)
