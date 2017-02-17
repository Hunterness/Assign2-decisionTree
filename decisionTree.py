import regex as re
from collections import OrderedDict
from math import log2

"""Reader. reads in ARFF-file"""
def reader(filename):
    attributes = {}
    data = {}
    file = open(filename)
    input = file.read().lower()
    inputLines = re.finditer('(.*\n)', input)
    counterAttr = 0
    counterData = 0
    for line in inputLines:
        word = line.group().replace('\n', '')
        pos = word.find('%')
        if(pos != -1):
            word = word[0:pos]
        if(word != '' and not re.match('@relation.*', word)
        and not re.match('@data.*', word)):
            if(re.match('@attribute .*', word)):
                pos = word.find(' {')
                if(pos != -1):
                    attr = word[11:pos]
                    types = word[pos+2:len(word)-1]+","
                pos = types.find(',')
                attributes[counterAttr] = [attr]
                while(pos != -1):
                    attributes[counterAttr].append(types[0:pos])
                    types = types[pos+1:len(types)]
                    pos = types.find(',')
                counterAttr = counterAttr+1
            else:
                word = word+","

                for i in range(0,len(attributes.keys())):
                    pos = word.find(',')
                    if(pos != -1):
                        a = word[0:pos]
                        try:
                            data[counterData].append((attributes[i][0],a))
                        except:
                            data[counterData] = [(attributes[i][0],a)]
                    word = word[pos+1:len(word)]
                counterData = counterData+1

    attributesNew = OrderedDict()
    for attr in attributes:
        try:
            attributesNew[attributes[attr][0]].append(attributes[attr][1:len(attributes)])
        except:
            attributesNew[attributes[attr][0]] = [attr]+ attributes[attr][1:len(attributes)]
    i = len(data)
    dataNew = []
    for j in range(i):
        dataNew.append(data[j])
    return attributesNew,dataNew

"""Algorithm for Decision Tree"""
treePrint = []

def same_class(examples,types):
    nbr = []
    for k in range(len(types)):
        nbr.append(0)
    for e in examples:
        for k in range(len(types)):
            if e[-1][1] == types[k]:
                nbr[k] = nbr[k] + 1
    for k in range(len(types)):
        if nbr[k] == len(examples):
            return True
    return False

def nbrPerVal(examples, attributes, attr, val,types):
    nbr = []
    for k in range(len(types)):
        nbr.append(0)
    indexAttr = attributes[attr][0]
    for e in examples:
        if e[indexAttr][1] == val:
            for k in range(len(types)):
                if e[-1][1] == types[k]:
                    nbr[k] = nbr[k] + 1
    return nbr

def nbrTotal(examples, attributes, attr,types):
    nbr = []
    for k in range(len(types)):
        nbr.append(0)
    indexAttr = attributes[attr][0]
    for e in examples:
        for k in range(len(types)):
            if e[-1][1] == types[k]:
                nbr[k] = nbr[k] + 1
    return nbr
"""
def B(q,types):
    if q == 0 or q == 1:
        return 0
    return -(q*log2(q)+(1-q)*log2(1-q))
"""
def H(nbrTypes, sum):
    if sum == 0:
        return 0
    res = 0
    for t in nbrTypes:
        if t != 0:
            res = res - (t/sum)*log2(t/sum)
    return res

def importance(attributes,examples,types):
    max_attr = ''
    max_gain = 0
    for a in attributes:
        if a != 'willwait':
            remainder = 0
            listOfNbrOfTotal = nbrTotal(examples,attributes,a,types)
            sumT = 0
            for k in range(len(types)):
                sumT = sumT + listOfNbrOfTotal[k]
            h = H(listOfNbrOfTotal,sumT)
            for v in attributes[a][1:len(attributes[a])]:
                listOfNbrOfVal = nbrPerVal(examples,attributes,a,v,types)
                sumV = 0
                for k in range(len(types)):
                    sumV = sumV + listOfNbrOfVal[k]

                remainder = remainder + (sumV/sumT)*H(listOfNbrOfVal,sumV)
            gain = h - remainder
            if gain > max_gain:
                max_attr = a
                max_gain = gain
    return max_attr

    """
    max_attr = ''
    max_gain = 0
    for a in attributes:
        if a != 'willwait':
            remainder = 0
            nbrT = nbrTotal(examples,attributes,a,types)
            pT = nbrT[0]
            nT = nbrT[1]
            sumT = 0
            for k in range(len(types)):
                sumT = sumT + nbrT[k]
            for v in attributes[a][1:len(attributes[a])]:
                nbrV = nbrPerVal(examples,attributes,a,v,types)
                #print(a,v,(pV+nV),(pT+nT))
                pV = nbrV[0]
                nV = nbrV[1]
                sumV = 0
                for k in range(len(types)):
                    sumV = sumV + nbrV[k]
                if sumV != 0:
                    q = pV/sumV
                    remainder = remainder + B(q,types)*sumV/sumT

            gain = B(pT/sumT,types)-remainder
            if gain > max_gain:
                max_attr = a
                max_gain = gain

    return max_attr
"""

def plurality_value(examples,types):
    nbr = []
    for k in range(len(types)):
        nbr.append(0)
    for e in examples:
        for k in range(len(types)):
            if e[-1][1] == types[k]:
                nbr[k] = nbr[k] + 1
    ans = types[0]
    max = 0
    for k in range(len(types)):
        if nbr[k] > max:
            ans = types[k]
            max = nbr[k]
    return ans
    """if nbrYes == nbrNo:
        return examples[0][-1][1]
    elif nbrYes > nbrNo:
        return 'yes'
    else:
        return 'no'
    """


def decision_tree_algorithm(examples, attributes,parent_examples,turn):
    """if examples.empty
			return plurality_value(parent_examples)
		else if all examples have samma classification
			return
		else if attributes.empty
			return plurality_value(examples)
		else
			A = importance
			tree = new decision tree with root A
			for each v_k of A
				exs = [e of examples ^ e.A = v_k]
				subtree = decision_tree_algorithm(exs, attributes-A,examples)
				add branch to tree with label (A=v_k) and subtree "subtree"
		return tree"""
    types = attributes['willwait'][1:len(attributes['willwait'])]
    if not examples:
        #no more data
        #print("no data")
        treePrint.append((": " + plurality_value(parent_examples,types),0,True))
        #return ": " + plurality_value(parent_examples,types) + "\n", True
    elif same_class(examples,types):
        #print("same class")
        #alla kvarvarande exempel har samma resultat
        treePrint.append((": " + examples[0][-1][1],0,True))
        #return ": " + examples[0][-1][1] + "\n", True #returnerar yes/no
    elif not attributes:
        #no more attributes
        #print("no attr")
        treePrint.append((": " + plurality_value(examples,types),0,True))
        #return ": " + plurality_value(examples,types) + "\n", True
    else:
        a = importance(attributes, examples,types)
        #tree = ""
        i = attributes[a][0]
        values = attributes[a][1:len(attributes[a])]
        del attributes[a]
        for v in values:
            #tree = tree + a + " = " + v
            treePrint.append((a + " = " + v,turn,False))
            exs = []
            for j in range(len(examples)):
                res = examples[j][i][1]
                if res == v:
                    exs.append(examples[j])
            #subtree, end =
            decision_tree_algorithm(exs,attributes,examples,turn+1)
            """if end:
                tree = tree + subtree
            else:
                tree = tree + "\n"
                for k in range(turn+1):
                    tree = tree + "\t"
                tree = tree + subtree
                for k in range(turn+1):
                    tree = tree + "\t"""

        #return tree, False





if __name__ == '__main__':
    filename = 'input_2res.arff'
    attributes, data = reader(filename)
    #tree, end =
    decision_tree_algorithm(data, attributes, data,0)
    print("Restaurant 2:")
    #print(tree)
    printout = ""
    for i in range(len(treePrint)-1):
        if not treePrint[i][2] and treePrint[i+1][2]:
            for k in range(treePrint[i][1]):
                printout = printout + "\t"
            printout = printout + treePrint[i][0]

        else:
            for k in range(treePrint[i][1]):
                printout = printout + "\t"
            printout = printout + treePrint[i][0] + "\n"

    print(printout)
    treePrint = []


    filename = 'input_3res.arff'
    attributes, data = reader(filename)
    #tree, end =
    decision_tree_algorithm(data, attributes, data,0)
    print("\nRestaurant 3:")
    printout = ""
    for i in range(len(treePrint)-1):
        if not treePrint[i][2] and treePrint[i+1][2]:
            for k in range(treePrint[i][1]):
                printout = printout + "\t"
            printout = printout + treePrint[i][0]

        else:
            for k in range(treePrint[i][1]):
                printout = printout + "\t"
            printout = printout + treePrint[i][0] + "\n"
    print(printout)
