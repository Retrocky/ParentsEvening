import csv
import pandas


filename = 'ParentsEvening.csv'

'''
reader = csv.DictReader(open(filename))
for raw in reader:
    #print(raw)

class Student:
    def __init__(self,name,teachers,eveningarrival,eveningdeparture):
        self.name = name
        self.teachers = teachers
        self.eveningarrival = eveningarrival
        self.eveningdeparture = eveningdeparture
'''

'''
breaklist = ['Harry','Jack']
print(breaklist)
breaklist.remove('Harry')
print(breaklist)
'''

dict = {}
startTimes = {}
endTimes = {}

data = pandas.read_csv(filename)
for i in range(len(data.index)):
    item = data.loc[i]
    dict[item[0]] = item[1]
    startTimes[item[0]] = item[2]
    endTimes[item[0]] = item[3]

print(dict)
print(startTimes)
print(endTimes)
