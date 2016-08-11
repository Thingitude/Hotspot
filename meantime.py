import time
import pickle
import sys

start_time = time.time()
instance = None
people = []
num_lines = sum(1 for line in open('hashFile'))

#Data Structure
class user(object):
	def __init__(self,mac,state,start,lastSeen,duration,misscount):
		self.mac = mac
		self.state = state
		self.start = start
		self.lastSeen = lastSeen
		self.duration = duration
		self.misscount = misscount


def main(argv):
	
	if argv == "run":
		if(instance ==0):
			saveData()
			sys.exit()
		loadData()
		genData()
		saveData()
		outputData()
	if argv == "save":
		genData()
		people_count = len(people)
		
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
	for i in people:
		search = str(i.mac) + "\n"
		macSearch(search)
	printPeople()

def genData():
	with open('hashFile') as infile:
		for line in infile:

			id = peopleSearch(line[:-1])
			if id != None:	
				updateExisting(id)
			else:
				createEntry(line[:-1])
#seach through "people" list to find mac entry
def peopleSearch(id):
	global current_id

	for x in range(0,num_lines):
		if people[x].mac == id:
			
			current_id = x
			return id
			#return index of entry	
	return None
def macSearch(id):

	with open('hashFile') as infile:
		if id in infile:
			return findElement(id[:-1])
			print "located"
		else:
			people[findElement(id[:-1])].misscount += 1
			if people[findElement(id[:-1])].misscount >=3:
				people[findElement(id[:-1])].state = 0
			return None

def createEntry(mac):
	people.append(user(mac,1,long(start_time),long(start_time),0,0))



def updateExisting(id):
	current_id = findElement(id)
	people[current_id].lastSeen = long(time.time())
	people[current_id].duration = long(people[current_id].lastSeen - people[current_id].start)
	people[current_id].misscount = 0

#Print Structure
def printPeople():
	print "mac  |State|Start          |lastSeen     |duration|misscount"
	print "=============================================================="
	for x in range(0,len(people)):
		print people[x].mac + "|" ,  people[x].state , "  |" ,people[x].start,"|" ,people[x].lastSeen , "|", people[x].duration ,"     |", people[x].misscount
#Search for element based on mac address
def findElement(x):
	for i in people:
		if i.mac == x:
			return people.index(i)
#Use standard output to output the data
def outputData():

	sys.stdout(str(len(people)+","+meanTime() ) 
#Calculate the mean duration
def meanTime():
	sum = 0
	for i in people:
		sum += int(i.duration*0.000016667)
	return sum/len(people)
if __name__ == "__main__":
	main(sys.argv[1])