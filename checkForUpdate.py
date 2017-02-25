with open ("/home/pi/HotspotUpdates/new/Version", "r") as myfile:
  data=myfile.read() 

with open ("/home/pi/HotspotUpdates/current/Version", "r") as myoldfile:
  current=myoldfile.read()

if current == data:
  print 1
else:
  print 2
