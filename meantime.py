import time
import pickle
import os
import sys
end_string = "/home/pi/Hotspot/ttnpub 0,0,0,0,0,0,{}"

session_count = 1
mac_frac = 0
apple_count = 1
start_time = time.time()
instance = None
people = []
num_lines = sum(1 for line in open('hashFile'))



def findElement(x):
	for i in people:
		if i.mac == x:
			return people.index(i)

def main(argv):
	
	if argv == "run":
		if(instance ==0):
			genData()
			saveData()
			sys.exit()
		loadData()
		genData()
		saveData()
		outputData()
	if argv == "refresh":
		refresh()
		printPeople()
	if argv == "day":
		loadData()
		endDay()
		refresh()
	if argv == "load":
		print "loading data"
		loadData()
	if argv == "print":
		loadData()
		printPeople()
		

#Use pickle to save "people" List
def saveData():
	global instance
	global mac_frac

	mac_frac = (mac_frac +(apple_count/session_count))/2
	if instance == None:
		instance = 1
	else:
		instance+=1
	data = [people,instance,mac_frac]
	pickle.dump(data,open("/home/pi/Hotspot/Data.pkl","wb"))
	#print "Data Saved, Instance:", instance
	#printPeople()
#use pickle to load "people" List
def loadData():
	global people
	global instance
	global session_count
	global mac_frac
	data = []
	data  = pickle.load(open("/home/pi/Hotspot/Data.pkl","rb")) 
	#print "Data loaded"
	people = data[0]
	instance= data[1]
	mac_frac = data[2]
	for i in people:
		search = str(i.mac) + "\n"
		macSearch(search)
	#printPeople()
#seach through "people" list to find mac entry
def peopleSearch(id):
	global current_id

	for x in range(0,len(people)):
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
			if people[findElement(id[:-1])].state == 1:
				people[findElement(id[:-1])].misscount += 1
				if people[findElement(id[:-1])].misscount >=3:
					people[findElement(id[:-1])].state = 0
					people[findElement(id[:-1])].misscount = 0
			return None
def updateExisting(id):
	current_id = findElement(id)
	people[current_id].lastSeen = long(time.time())
	people[current_id].duration = long(people[current_id].lastSeen - people[current_id].start)
	people[current_id].misscount = 0

def createEntry(mac):
	global apple_count
	apple = None
	if "A" in mac:
		apple = 1
		apple_count+=1
	else:
		apple = 0
	people.append(user(mac,1,long(start_time),long(start_time),0,0,apple))



#Print Structure
def printPeople():
	print "mac                             |State|Start       |lastSeen     |duration|misscount|apple"
	print "=============================================================================================="
	for x in range(0,len(people)):
		print people[x].mac + "|" ,  people[x].state , "  |" ,people[x].start,"|" ,people[x].lastSeen , "|", people[x].duration ,"     |", people[x].misscount, "|",people[x].apple

#Data Structure
class user(object):
	def __init__(self,mac,state,start,lastSeen,duration,misscount,apple):
		self.mac = mac
		self.state = state
		self.start = start
		self.lastSeen = lastSeen
		self.duration = duration
		self.misscount = misscount
		self.apple = apple


def genData():
	global session_count
	with open('hashFile') as infile:
		for line in infile:
			session_count+=1
			id = peopleSearch(line[:-1])
			if id != None:	
				updateExisting(id)
			else:
				createEntry(line[:-1])
def outputData():
	#calculate the data to get sent
	#sys.stdout.write(str(meanTime()) + " " + str(len(people)))
	sys.stdout.write(str(meanTime()) + " " + str(totPeople()))
	

def meanTime():
	sum = 0
	for i in people:
		if i.apple == 1:
			continue
		sum += int(i.duration/60)
	return sum/len(people)

def totPeople():
	sum=0
	for i in people:
		if i.duration == 0:
			continue
		sum = sum +1
	return sum

def endDay():
	count = len(people) * mac_frac
	count = int(count)
	os.system(end_string.format(count))
def refresh():
	global people
	global instance
	global mac_frac
	
	people = []
	instance = 0
	mac_frac = 0
	saveData()
if __name__ == "__main__":
	main(sys.argv[1])
