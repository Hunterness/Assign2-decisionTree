import regex as re
from collections import OrderedDict
from math import log2

"""Reader. reads in ARFF-file
    Can't handle '?' in data or
    any valutypes not within {} for the attributes"""
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


def decision_tree_algorithm(examples, attributes,parent_examples,turn):
    types = attributes['willwait'][1:len(attributes['willwait'])]
    if not examples:
        #no more data
        treePrint.append((": " + plurality_value(parent_examples,types),0,True))
    elif same_class(examples,types):
        #alla kvarvarande exempel har samma resultat
        treePrint.append((": " + examples[0][-1][1],0,True))
    elif not attributes:
        #no more attributes
        treePrint.append((": " + plurality_value(examples,types),0,True))
    else:
        a = importance(attributes, examples,types)
        i = attributes[a][0]
        values = attributes[a][1:len(attributes[a])]
        del attributes[a]
        for v in values:
            treePrint.append((a + " = " + v,turn,False))
            exs = []
            for j in range(len(examples)):
                res = examples[j][i][1]
                if res == v:
                    exs.append(examples[j])
            decision_tree_algorithm(exs,attributes,examples,turn+1)


if __name__ == '__main__':
    filename = 'input_2res.arff'
    attributes, data = reader(filename)
    decision_tree_algorithm(data, attributes, data,0)
    print("Restaurant 2:")
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
    printout = printout + treePrint[-1][0]
    print(printout)


    treePrint = []
    filename = 'input_3res.arff'
    attributes, data = reader(filename)
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
    printout = printout + treePrint[-1][0]
    print(printout)
