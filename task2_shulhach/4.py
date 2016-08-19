import re
from collections import Counter
f = open('ip.txt')
data = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', f.read())
for ip in Counter(data).most_common(10):
    print (ip[0])