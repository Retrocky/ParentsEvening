# TO DO LIST
# Allow for student evening timings
# Need to take in data from csv and format it to work in here
# Priority weightings

slots = []
excluded = []
breakList = []
breakList2 = []
empty = 0
appointmentLength = 5
appointmentDivisible = appointmentLength/60

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
    #addBreak(student)

'''
def addBreak(student):
    breakList.append(student)

def clearBreaks(slot):
    if slot == slot-1:
        print('CLEARING BREAKLIST')
        breakList.clear()

def onBreak(student):
    for item in slots[::-1]:
        if 'Slot : ' in item:
            for i in range(0,4):
                try:
                    nice = slots[slots.index(item)-i]
                    print(nice)
                    if student in nice:
                        return True

                except:
                    return False
    return False
'''

def excludeStudent(student):
    excluded.append(student)

def checkExcluded(student):
    if student in excluded:
        return True
    else:
        return False

def clearExcluded():
    excluded.clear()

def slotHeading(slot,StartTime):
    time = StartTime+appointmentDivisible*slot
    hours = int(time)
    minutes = (time * 60) % 60
    minutes = str(int(minutes.__round__()))
    if len(minutes) == 1:
        minutes = '0'+minutes
    time = str(hours)+':'+str(minutes)
    slots.append('Slot : '+str(slot)+' Time : '+str(time))

# Loops through each slot with each teacher and matches students to their teachers needed
def slotSorter(TotalSlots,teacherlist,Students):
    for i in range(TotalSlots):
        clearExcluded()
        slotHeading(i,StartTime)
        for teacher in teacherlist:
            slotCreated = False
            for student in Students.keys():
                if teacher in Students[student]:
                    if checkSlot(teacher,student) and not checkExcluded(student):
                        createSlot(teacher,student,i)
                        slotCreated = True
                        break
            if slotCreated == False:
                emptySlot(teacher)
    outputSlots()

slotSorter(TotalSlots,teacherlist,studentTeacher)