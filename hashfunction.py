import sys
import hashlib
data = sys.stdin.readlines()
datastr= ''.join(data)
hash = hashlib.sha1(datastr.encode("UTF-8")).hexdigest()
sys.stdout(hash[:10])