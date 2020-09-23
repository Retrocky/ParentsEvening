# TO DO LIST
# Slot gap needed in-between each students appointment - DOING
# Allow for student evening timings
# Show time for each appointment - DOING
# Need to take in data from csv and format it to work in here
# Priority weightings

slots = []
excluded = []
breakList = []
empty = 0
appointmentLength = 5
appointmentDivisible = 0.12

teacherlist = ['Mr.Walter','Mr.Jeff','Ms.Gary','Ms.Onion']

studentTeacher = {'Will':'Mr.Walter,Ms.Gary,Mr.Jeff,Ms.Onion','Bob':'Mr.Jeff,Ms.Onion,Mr.Walter',
                      'Gee':'Mr.Walter,Mr.Jeff,Ms.Onion,Ms.Gary','Jack':'Mr.Jeff,Ms.Onion,Mr.Walter',
                      'Harry':'Ms.Onion,Ms.Gary','Alice':'Ms.Gary,Ms.Gary','Emily':'Mr.Walter,Mr.Jeff,Ms.Onion,Ms.Gary',
                      'Ben':'Mr.Walter,Mr.Jeff,Ms.Onion,Ms.Gary','Bug':'monkey','AnotherBug':'28828199282991',}

StartTime = 7
EndTIme = 8.5
TotalSlots = int((EndTIme - StartTime)*12)
print('Number of slots : '+str(TotalSlots))

# Outputs slots
def outputSlots():
    print('='*100)
    for item in slots:
        if 'Slot : ' in item:
            print("")
            print('-'*50)
            print(item)
        else:
            print(item)
    print('='*100)

# Checks if the slot has already been made
def checkSlot(teacher,student):
    if len(slots) == 0:
        return True
    else:
        for appointment in slots:
            if (teacher+" : "+student) == appointment:
                return False
        return True

def emptySlot(teacher):
    slots.append((teacher+" : BREAK"))

# Creates slots and excludes students from another appointment that time slot
def createSlot(teacher,student,slot):
    slots.append((teacher+" : "+student))
    excludeStudent(student)
    addBreak(student,slot)

def addBreak(student,slot):
    breakList.append((slot,student))

def checkBreaks(slot):
    for item in breakList:
        if slot >= item[0]+2:
            breakList.remove(item)
            checkBreaks(slot)

def onBreak(student):
    if student in breakList:
        return True
    else:
        return False

def excludeStudent(student):
    excluded.append(student)

def checkExcluded(student):
    if student in excluded:
        return True
    else:
        return False

def clearExcluded():
    excluded.clear()

# Loops through each slot with each teacher and matches students to their teachers needed
def slotSorter(TotalSlots,teacherlist,Students):
    for i in range(TotalSlots):
        checkBreaks(i)
        clearExcluded()
        slots.append('Slot : '+str(i)+' Time : '+str(StartTime)+':'+str(float(appointmentDivisible*i)*60))
        for teacher in teacherlist:
            slotCreated = False
            for student in Students.keys():
                if teacher in Students[student]:
                    if checkSlot(teacher,student) and not checkExcluded(student) and not onBreak(student):
                        createSlot(teacher,student,i)
                        slotCreated = True
                        break
            if slotCreated == False:
                emptySlot(teacher)
    outputSlots()

slotSorter(TotalSlots,teacherlist,studentTeacher)