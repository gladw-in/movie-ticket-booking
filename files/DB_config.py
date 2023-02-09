import pickle


def run():
    a = "localhost"
    b = "root"
    c = input("Enter password ")
    d = "movie_ticketbooking"
    data = {"host": a, "user": b, "pass": c, "db": d}
    f = open("db.dat", "wb")
    pickle.dump(data, f)
    f.close()
