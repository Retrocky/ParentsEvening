import csv

filename = 'ParentsEvening.csv'

reader = csv.DictReader(open(filename))
for raw in reader:
    print(raw)

class Student:
    def __init__(self,name,teachers,eveningarrival,eveningdeparture):
        self.name = name
        self.teachers = teachers
        self.eveningarrival = eveningarrival
        self.eveningdeparture = eveningdeparture
