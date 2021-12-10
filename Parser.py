from Grammar import Grammar


class Parser:
    def __init__(self, grammar):
        self._grammar = grammar
        self.firstSet = {i: set() for i in self._grammar.getNonTerminals()}
        self.followSet = {i: set() for i in self._grammar.getNonTerminals()}
        self._table = {}
        self.First()
        self.Follow()

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

    def First(self):
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

    def Follow(self):
        self.followSet[self._grammar.getStartSymbol()].add('E')
        isSetChanged = False
        for production in self._grammar.getProductions():
            key = production.getLeftSide()
            value = production.getRightSide()
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
                key = production.getLeftSide()
                value = production.getRightSide()
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

    def create_parsing_table(self):
        parsingTable = {}
        for nonTerminal in self._grammar.getNonTerminals():
            parsingTable[nonTerminal] = {}
            for terminal in self._grammar.getTerminals():
                parsingTable[nonTerminal][terminal] = 0
        print(parsingTable)

    def generateTable(self):
        nonterminals = self._grammar.getNonTerminals()
        terminals = self._grammar.getTerminals()
        for i in self._grammar.getProductions():
            key = i.getLeftSide()
            right = i.getRightSide()
            right_splitted = list(right)
            index = i.getIndex()
            rowSymbol = key
            for columnSymbol in terminals + ["E"]:
                pair = (rowSymbol, columnSymbol)
                if right_splitted[0] == columnSymbol and columnSymbol != "E":
                    self._table[pair] = (right, index)
                elif right_splitted[0] in nonterminals and columnSymbol in self.firstSet[right_splitted[0]]:
                    if pair not in self._table.keys():
                        self._table[pair] = (right, index)
                    else:
                        print(pair)
                        print("Grammar is not LL(1).")
                        return
                else:
                    if right_splitted[0] == "E":
                        for b in self.followSet[rowSymbol]:
                            if b == 'E':
                                b = '$'
                            self._table[(rowSymbol, b)] = (right, index)
                    else:
                        firsts = set()
                        for production in self._grammar.getProductions():
                            if production.getLeftSide() == rowSymbol:
                                if production.getRightSide() in nonterminals:
                                    firsts = firsts.union(self.firstSet[production.getRightSide()])
                                if 'E' in firsts:
                                    for b in self.followSet[rowSymbol]:
                                        if b == 'E':
                                            b = '$'
                                        if (rowSymbol, b) not in self._table.keys():
                                            self._table[(rowSymbol, b)] = (right, index)
        for t in terminals:
            self._table[(t, t)] = ('pop', -1)

        # rule 3
        self._table[('$', '$')] = ('acc', -1)

    def evaluateSequence(self, sequence):
        w = list(sequence)
        stack = [self._grammar.getStartSymbol(), '$']
        output = ""
        while stack[0] != '$' and w:
            print(w, stack)
            # pop operation
            if w[0] == stack[0]:
                w = w[1:]
                stack.pop(0)
            else:
                x = w[0]
                a = stack[0]
                # error operation
                if (a, x) not in self._table.keys():
                    return None
                # push operation
                else:
                    stack.pop(0)
                    rhs, index = self._table[(a, x)]
                    rhs = list(rhs)
                    for i in range(len(rhs) - 1, -1, -1):
                        if rhs[i] != 'E':
                            stack.insert(0, rhs[i])
                    output += str(index) + " "
            print(output)
        # error operation
        if stack[0] == '$' and w:
            return None
        # push or accept operation
        elif not w:
            while stack[0] != '$':
                a = stack[0]
                if (a, '$') in self._table.keys():
                    output += str(self._table[(a, '$')][1]) + " "
                stack.pop(0)
            return output


g = Grammar("resources/grammars/g2.txt")
p = Parser(g)
p.generateTable()
for key in p._table:
    print(f'{key} -> {p._table[key]}')
# print(p._table)
print('==================================')
print('==================================')
print(p.evaluateSequence('+*i'))
