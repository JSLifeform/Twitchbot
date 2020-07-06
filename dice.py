#threes dice game dice module

#import random for dice rolling
import random

#initialize generic die
class Die:
    def __init__(self, sides = 6, value = 0, score = 0, locked = False):
        if not sides >= 2:
            raise ValueError("Must have at least 2 sides to randomize die!")
        if not isinstance(sides, int):
            raise ValueError("The number of sides of a die must be an integer, silly goose!")
        self.value = value or random.randint(1, sides)
        self.locked = locked
        if self.value == 3:
            self.score = 0
        else:
            self.score = self.value

    def __int__(self):
        return self.value

    def __eq__(self, other):
        return int(self) == other

    def __ne__(self, other):
        return int(self) != other

    def __gt__(self, other):
        return int(self) > other    

    def __lt__(self, other):
        return int(self) < other

    def __ge__(self, other):
        return int(self) >= other    

    def __le__(self, other):
        return int(self) <= other    

    def __cmp__(self, other):
        if self.value == 3:
            return -1

    # def __repr__(self):
    #     return str(self.value)

#initialize d6 class
class D6(Die):
    def __init__(self, value = 0, locked = False):
        super().__init__(sides = 6,  value = value, locked = False)

#initialize d4 class
class D4(Die):
    def __init__(self, value = 0):
        super().__init__(sides = 4, value = value)

#initialize d20 class
class D20(Die):
    def __init__(self, value = 0):
        super().__init__(sides = 20, value = value)