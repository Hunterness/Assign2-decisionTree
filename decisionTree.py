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

def same_class(examples):
    nbr_yes = 0
    nbr_no = 0
    for e in examples:
        if e[-1][1] == 'yes':
            nbr_yes = nbr_yes + 1
        else:
            nbr_no = nbr_no + 1
    if nbr_no == 0 or nbr_yes == 0:
        return True
    return False

def nbrPosNegPerVal(examples, attributes, attr, val):
    nbrPos = 0
    nbrNeg = 0
    indexAttr = attributes[attr][0]
    for e in examples:
        if e[indexAttr][1] == val:
            if e[-1][1] == 'yes':
                nbrPos = nbrPos + 1
            else:
                nbrNeg = nbrNeg + 1

    return nbrPos, nbrNeg

def nbrPosNegTotal(examples, attributes, attr):
    nbrPos = 0
    nbrNeg = 0
    indexAttr = attributes[attr][0]
    for e in examples:
        if e[-1][1] == 'yes':
            nbrPos = nbrPos + 1
        else:
            nbrNeg = nbrNeg + 1
    return nbrPos, nbrNeg

def B(q):
    if q == 0 or q == 1:
        return 0
    return -(q*log2(q)+(1-q)*log2(1-q))

def importance(attributes, examples): #just nu bara första attributet
    max_attr = ''
    max_gain = 0
    for a in attributes:
        if a != 'willwait':
            remainder = 0
            pT,nT = nbrPosNegTotal(examples,attributes,a)

            for v in attributes[a][1:len(attributes[a])]:
                pV,nV = nbrPosNegPerVal(examples,attributes,a,v)
                #print(a,v,(pV+nV),(pT+nT))
                if pV+nV != 0:
                    q = pV/(pV+nV)
                    remainder = remainder + B(q)*(pV+nV)/(pT+nT)

            gain = B(pT/(pT+nT))-remainder
            if gain > max_gain:
                max_attr = a
                max_gain = gain

    return max_attr


def plurality_value(examples): #just nu bara första exemplet?
    nbrYes = 0
    nbrNo = 0
    for e in examples:
        if e[-1][1] == 'yes':
            nbrYes = nbrYes + 1
        else:
            nbrNo = nbrNo + 1
    if nbrYes == nbrNo:
        return examples[0][-1][1]
    elif nbrYes > nbrNo:
        return 'yes'
    else:
        return 'no'



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
    if not examples:
        #no more data
        return ": " + plurality_value(parent_examples) + "\n", True
    elif same_class(examples):
        #alla kvarvarande exempel har samma resultat
        return ": " + examples[0][-1][1] + "\n", True #returnerar yes/no
    elif not attributes:
        #no more attributes
        return ": " + plurality_value(examples) + "\n", True
    else:
        a = importance(attributes, examples)
        tree = ""
        i = attributes[a][0]
        values = attributes[a][1:len(attributes[a])]
        del attributes[a]
        for v in values:
            tree = tree + a + " = " + v
            exs = []
            for j in range(len(examples)):
                res = examples[j][i][1]
                if res == v:
                    exs.append(examples[j])
            subtree, end = decision_tree_algorithm(exs,attributes,examples,turn+1)
            if end:
                tree = tree + subtree
            else:
                tree = tree + "\n"
                for k in range(turn+1):
                    tree = tree + "\t"
                tree = tree + subtree
        return tree, False





if __name__ == '__main__':
    filename = 'input_withRes.arff'
    attributes, data = reader(filename)
    tree, end = decision_tree_algorithm(data, attributes, data,0)
    print(tree)
