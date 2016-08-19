keys = ['a', 'b', 'c', 'd']
values = [1, 2, 3]
result = {}
for i in range(len(keys)):
   try:
       result [keys[i]] = values[i]
   except:
       result[keys[i]]="None"
print(result)