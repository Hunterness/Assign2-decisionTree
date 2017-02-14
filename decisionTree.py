import regex as re

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


    return attributes,data

"""Algorithm for Decision Tree"""

def same_class(examples):
    nbr_yes = 0
    nbr_no = 0
    for key in examples.keys():
        values = examples.get(key)
        indexLast = len(values)
        if values[indexLast-1][1] == 'yes':
            nbr_yes = nbr_yes + 1
        else:
            nbr_no = nbr_no + 1
    if nbr_no == 0 or nbr_yes == 0:
        return True
    return False

def importance(attributes):
    #print("do something")
    return attributes[0][0]

def plurality_value(examples):
    #print("do something")
    i = len(examples.get(0))
    return examples[0][i-1]


def decision_tree_algorithm(examples, attributes,parent_examples):
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
        return plurality_value(parent_examples)
    elif same_class(examples):
        #alla kvarvarande exempel har samma resultat
        i = len(examples.get(0))
        return examples[0][i-1]
    elif not attributes:
        #no more attributes
        return plurality_value(examples)
    else:
        a = importance(attributes)




if __name__ == '__main__':
    #column_names = ['Alternative', 'Bar', 'Fri/Sat', 'Hungry', 'Patrons',
    #'Price', 'Raining', 'Reservation', 'Type', 'WaitEstimate']
    filename = 'input_withRes.arff'
    attributes, data = reader(filename)
    decision_tree_algorithm(data, attributes, data)
