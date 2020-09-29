import time
# TO DO LIST
# Student timings constraint
# CSV input - Extension google form -> CSV -> Python - DOING
# Priority weightings constraint
# Add breaks - FIXING

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

temp = studentTeacher.copy()

StartTime = 7
EndTIme = 8.5
TotalSlots = int((EndTIme - StartTime)*12)
print('Number of slots : '+str(TotalSlots))

def menu():
    print('+'*100)
    print('')
    print('Parents Evening Scheduler')
    print('')
    print('1 - Run algorithm with default settings')
    print('2 - Change settings')
    print('3 - Exit')
    print('')
    value = input('Enter choice : ')
    print('+'*100)
    checkMenuValues(value)

def checkMenuValues(value):
    try:
        value = int(value)
        if value == 1:
            slotSorter(TotalSlots, teacherlist, studentTeacher, temp)
        elif value == 2:
            pass
        elif value == 3:
            exit()
        else:
            print('Invalid choice - Please try again.')
            print('')
            menu()
    except ValueError:
        print('Enter a digit from 1 -> 3')
        print('')
        menu()

# Outputs slots
def outputSlots():
    print('='*100)
    for item in slots:
        if 'Slot : ' in item:
            time.sleep(0.5)
            print("")
            print('-'*50)
            print(item)
        else:
            print(item)
    print('='*100)

def emptySlot(teacher):
    slots.append((teacher+" : BREAK"))

# Creates slots and excludes students from another appointment that time slot
def createSlot(teacher,student):
    slots.append((teacher+" : "+student))
    studentTeacher[student] = studentTeacher[student].replace(teacher + ',', '')
    temp.update(studentTeacher)
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

# SLOT HEADING - CREATES TIME FORMAT
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
def slotSorter(TotalSlots,teacherlist,Students,temp):
    for i in range(TotalSlots):
        clearExcluded()
        slotHeading(i,StartTime)
        for teacher in teacherlist:
            slotCreated = False
            for student in Students.keys():
                if teacher in Students[student]:
                    if not checkExcluded(student) and slotCreated == False:
                        createSlot(teacher,student)
                        slotCreated = True
                        Students[student] = 'BREAK'
                        break
                elif Students[student] == 'BREAK' and slotCreated == False:
                    Students[student] = temp[student]
            if slotCreated == False:
                emptySlot(teacher)
    outputSlots()

if __name__ == '__main__':
    menu()