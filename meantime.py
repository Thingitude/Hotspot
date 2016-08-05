import time
import pickle
import sys

start_time = time.time()


people = []

def main(argv):
	
	
	if argv == "save":
		genData()
		#people.append(user(1,2,3,3,4))
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
			print "The id is ", id
			return id
			#return index of entry
		else:
			return  None		
			#if not present return none

def updateExisting(id):
	print "updating"
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
	#create emp list
	with open('hashFile') as infile:
		for line in infile:
			id = macSearch(line[:-1]) 
			if id != None:	
				updateExisting(id)
			else:
				createEntry(line[:-1])
				

if __name__ == "__main__":
	main(sys.argv[1])
	
