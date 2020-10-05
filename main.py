import time
import pandas

# Priority weightings constraint

# Hardcoded variables
slots = []
excluded = []
breaklist = []
higherbreaklist = []
teacherlist = ['Mr.Walter','Mr.Jeff','Ms.Gary','Ms.Onion']
studentTeacher = {}
startTimes = {}
endTimes = {}

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
            getData('ParentsEvening.csv')
            slotSorter(teacherlist,studentTeacher)
        elif value == 2:
            print(' Custom run')
            print('')
            while True:
                eveningStart = input('Evening start time : ')
                try:
                    eveningStart = float(eveningStart)
                    break
                except ValueError:
                    print('Please enter a digit')
            while True:
                eveningEnd = input('Evening end time : ')
                try:
                    eveningEnd = float(eveningEnd)
                    break
                except ValueError:
                    print('Please enter a digit')
            while True:
                appointmentLength = input('Enter appointment length (In minutes) : ')
                try:
                    appointmentLength = int(appointmentLength)
                    break
                except ValueError:
                    print('Please enter an integer')
            while True:
                filename = input('CSV file path : ')
                try:
                    getData(filename)
                    break
                except FileNotFoundError:
                    print('File doesnt exist, please try again.')
            customRun(eveningStart, eveningEnd, appointmentLength)
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

# Redirects custom run to main slot-sorter, changing the default values
def customRun(eveningStart,eveningEnd,appointmentLength):
    slotSorter(teacherlist,studentTeacher,eveningStart,eveningEnd,appointmentLength)

def getData(filename):
    data = pandas.read_csv(filename)
    for i in range(len(data.index)):
        item = data.loc[i]
        studentTeacher[item[0]] = item[1]
        startTimes[item[0]] = item[2]
        endTimes[item[0]] = item[3]

def getPriority(student,studentTeacher,reqTeacher):
    teachers = str(studentTeacher[student]).split(',')
    for teacher in teachers:
        if reqTeacher in teacher:
            priority = (teacher.split('('))[1][0]
            return int(priority)

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
    breaklist.append(student)

# Checks if student hasn't already had an appointment with teacher
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

def clearLowBreak():
    breaklist.clear()

# Slot heading - Formats time in a user-friendly manner
def slotHeading(slot,startTime,appointmentLength):
    time = decimalTime(slot,startTime,appointmentLength)
    hours = int(time)
    minutes = (time * 60) % 60
    minutes = str(int(minutes.__round__()))
    if len(minutes) == 1:
        minutes = '0'+minutes
    time = str(hours)+':'+str(minutes)
    slots.append('Slot : '+str(slot)+' Time : '+str(time))

def decimalTime(slot,startTime,appointmentLength):
    appointmentDivisible = appointmentLength/60
    time = startTime+appointmentDivisible*slot
    return time

# Broken here
def prioritySorter(priorityDict):
    sortedList = []
    flipped = {}
    for key, value in priorityDict.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)
    for weight in range(1, 4):
        if weight in list(flipped.keys()):
            for i in range(len(flipped[weight])):
                sortedList.append(flipped[weight][i])
    new = []
    for i in reversed(sortedList):
        new.append(i)
    return new

# Loops through each slot with each teacher and matches students to their teachers needed
def slotSorter(teacherList, students, eveningStart=7, eveningEnd=8, appointmentLength=5):
    TotalSlots = int((eveningEnd - eveningStart) * 12)
    print('Total slots : '+str(TotalSlots))
    for i in range(TotalSlots):
        priorities = {}
        decTime = decimalTime(i,eveningStart,appointmentLength)
        clearExcluded()
        higherbreaklist = breaklist.copy()
        clearLowBreak()
        slotHeading(i,eveningStart,appointmentLength)
        for teacher in teacherList:
            slotCreated = False
            for student in students.keys():
                if teacher in students[student]:
                    priorities[student] = getPriority(student,studentTeacher,teacher)
            studentPriorities = prioritySorter(priorities)
            for student in studentPriorities:
                # Optimal solution
                if not checkExcluded(student) and slotCreated == False and checkSlot(teacher,student) and student not in higherbreaklist and startTimes[student] <= decTime and endTimes[student] > decTime:
                    createSlot(teacher, student)
                    slotCreated = True
                    break
            # Comes here if constraints don't allow anyone or all appointments have been made
            if slotCreated == False:
                emptySlot(teacher)
    outputSlots()

# Starts the program
if __name__ == '__main__':
    menu()