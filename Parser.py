from Grammar import Grammar


class Parser:
    def __init__(self, grammar):
        self._grammar = grammar
        self.firstSet = {i: set() for i in self._grammar.getNonTerminals()}
        self.followSet = {i: set() for i in self._grammar.getNonTerminals()}
        self.generateFirst()

    def Loop(self, initialSet, items, additionalSet):
        copySet = initialSet
        for i in range(len(items)):
            if items[i] in self._grammar.getNonTerminals():
                copySet = copySet.union(entry for entry in self.firstSet[items[i]] if entry != 'E')
                if 'E' in self.firstSet[items[i]]:
                    if i < len(items) - 1:
                        continue
                    copySet = copySet.union(additionalSet)
                    break
                else:
                    break
            else:
                copySet = copySet.union({items[i]})
                break
        return copySet

    def generateFirst(self):
        isSetChanged = True
        while isSetChanged:
            isSetChanged = False
            for production in self._grammar.getProductions():
                key = production.getLeftSide()
                value = production.getRightSide()
                v = list(value)
                copySet = self.firstSet[key]
                copySet = copySet.union(self.Loop(copySet, v, ['E']))

                if len(self.firstSet[key]) != len(copySet):
                    self.firstSet[key] = copySet
                    isSetChanged = True

g = Grammar("resources/grammars/g2.txt")
p = Parser(g)
