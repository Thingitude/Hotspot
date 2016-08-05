from pprint import pprint 
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
		


def saveData():
	pickle.dump(people,open("Data.pkl","wb"))
	print "Data Saved"
	printPeople()

def loadData():
	global people
	people = pickle.load(open("Data.pkl","rb"))	
	print "Data loaded"
	printPeople()
	
	
	
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
			people.append(user(line[:-1],1,start_time,4,0))




if __name__ == "__main__":
	main(sys.argv[1])
