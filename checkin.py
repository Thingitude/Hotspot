import threading 
import time
start_time = time.time()
end_time =0
people = []

#Print Structure
def printPeople():
	print "mac |State|Duration"
	print "==================="
	for x in range(0,len(people)):
		print people[x].mac + "|" ,  people[x].state , "  |"  ,people[x].duration

#Data Structure
class user(object):
	def __init__(self,mac,state,duration):
		self.mac = mac
		self.state = state
		self.duration = duration


def timer():
	end_time = time.time() - start_time
	print int(end_time)
	threading.Timer(1, timer).start()


#create emp list
with open('hashFile') as infile:
	for line in infile:
		people.append(user(line[:-1],1,3))



#for p in people: print p.state

printPeople()
