import hashlib
hashStr = None
readStr = None
currentMac = None
open("hashFile","w").close()
hashFile = open("hashFile","wb")

def main():
    global hashFile
    global currentMac
    with open('macFile') as macFile:
        for line in macFile:
            currentMac = line
            hashMac()
    hashFile.close()
    open("macFile","w").close()
            

def isApple(firstEight):
    if firstEight in open ('appleM').read():
        print "APPLE"
        return True

def hashMac():
    hashobject = hashlib.md5(currentMac.encode())
    hashStr = hashobject.hexdigest()
    
    if(isApple(currentMac[:8])):
        hashStr = "A"+ hashStr
    
    print "MAC:",currentMac
    print "HASH: ",hashStr
    hashFile.write(hashStr +"\n")


if __name__ == "__main__":
	main()
