slots = []
excluded = []
empty = 0
teacherlist = ['Mr.Walter','Mr.Jeff','Ms.Gary','Ms.Onion']
Students = {'Will':'Mr.Walter,Ms.Gary','Bob':'Mr.Jeff,Ms.Onion'}
# Introducing a harder students list with 'Gee' needing one of Bob's teachers and one of Will's teachers
HarderStudents = {'Will':'Mr.Walter,Ms.Gary','Bob':'Mr.Jeff,Ms.Onion','Gee':'Mr.Walter,Mr.Jeff'}

EvenHarderStudents = {'Will':'Mr.Walter,Ms.Gary,Mr.Jeff,Ms.Onion','Bob':'Mr.Jeff,Ms.Onion,Mr.Walter',
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
        if 'Slot :' in item:
            print("")
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
def createSlot(teacher,student):
    slots.append((teacher+" : "+student))
    excludeStudent(student)

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
        clearExcluded()
        slots.append('Slot :'+str(i))
        for teacher in teacherlist:
            slotCreated = False
            for student in Students.keys():
                if teacher in Students[student]:
                    if checkSlot(teacher,student) and not checkExcluded(student):
                        createSlot(teacher,student)
                        slotCreated = True
                        break
            if slotCreated == False:
                emptySlot(teacher)
    outputSlots()

slotSorter(TotalSlots,teacherlist,EvenHarderStudents)

# Stop the occurence of a teacher and student having multiple appointemnts per time slot