import pickle as B
def run():C='localhost';D='root';E=input('Enter password ');F='movie_ticketbooking';G={'host':C,'user':D,'pass':E,'db':F};A=open('db.dat','wb');B.dump(G,A);A.close()
