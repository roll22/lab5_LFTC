class Production:
    def __init__(self, left_side, right_side, index):
        self.__leftSide = left_side
        self.__rightSide = right_side
        self.__index = index

    def getIndex(self):
        return self.__index

    def getLeftSide(self):
        return self.__leftSide

    def getRightSide(self):
        return self.__rightSide

    def __str__(self):
        right_str = "["
        for i in range(len(self.getRightSide())):
            if i != len(self.getRightSide()) - 1:
                right_str += self.getRightSide()[i] + ", "
            else:
                right_str += self.getRightSide()[i]
        right_str += "]"
        return self.__leftSide + " -> " + right_str + ", " + str(self.__index)

    def __eq__(self, other):
        return self.__rightSide == other.getRightSide() and self.__leftSide == other.getLeftSide()
