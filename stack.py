class Stack:
    """
    A stack object with the core functionality needed
    """
    def __init__(self):
        self.list = []
        self.pointer = -1

    def push(self, value):
        self.pointer += 1
        self.list.insert(self.pointer, value)

    def peek(self):
        return self.list[self.pointer]

    def checkEmpty(self):
        if self.pointer == -1:
            return True
        else:
            return False

    def pop(self):
        if self.checkEmpty():
            self.stackUnderflow()
        else:
            temp = self.list[self.pointer]
            self.pointer -= 1
            return temp

    def stackUnderflow(self):
        raise IndexError("Stack Underflow")



