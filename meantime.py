import time
import pickle
import sys

start_time = time.time()


people = []

def main(argv):
	
	if argv == "save":
		genData()
		people.append(user("TEST",2,3,4,5))
		print "saving data"
		saveData()
	if argv == "load":
		print "loading data"
		loadData()
		

#Use pickle to save "people" List
def saveData():
	pickle.dump(people,open("Data.pkl","wb"))
	print "Data Saved"
	printPeople()
#use pickle to load "people" List
def loadData():
	global people
	people = pickle.load(open("Data.pkl","rb"))	
	print "Data loaded"
	printPeople()
#seach through "people" list to find mac entry
def macSearch(id):
position = None
	for x in range(0,len(people)):
		if people[x].mac == id:
			return id
			#return index of entry
		else:
			return  None		
			#if not present return none

def updateExisting():


def createEntry():


#Print Structure
def printPeople():
	print "mac  |State|lastSeen   |duration|misscount"
	print "======================================"
	print len(people)
	for x in range(0,len(people)):
		print people[x].mac + "|" ,  people[x].state , "  |"  ,people[x].lastSeen , "|", people[x].duration ,"   |", people[x].misscount

#Data Structure
class user(object):
	def __init__(self,mac,state,lastSeen,duration,misscount):
		self.mac = mac
		self.state = state
		self.lastSeen = lastSeen
		self.duration = duration
		self.misscount = misscount



def genData():
	#create emp list
	with open('hashFile') as infile:
		for line in infile:
			id = macSearch[line[:-1]]
			if id != None:	
				updateExisting(id)
			else:
				createEntry()

if __name__ == "__main__":
	main(sys.argv[1])
