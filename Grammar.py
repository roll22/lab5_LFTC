from Production import Production


class Grammar:
    def __init__(self, filepath):
        self.__nonTerminals = []
        self.__terminals = []
        self.__productions = []
        self.__start = None
        self.__readFromFile(filepath)

    def getStartSymbol(self):
        return self.__start

    def getTerminals(self):
        return self.__terminals

    def getNonTerminals(self):
        return self.__nonTerminals

    def getProductions(self):
        return self.__productions

    def getProdForNT(self, nonTerm):
        return list(
            filter(
                lambda x: x.getLeftSide() == nonTerm, self.__productions)
        )

    def __readFromFile(self, filepath):
        with open(filepath, 'r') as file:
            self.__nonTerminals = file.readline().strip().split(' ')
            self.__terminals = file.readline().strip().split(' ')
            self.__start = file.readline().strip()
            for line in file:
                production = line.strip().split(' ')
                key = production[0].strip()
                values = list(production[2].strip().split('|'))
                for value in values:
                    self.__productions.append(
                        Production(key, list(value))
                    )
        file.close()
