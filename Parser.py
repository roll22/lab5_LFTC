from Grammar import Grammar


class Parser:
    def __init__(self, grammar):
        self._grammar = grammar
        self.firstSet = {i: set() for i in self._grammar.getNonTerminals()}
        self.followSet = {i: set() for i in self._grammar.getNonTerminals()}
        self.Follow()
        print(self.followSet)

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

    def Follow(self):
        self.followSet[self._grammar.getStartSymbol()].add('$')
        isSetChanged = False
        for production in self._grammar.getProductions():
            key = production.getLeft()
            value = production.getRight()
            v = list(value)
            for i in range(len(v)):
                if v[i] not in self._grammar.getNonTerminals():
                    continue
                copySet = self.followSet[v[i]]
                if i < len(v) - 1:
                    copySet = copySet.union(self.Loop(copySet, v[i + 1:], self.followSet[key]))
                else:
                    copySet = copySet.union(self.followSet[key])
                if len(self.followSet[v[i]]) != len(copySet):
                    self.followSet[v[i]] = copySet
                    isSetChanged = True

        while isSetChanged:
            isSetChanged = False
            for production in self._grammar.getProductions():
                key = production.getLeft()
                value = production.getRight()
                v = list(value)
                for i in range(len(v)):
                    if v[i] not in self._grammar.getNonTerminals():
                        continue
                    copySet = self.followSet[v[i]]
                    if i < len(v) - 1:
                        copySet = copySet.union(self.Loop(copySet, v[i + 1:], self.followSet[key]))
                    else:
                        copySet = copySet.union(self.followSet[key])
                    if len(self.followSet[v[i]]) != len(copySet):
                        self.followSet[v[i]] = copySet
                        isSetChanged = True


g = Grammar("resources/grammars/g2.txt")
p = Parser(g)
