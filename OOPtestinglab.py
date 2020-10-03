dict = {'Will':1,'Bob':3,'Gee':2,'Harry':3}
sortedList = []
flipped = {}

for key, value in dict.items():
    if value not in flipped:
        flipped[value] = [key]
    else:
        flipped[value].append(key)

for weight in range(1,4):
    for i in range(len(flipped[weight])):
        sortedList.append(flipped[weight][i])

print(sortedList)
new = []

for i in reversed(sortedList):
    new.append(i)

print(new)