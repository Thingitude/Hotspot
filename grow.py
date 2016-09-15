import sys

while 1:	# we do this forever
	mac=sys.stdin.readline()
	print(mac)
	if mac == "bc:6e:64:e4:01:c8\n":
		print("Found Mark!!")
		break

	if mac == "68:fb:7e:cf:2e:79\n":
		print("Found Tom!!")
		break

	if mac == "c0:63:94:0d:ad:11\n":
		print("Found Alex!!")
		break

	if mac == "c0:63:94:0d:43:33\n":
		print("Found Alex!!")
		break



