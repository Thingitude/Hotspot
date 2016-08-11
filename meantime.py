import time
import pickle
import sys

start_time = time.time()
current_id = 0
instance = None
people = []

def main(argv):
	
	if argv == "run":
		loadData()
		saveData()
		genData()
	if argv == "save":
		genData()
		people_count = len(people)
		#people.append(user(1,2,3,3,4))
		print "saving data"
		saveData()
	if argv == "load":
		print "loading data"
		loadData()
		

#Use pickle to save "people" List
def saveData():
	global instance
	if instance == None:
		instance = 1
	else:
		instance+=1
	data = [people,instance]
	pickle.dump(data,open("Data.pkl","wb"))
	print "Data Saved, Instance:", instance
	printPeople()
#use pickle to load "people" List
def loadData():
	global people
	global instance
	data = []
	data  = pickle.load(open("Data.pkl","rb")) 
	print "Data loaded"
	people = data[0]
	instance= data[1]
	printPeople()
#seach through "people" list to find mac entry
def macSearch(id):
	print "MACSEARCH"
	position = None
	for x in range(0,len(people)):
		print "Number:",x
		if people[x].mac == id:
			
			current_id = x
			return id
			#return index of entry	
	return None

def updateExisting(id):
	print "updating"
	people[current_id].lastSeen = time.time()

def createEntry(mac):
	people.append(user(mac,1,start_time,start_time,0,0))
	print "creating"


#Print Structure
def printPeople():
	print "mac  |State|Start          |lastSeen       |duration|misscount"
	print "=============================================================="
	for x in range(0,len(people)):
		print people[x].mac + "|" ,  people[x].state , "  |" ,people[x].start,"|" ,people[x].lastSeen , "|", people[x].duration ,"     |", people[x].misscount

#Data Structure
class user(object):
	def __init__(self,mac,state,start,lastSeen,duration,misscount):
		self.mac = mac
		self.state = state
		self.start = start
		self.lastSeen = lastSeen
		self.duration = duration
		self.misscount = misscount



def genData():
	with open('hashFile') as infile:
		for line in infile:

			id = macSearch(line[:-1])
			if id != None:	
				updateExisting(id)
			else:
				createEntry(line[:-1])

if __name__ == "__main__":
	main(sys.argv[1])

