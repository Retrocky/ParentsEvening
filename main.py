# Importing required packages

import os  # Used to access the current directory
import time  # Used to delay the program at points - making it much more smooth
import tkinter.filedialog as fd  # Used to browse files
from tkinter import *  # Used to hide the default tkinter dialog box when choosing a file

import pandas  # Used to read and help format the user's csv file
import pandas.errors  # Used to capture errors when parsing the user-inputted csv file
import yagmail  # Used to email end-users with appointments

from ParentsEvening import mail  # A separate file containing passwords for the email to make it more secure

# Declaring variables

slots = []
# Main list where all appointments created will be added to

excluded = []
# The list of students excluded from the rest of the time slot as they have already had an appointment

breakList = []
# The lower break list students who have just had a new appointment are added to this, at the start
# of a new time slot this is cleared

teacherList = []
# List of all the teachers participating in the evening, teachers are removed when they have no
# more appointment requests

staticTeachers = []
# A copy of teacherList that is static so it can be used at the end of the evening

studentTeacher = {}
# The main dictionary containing all students as keys and their requested teachers and priorities
# as values

staticStudents = []
# A static copy of the list of students, used to send emails post-optimisation

startTimes = {}
# A dictionary with students being keys and their respective start times being values

endTimes = {}
# A dictionary with students being keys and their respective end times being values

studentEmails = {}
# A dictionary with students being keys and their respective emails being values

teacherEmails = {}
# A dictionary with teachers being keys and their respective emails being values

fileName = ''
# A global instantiation of the csv filename so local functions can access it

optimality = 100
# The optimality percentage of the program, starts at 100%, -2% for a break, +5% for an appointment
# and -the sum of the priorities of the outstanding requests * the number of outstanding requests at the end of the
# evening

totalSlots = 0
# The number of maximum total time slots there will be according to the admin constraints

breakNum = 0
# The number of breaks allocated throughout the evening - seen as not optimal, incremented in the emptySlot function

appointmentNum = 0


# The number of successful appointments allocated, incremented in the createSlot function


# User-friendly UI functionality


def continueReq():
    """Slows down the pace of the program to make it more user friendly"""
    shortSleep()
    input('Press enter to continue...')


def shortSleep():
    """Calls the time library function - sleep, for 0.5s to slow down the pace of the program"""
    time.sleep(0.5)


def error(message):
    """Outputs a formatted error message"""
    block = '+' * (len(message) + 16)
    print(f'\n{block}\nERROR - {message} - ERROR\n{block}\n')
    continueReq()


# Part 1 - Pre-Optimisation functionality


def menu():
    """Main menu UI & choices"""
    print('\nParents Evening Scheduler\n')
    shortSleep()
    print('\n1 - Configure')
    print('2 - Exit\n')
    value = input('Enter choice : ')
    checkMenuValues(value)


def checkMenuValues(value):
    """Checks/validates menu choices and redirects user to the correct function"""
    global fileName
    try:
        value = int(value)
    except ValueError:
        error('Enter a digit from 1 -> 3')
        menu()
    if value == 1:
        print('Please open CSV file to import data.\n')
        continueReq()
        root = Tk()
        root.geometry('1x1')
        fileName = getFile()
        root.destroy()
        getData(fileName)
        while True:
            eveningStart = input('Evening start time (24hr HH:MM) : ')
            try:
                if checkTime(eveningStart):
                    eveningStart = decimalTimeFromString(eveningStart)
                    break
                else:
                    error('Please enter the time (24hr HH:MM) e.g - 21:15')
            except ValueError:
                error('Please enter the time (24hr HH:MM) e.g - 21:15')
        while True:
            eveningEnd = input('Evening end time (24hr HH:MM) : ')
            try:
                if checkTime(eveningEnd):
                    eveningEnd = decimalTimeFromString(eveningEnd)
                    if eveningEnd > eveningStart:
                        break
                    else:
                        error('The end of the evening must be later than the start of the evening.')
                else:
                    error('Please enter the time (24hr HH:MM) e.g - 21:15')
            except ValueError:
                error('Please enter the time (24hr HH:MM) e.g - 21:15')
        while True:
            appointmentLength = input('Enter appointment length (In minutes) : ')
            try:
                appointmentLength = int(appointmentLength)
                if 30 > appointmentLength > 0:
                    break
                else:
                    error(f'{appointmentLength} must be less than 30 minutes and greater than 0 minutes')
            except ValueError:
                error('Please enter an integer.')
        customRun(eveningStart, eveningEnd, appointmentLength)
    elif value == 2:
        exit()
    else:
        error('Invalid choice - Please try again.')
        menu()


def getFile():
    """Opens up the system file browser UI and returns the filename"""
    return fd.askopenfilename(initialdir=os.getcwd(), title="Select CSV to import",
                              filetypes=(('CSV files', '*.csv'), ('all files', '*.*')))


def getData(filename):
    """Retrieves and formats data from csv file using a pandas dataFrame"""
    global teacherList, staticTeachers, staticStudents
    try:
        data = pandas.read_csv(filename)
        teachers = str(data['Teachers'][0])
        for teacher in teachers.split(','):
            teacherList.append(teacher.split('(')[0].strip())
        staticTeachers = teacherList.copy()
        for i in range(1, len(data.index)):
            item = data.loc[i]
            studentTeacher[item[0]] = item[1]
            startTimes[item[0]] = decimalTimeFromString(item[2])
            endTimes[item[0]] = decimalTimeFromString(item[3])
            studentEmails[item[0]] = item[4]
        staticStudents = list(studentTeacher.keys()).copy()
        for item in data.loc[0]:
            if item != 'x':
                temp = item.split(',')
                for email in temp:
                    teacher = email.split('(')[0].strip()
                    teacherEmails[teacher] = email.split('(')[1][:-1]
    except:
        # Bare except needed as csv could be formatted incorrectly in countless permutations
        error('CSV not formatted correctly.')
        menu()


def checkTime(reqTime):
    """Checks time is in the correct format - HH:MM"""
    temp = reqTime.split(':')
    try:
        if len(temp[0]) == 2 and len(temp[1]) == 2:
            if int(temp[0][0]) == 1 or int(temp[0][0]) == 0:
                int(temp[0][1])
                if 0 <= int(temp[1][0]) <= 5:
                    int(temp[1][1])
                    return True
            elif int(temp[0][0]) == 2:
                if int(temp[0][1]) < 4 and 0 <= int(temp[1][0]) <= 5:
                    int(temp[1][1])
                    return True
        return False
    except ValueError:
        return False


def decimalTimeFromString(string):
    """Converts time in format HH:MM to decimal form so it can be used in mathematical calculations"""
    (h, m) = string.split(':')
    return float(int(h) + int(m) / 60)


def customRun(eveningStart, eveningEnd, appointmentLength):
    """Redirects custom run to main slot-sorter, changing the default values"""
    global slots, teacherList
    slots = []
    slotSorter(teacherList, studentTeacher, eveningStart, eveningEnd, appointmentLength)


# Part 2 - Optimisation functionality


def slotSorter(teachers, students, eveningStart, eveningEnd, appointmentLength):
    """Loops through each slot with each teacher and matches students to their teachers needed"""
    global totalSlots
    totalSlots = int((eveningEnd - eveningStart) * (60 / appointmentLength))
    for i in range(1, totalSlots + 1):
        # Looping through each slot, bounds incremented to eliminate the 0-based index in python
        decTime = decimalTime(i, eveningStart, appointmentLength)
        clearExcluded()
        higherBreakList = breakList.copy()
        clearLowBreak()
        slotHeading(i, eveningStart, appointmentLength)
        for teacher in teachers:
            # Loops through each teacher and sorts students from highest to lowest priority for the respective teacher
            priorities = {}
            slotCreated = False
            for student in students.keys():
                if teacher in students[student]:
                    priorities[student] = getPriority(student, studentTeacher, teacher)
            studentPriorities = prioritySorter(priorities)
            for student in studentPriorities:
                if not checkExcluded(student) and slotCreated is False and student not in higherBreakList and \
                        startTimes[student] <= decTime < endTimes[student]:
                    # The optimal solution, following all user-defined constraints and an appointment break
                    createSlot(teacher, student)
                    slotCreated = True
                    break
            if not slotCreated:
                # If constraints don't allow anyone or all appointments have been made
                remove = True
                for student in list(studentTeacher.keys()):
                    # Checks if any student present at the time is requesting an appointment with the teacher
                    if teacher in studentTeacher[student] and endTimes[student] > decTime:
                        remove = False
                        emptySlot(teacher)
                if remove:
                    teachers.remove(teacher)
                    if len(teachers) == 0:
                        # If no teachers needed left the evening will end
                        endEvening()
                        break
    endEvening()


# Returns the decimal time of a specified slot
def decimalTime(slot, startTime, appointmentLength):
    appointmentDivisible = appointmentLength / 60
    decTime = startTime + appointmentDivisible * (slot - 1)
    return decTime


# Clears the excluded students at the start of a new slot
def clearExcluded():
    excluded.clear()


# Clears the lower level break-list so new students can be added
def clearLowBreak():
    breakList.clear()


# Formats time in a user-friendly manner, converting decimal to hours & minutes
def slotHeading(slot, startTime, appointmentLength):
    strTime = decimalTime(slot, startTime, appointmentLength)
    hours = int(strTime)
    minutes = (strTime * 60) % 60
    minutes = str(int(minutes.__round__()))
    if len(minutes) == 1:
        minutes = f'0{minutes}'
    strTime = f'{hours}:{minutes}'
    slots.append(f'Slot : {slot} Time : {strTime}')


# Returns the priority weighting for a teacher by the respective student
def getPriority(student, students, reqTeacher):
    teachers = str(students[student]).split(',')
    for teacher in teachers:
        if reqTeacher in teacher:
            return int((teacher.split('('))[1][0])


# Sorts students from highest priority to lowest priority given a certain teacher
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


# Checks if a student is excluded from this round
def checkExcluded(student):
    return True if student in excluded else False


# Creates slots and excludes students from another appointment that time slot, optimality increases by 5%
def createSlot(teacher, student):
    global appointmentNum, optimality
    appointmentNum += 1
    slots.append(f'{teacher} : {student}')
    temp = studentTeacher[student].split(',')
    for teacherIter in temp:
        if teacher in teacherIter:
            temp.pop(temp.index(teacherIter))
    studentTeacher[student] = ','.join(temp)
    if studentTeacher[student] == '':
        studentTeacher.__delitem__(student)
    excludeStudent(student)
    breakList.append(student)
    optimality *= 1.05
    if optimality > 100:
        optimality = 100


# Excludes student from another appointment during the current slot
def excludeStudent(student):
    excluded.append(student)


# Creates a break for the teacher if the slot is empty
def emptySlot(teacher):
    slots.append(f"{teacher} : BREAK")
    global breakNum, optimality
    optimality *= 0.98
    breakNum += 1


# Part 3 - Post optimisation functionality


# Initiates the end of the evening, calculates optimality and requests to email students & teachers
def endEvening():
    global studentTeacher, optimality, staticStudents
    slots.append('End of evening\n')
    print(f'Outstanding requests : {studentTeacher}')
    if len(studentTeacher) > 3:
        print(f'{len(studentTeacher)} appointments unfulfilled, perhaps try changing the evening start & end times or '
              f'change the appointment length')
    priorityImpact = 0
    for student in studentTeacher.keys():
        for teacher in studentTeacher[student].split(','):
            priorityImpact += getPriority(student, studentTeacher, teacher)
    percentageDecrease = (0.05 * len(studentTeacher) * priorityImpact)
    if percentageDecrease > 0.9:
        percentageDecrease = 0.9
    optimality *= 1 - percentageDecrease
    adminMenu()


# Outputs slots in a user-friendly manner
def outputSlots():
    print('=' * 100)
    for item in slots:
        if 'Slot : ' in item:
            time.sleep(0.1)
            print('-' * 50)
            print(item)
        elif item == 'End of evening':
            print('\nEnd of evening\n')
        else:
            print(item)
    print('=' * 100)


# Returns a dictionary of a certain teacher's slots
def teacherSlots(teacher):
    temp = ''
    teacherAppointments = {}
    for item in slots:
        if 'Slot : ' in item:
            temp = item
        elif teacher + ' : ' in item:
            teacherAppointments[temp] = item
    emailTeacher(teacher, teacherAppointments)


# Returns a dictionary of a certain student's slots
def studentSlots(student):
    temp = ''
    studentAppointments = {}
    for item in slots:
        if 'Slot : ' in item:
            temp = item
        elif ' : ' + student in item:
            if item.split(':')[1].strip() == student:
                studentAppointments[temp] = item
    emailStudent(student, studentAppointments)


# Using the Yagmail library - teachers are emailed in a user-friendly manner all of their slots
def emailTeacher(teacher, data):
    message = f'Hello {teacher}, here are your appointments :\n\n'
    for slot in data.keys():
        message += f'{slot}\n{data[slot]}\n\n'
    yagmail.SMTP(mail.email, mail.password).send(teacherEmails[teacher], 'Parents Evening Appointments', message)


# Using the Yagmail library - students are emailed in a user-friendly manner all of their slots
def emailStudent(student, data):
    message = f'Hello {student}, here are your appointments : \n\n'
    for slot in data.keys():
        message += f'{slot}\n{data[slot]}\n\n'
    yagmail.SMTP(mail.email, mail.password).send(studentEmails[student], 'Parents Evening Appointments', message)


# Takes the admin to stage 2 of the program, the post optimisation menu
def adminPortal():
    adminMenu()


# Admin menu UI
def adminMenu():
    print('+' * 100)
    print('\nAdmin portal')
    print('\n1 - Output all appointments')
    print('2 - Send all appointments to an email address')
    print('3 - Edit appointments')
    print('4 - Configure & run again')
    print('5 - View analytics\n')
    print('6 - Email teachers & students\n')
    print('7 - Exit\n')
    value = input('Enter choice : ')
    print('\n' + '+' * 100)
    checkAdminMenuValues(value)


# Checks / validates menu choices and redirects to correct function.
def checkAdminMenuValues(value):
    global staticTeachers, staticStudents
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
            edit()
        elif value == 4:
            print('Restarting...')
            time.sleep(0.25)
            checkMenuValues(1)
        elif value == 5:
            print('Calculating analytics')
            analyse()
        elif value == 6:
            print('Emailing teachers')
            for teacher in staticTeachers:
                teacherSlots(teacher)
            print('Emailing students')
            for student in staticStudents:
                studentSlots(student)
            adminMenu()
        elif value == 7:
            print('Exiting program')
            time.sleep(0.5)
            exit()
        else:
            error('Invalid choice - Please try again.')
            adminMenu()
    except ValueError:
        error('Enter a digit from 1 -> 3')
        adminMenu()


# Emails an admin with all of the generated slots
def emailAdmin(email, data):
    message = 'Hello, here are all of the generated appointments : \n'
    for slot in data:
        message += f'\n{slot}\n' if 'Slot : ' in slot else f'{slot}\n'
    yagmail.SMTP(mail.email, mail.password).send(email, 'Parents Evening Appointments', message)


def edit():
    global slots, totalSlots
    potentialEdits = []
    print('Editing\n')
    outputSlots()
    while True:
        reqSlot = input('\nWhich slot would you like to change? (Enter slot number) : ')
        try:
            reqSlot = int(reqSlot)
            if reqSlot > 0 and reqSlot >= totalSlots:
                break
        except ValueError:
            error(f'Please enter a number in the range of 0 -> {totalSlots}')
            pass
    for item in slots:
        if f'Slot : {reqSlot}' in item:
            for i in range(len(staticTeachers) + 1):
                print(f'\n{slots[slots.index(item) + i]}')
                potentialEdits.append(slots[slots.index(item) + i])
    while True:
        reqTeacher = str(input('\nWhich appointment would you like to change? (Enter teacher name) : '))
        if reqTeacher in staticTeachers:
            break
        else:
            error(f'Please enter one of these teachers : {staticTeachers}')
            pass
    for appointment in potentialEdits:
        if f'{reqTeacher} : ' in appointment:
            confirmedEdit = str(appointment)
            print(f'\nChanging : {appointment}\n')
            currentStudent = appointment.split(':')[1].strip()
            reqStudent = input(f'Enter the student you would like to add instead of the {currentStudent} : ')
            print(f'New slot : {reqTeacher} : {reqStudent}')
            confirmedEdit = confirmedEdit.replace(currentStudent, reqStudent)
            for item in slots:
                if item == f'{reqTeacher} : {currentStudent}':
                    slots[slots.index(item)] = confirmedEdit
            print('Successfully updated')
            continueReq()
            outputSlots()
    adminMenu()


# Outputs the optimisation analytics in a user-friendly format
def analyse():
    time.sleep(1)
    global optimality, totalSlots, appointmentNum, breakNum
    print(f'\nOverall optimality : {int(optimality)}%'
          f'\nNumber of successful appointments : {appointmentNum}\nNumber of breaks : {breakNum}'
          f'\nNumber of appointments not fulfilled : {len(studentTeacher)}')
    continueReq()
    adminMenu()


# Starts the program
if __name__ == '__main__':
    menu()
