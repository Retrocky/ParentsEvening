teachers = 'Mr.Jeff (1), Mr.Walter (3), Ms.Gary (1), Ms.Onion (2)'
finalTeacher = []
for teacher in teachers.split(','):
    finalTeacher.append(teacher.split('(')[0].strip())

print(finalTeacher)
