from Grammar import Grammar

if __name__ == '__main__':
    g = Grammar("resources/grammars/g1.txt")
    print("Start: " + str(g.getStartSymbol()))
    print("Terminals: " + str(g.getTerminals()))
    print("nonTerminals: " + str(g.getNonTerminals()))
    print('Productons : ')
    for prod in g.getProductions():
        print(prod)

    print("Prod for nonterm: ")
    for prod in g.getProdForNT('S'):
        print(prod)
