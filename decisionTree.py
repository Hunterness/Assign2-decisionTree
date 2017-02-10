import regex as re

def reader(filename):
    file = open(filename)
    input = file.read().lower()
    attributes = re.finditer('(.*\n)', input)
    for line in attributes:
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
                    types = word[pos+2:len(word)-1]
                print("attribut: ", attr, "types: ", types)
            else:
                print("data: ", word)





















if __name__ == '__main__':
    column_names = ['Alternative', 'Bar', 'Fri/Sat', 'Hungry', 'Patrons',
    'Price', 'Raining', 'Reservation', 'Type', 'WaitEstimate']
    filename = 'input.arff'
    reader(filename)
