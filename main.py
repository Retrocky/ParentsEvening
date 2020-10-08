import time
import pandas
import yagmail
from ParentsEvening import mail

# GUI
# Admin slot editing?

# Declaring variables
slots = []
excluded = []
breakList = []
higherBreakList = []
teacherList = []
staticTeachers = []
studentTeacher = {}
staticStudents = []
startTimes = {}
endTimes = {}
studentEmails = {}
teacherEmails = {}
optimality = 100
totalSlots = 0
breakNum = 0
appointmentNum = 0


# Main menu UI
def menu():
    print('+' * 100)
    print('')
    print('Parents Evening Scheduler')
    print('')
    print('1 - Run')
    print('2 - Configure')
    print('3 - Exit')
    print('')
    value = input('Enter choice : ')
    print('+' * 100)
    checkMenuValues(value)


# Checks / validates menu choices and redirects to correct function.
def checkMenuValues(value):
    try:
        value = int(value)
        if value == 1:
            getData('ParentsEvening.csv')
            slotSorter(teacherList, studentTeacher)
        elif value == 2:
            print('Custom run\n')
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
            print('Invalid choice - Please try again.\n'), menu()
    except ValueError:
        print('Enter a digit from 1 -> 3\n'), menu()


# Redirects custom run to main slot-sorter, changing the default values
def customRun(eveningStart, eveningEnd, appointmentLength):
    global slots
    slots = []
    slotSorter(teacherList, studentTeacher, eveningStart, eveningEnd, appointmentLength)


def getData(filename):
    data = pandas.read_csv(filename)
    teachers = str(data['Teachers'][0])
    for teacher in teachers.split(','):
        teacherList.append(teacher.split('(')[0].strip())
    global staticTeachers, staticStudents
    staticTeachers = teacherList.copy()
    for i in range(1, len(data.index)):
        item = data.loc[i]
        studentTeacher[item[0]] = item[1]
        startTimes[item[0]] = float(item[2])
        endTimes[item[0]] = float(item[3])
        studentEmails[item[0]] = item[4]
    staticStudents = list(studentTeacher.keys()).copy()
    for item in data.loc[0]:
        if item != 'x':
            temp = item.split(',')
            for email in temp:
                teacher = email.split('(')[0].strip()
                teacherEmails[teacher] = email.split('(')[1][:-1]


# Returns the priority weighting for a teacher by the respective student
def getPriority(student, studentTeacher, reqTeacher):
    teachers = str(studentTeacher[student]).split(',')
    for teacher in teachers:
        if reqTeacher in teacher:
            return int((teacher.split('('))[1][0])


# Outputs slots
def outputSlots():
    print('=' * 100)
    for item in slots:
        if 'Slot : ' in item:
            time.sleep(0.1)
            print("")
            print('-' * 50)
            print(item)
        elif item == 'End of evening':
            print('')
            print('End of evening')
            print('')
        else:
            print(item)
    print('=' * 100)


# Creates a break for the teacher if the slot is empty
def emptySlot(teacher):
    slots.append((f"{teacher} : BREAK"))
    global breakNum, optimality
    optimality *= 0.95
    breakNum += 1


# Creates slots and excludes students from another appointment that time slot
def createSlot(teacher, student):
    global appointmentNum
    appointmentNum += 1
    slots.append((f'{teacher} : {student}'))
    temp = studentTeacher[student].split(',')
    for teacherIter in temp:
        if teacher in teacherIter:
            temp.pop(temp.index(teacherIter))
    studentTeacher[student] = (',').join(temp)
    if studentTeacher[student] == '':
        studentTeacher.__delitem__(student)
    excludeStudent(student)
    breakList.append(student)
    global optimality
    optimality *= 1.05
    if optimality > 100:
        optimality = 100


# Excludes student from another appointment during the current slot
def excludeStudent(student):
    excluded.append(student)


# Checks if a student is excluded from this round
def checkExcluded(student):
    return True if student in excluded else False


# Clears the excluded students at the start of a new slot
def clearExcluded():
    excluded.clear()


def clearLowBreak():
    breakList.clear()


# Slot heading - Formats time in a user-friendly manner
def slotHeading(slot, startTime, appointmentLength):
    time = decimalTime(slot, startTime, appointmentLength)
    hours = int(time)
    minutes = (time * 60) % 60
    minutes = str(int(minutes.__round__()))
    if len(minutes) == 1:
        minutes = f'0{minutes}'
    time = f'{hours}:{minutes}'
    slots.append(f'Slot : {slot} Time : {time}')


def decimalTime(slot, startTime, appointmentLength):
    appointmentDivisible = appointmentLength / 60
    time = startTime + appointmentDivisible * slot
    return time


# Sorts students from highest priority to lowest priority
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
    return [i for i in reversed(sortedList)]


def endEvening():
    global studentTeacher, optimality, staticStudents
    slots.append('End of evening\n')
    print(f'Outstanding requests : \n{studentTeacher}')
    priorityImpact = 0
    for student in studentTeacher.keys():
        for teacher in studentTeacher[student].split(','):
            priorityImpact += getPriority(student, studentTeacher, teacher)
    percentageDecrease = (0.05 * len(studentTeacher) * priorityImpact)
    if percentageDecrease > 0.9:
        percentageDecrease = 0.9
    optimality *= 1 - percentageDecrease
    for teacher in staticTeachers:
        teacherSlots(teacher)
    for student in staticStudents:
        studentSlots(student)
    adminPortal()


# Loops through each slot with each teacher and matches students to their teachers needed
def slotSorter(teacherList, students, eveningStart=6, eveningEnd=9, appointmentLength=5):
    potentialEnd = {}
    for teacher in teacherList:
        potentialEnd[teacher] = 0
    totalSlots = int((eveningEnd - eveningStart) * (60 / appointmentLength))
    print(f'Total slots : {totalSlots}')
    for i in range(totalSlots):
        if len(teacherList) == 0:
            endEvening()
            break
        priorities = {}
        decTime = decimalTime(i, eveningStart, appointmentLength)
        clearExcluded()
        higherbreaklist = breakList.copy()
        clearLowBreak()
        slotHeading(i, eveningStart, appointmentLength)
        for teacher in teacherList:
            slotCreated = False
            for student in students.keys():
                if teacher in students[student]:
                    priorities[student] = getPriority(student, studentTeacher, teacher)
            studentPriorities = prioritySorter(priorities)
            for student in studentPriorities:
                # Optimal solution
                if not checkExcluded(student) and slotCreated == False and student not in higherbreaklist and \
                        startTimes[student] <= decTime < endTimes[student]:
                    createSlot(teacher, student)
                    slotCreated = True
                    potentialEnd[teacher] = 0
                    break
            # Comes here if constraints don't allow anyone or all appointments have been made
            if slotCreated == False:
                potentialEnd[teacher] += 1
                emptySlot(teacher)
                if potentialEnd[teacher] == 2:
                    remove = True
                    for student in list(studentTeacher.keys()):
                        if teacher in studentTeacher[student] and endTimes[student] > decTime:
                            remove = False
                    if remove == True:
                        teacherList.remove(teacher)
    endEvening()


def teacherSlots(teacher):
    temp = ''
    teacherSlots = {}
    for item in slots:
        if 'Slot : ' in item:
            temp = item
        elif teacher + ' : ' in item:
            teacherSlots[temp] = item
    emailTeacher(teacher, teacherSlots)


def studentSlots(student):
    temp = ''
    studentSlots = {}
    for item in slots:
        if 'Slot : ' in item:
            temp = item
        elif ' : ' + student in item:
            if item.split(':')[1].strip() == student:
                studentSlots[temp] = item
    emailStudent(student, studentSlots)


def emailTeacher(teacher, data):
    message = f'Hello {teacher}, here are your appointments :\n\n'
    for slot in data.keys():
        message += f'{slot}\n{data[slot]}\n\n'
    yagmail.SMTP(mail.email, mail.password).send(teacherEmails[teacher], 'Parents Evening Appointments', message)


def emailStudent(student, data):
    message = f'Hello {student}, here are your appointments : \n\n'
    for slot in data.keys():
        message += f'{slot}\n{data[slot]}\n\n'
    yagmail.SMTP(mail.email, mail.password).send(studentEmails[student], 'Parents Evening Appointments', message)


def adminPortal():
    print('OPTIMISATION SUCCESSFUL\n')
    adminMenu()


# Main menu UI
def adminMenu():
    print('\n' + '+' * 100)
    print('\nAdmin portal')
    print('\n1 - Output all appointments')
    print('2 - Send all appointments to an email address')
    print('3 - Configure & run again')
    print('4 - View analytics')
    print('5 - Exit\n')
    value = input('Enter choice : ')
    print('\n' + '+' * 100)
    checkAdminMenuValues(value)


def checkAdminMenuValues(value):
    try:
        value = int(value)
        if value == 1:
            outputSlots()
            time.sleep(1.5)
            adminMenu()
        elif value == 2:
            email = str(input('Enter email address : '))
            emailAdmin(email, slots)
            print('Email sent.')
            time.sleep(1)
            adminMenu()
        elif value == 3:
            print('Restarting...')
            time.sleep(0.25)
            checkMenuValues(2)
        elif value == 4:
            print('Calculating analytics')
            analyse()
        elif value == 5:
            print('Exiting program')
            time.sleep(0.5)
            exit()
        else:
            print('Invalid choice - Please try again.\n')
            adminMenu()
    except ValueError:
        print('Enter a digit from 1 -> 3\n')
        adminMenu()


def emailAdmin(email, data):
    message = 'Hello, here are all of the generated appointments : \n'
    for slot in data:
        message += f'\n{slot}\n' if 'Slot : ' in slot else f'{slot}\n'
    yagmail.SMTP(mail.email, mail.password).send(email, 'Parents Evening Appointments', message)


def analyse():
    time.sleep(1)
    global optimality, totalSlots, appointmentNum, breakNum
    print(f'\nOverall optimality : {int(optimality)}%')
    print(f'\nNumber of slots : {len(slots)}')
    print(f'\nNumber of appointments : {appointmentNum}')
    print(f'\nNumber of breaks : {breakNum}')
    print(f'\nNumber of appointments not fulfilled : {len(studentTeacher)}')
    adminMenu()


# Starts the program
if __name__ == '__main__':
    menu()
