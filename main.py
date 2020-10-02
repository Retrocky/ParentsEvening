import time
# TO DO LIST
# Student timings constraint
# CSV input - Extension google form -> CSV -> Python - DOING
# Priority weightings constraint
# Add breaks - FIXING

# Hardcoded variables
slots = []
excluded = []
teacherlist = ['Mr.Walter','Mr.Jeff','Ms.Gary','Ms.Onion']
studentTeacher = {'Will':'Mr.Walter,Ms.Gary,Mr.Jeff,Ms.Onion','Bob':'Mr.Jeff,Ms.Onion,Mr.Walter',
                      'Gee':'Mr.Walter,Mr.Jeff,Ms.Onion,Ms.Gary','Jack':'Mr.Jeff,Ms.Onion,Mr.Walter',
                      'Harry':'Ms.Onion,Ms.Gary','Alice':'Ms.Gary,Ms.Gary','Emily':'Mr.Walter,Mr.Jeff,Ms.Onion,Ms.Gary',
                      'Ben':'Mr.Walter,Mr.Jeff,Ms.Onion,Ms.Gary','Bug':'monkey','AnotherBug':'28828199282991',}

# Main menu UI
def menu():
    print('+'*100)
    print('')
    print('Parents Evening Scheduler')
    print('')
    print('1 - Run algorithm with default settings')
    print('2 - Custom run')
    print('3 - Exit')
    print('')
    value = input('Enter choice : ')
    print('+'*100)
    checkMenuValues(value)

# Checks / validates menu choices and redirects to correct function.
def checkMenuValues(value):
    try:
        value = int(value)
        if value == 1:
            slotSorter(teacherlist,studentTeacher)
        elif value == 2:
            print('')
            print(' Custom run')
            print('')
            eveningStart = input('Enter evening start time : ')
            eveningEnd = input('Enter evening end time : ')
            appointmentLength = input('Enter appointment length (In minutes) : ')
            try:
                eveningStart = int(eveningStart)
                try:
                    eveningEnd = int(eveningEnd)
                    try:
                        appointmentLength = int(appointmentLength)
                        customRun(eveningStart,eveningEnd,appointmentLength)
                    except ValueError:
                        print('Enter a digit : ')
                        print('')
                        checkMenuValues(value)
                except ValueError:
                    print('Enter a digit : ')
                    print('')
                    checkMenuValues(value)
            except ValueError:
                print('Enter a digit : ')
                print('')
                checkMenuValues(value)
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

def customRun(eveningStart,eveningEnd,appointmentLength):
    slotSorter(teacherlist,studentTeacher,eveningStart,eveningEnd,appointmentLength)

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

# Creates a break for the teacher if the slot is empty
def emptySlot(teacher):
    slots.append((teacher+" : BREAK"))

# Creates slots and excludes students from another appointment that time slot
def createSlot(teacher,student):
    slots.append((teacher+" : "+student))
    studentTeacher[student] = studentTeacher[student].replace(teacher + ',', '')
    excludeStudent(student)

def checkSlot(teacher,student):
    if len(slots) == 0:
        return True
    else:
        for appointment in slots:
            if (teacher+" : "+student) == appointment:
                return False
        return True

# Excludes student from another appointment during the current slot
def excludeStudent(student):
    excluded.append(student)

# Checks if a student is excluded from this round
def checkExcluded(student):
    if student in excluded:
        return True
    else:
        return False

# Clears the excluded students at the start of a new slot
def clearExcluded():
    excluded.clear()

# Slot heading - Formats time in a user-friendly manner
def slotHeading(slot,StartTime,appointmentLength):
    appointmentDivisible = appointmentLength/60
    time = StartTime+appointmentDivisible*slot
    hours = int(time)
    minutes = (time * 60) % 60
    minutes = str(int(minutes.__round__()))
    if len(minutes) == 1:
        minutes = '0'+minutes
    time = str(hours)+':'+str(minutes)
    slots.append('Slot : '+str(slot)+' Time : '+str(time))

# Loops through each slot with each teacher and matches students to their teachers needed
def slotSorter(teacherList, students, eveningStart=7, eveningEnd=8, appointmentLength=5):
    TotalSlots = int((eveningEnd - eveningStart) * 12)
    print('Number of slots : ' + str(TotalSlots))
    for i in range(TotalSlots):
        print('---')
        print(students)
        clearExcluded()
        slotHeading(i,eveningStart,appointmentLength)
        for teacher in teacherList:
            slotCreated = False
            for student in students.keys():
                if teacher in students[student]:
                    if not checkExcluded(student) and slotCreated == False and checkSlot(teacher,student):
                        createSlot(teacher,student)
                        slotCreated = True
                        break
            if slotCreated == False:
                emptySlot(teacher)
    outputSlots()

# Starts the program
if __name__ == '__main__':
    menu()