import random

list1 = ['Bob','Jack','Will','Harry']
breaklist = []

def randomWithBreak(list):
    for i in range(500):
        selected = list[random.randrange(0,4)]
        if selected not in breaklist:
            print(selected)
            breaklist.clear()
            breaklist.append(selected)
        else:
            while selected in breaklist:
                selected = list[random.randrange(0, 4)]

randomWithBreak(list1)