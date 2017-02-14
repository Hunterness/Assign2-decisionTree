import regex as re

"""Reader. reads in ARFF-file"""
def reader(filename):
    attributes = {}
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
                data = {}
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
		return tree
	"""


def importance(attributes):

def plurality_value(examples):


if __name__ == '__main__':
    #column_names = ['Alternative', 'Bar', 'Fri/Sat', 'Hungry', 'Patrons',
    #'Price', 'Raining', 'Reservation', 'Type', 'WaitEstimate']
    filename = 'input_withRes.arff'
    attribute, data = reader(filename)
    decision_tree_algorithm(data, attribute, data)
