import regex as re

def reader(filename):
    file = open(filename)
    input = file.read()
    attributes = re.finditer('(.*\n)', input)
    for line in attributes:
        word = line.group().replace('\n', '')
        pos = word.find('%')
        if(pos != -1):
            word = word[0:pos]
        if(word != ''):
            print(word)






















if __name__ == '__main__':
    column_names = ['Alternative', 'Bar', 'Fri/Sat', 'Hungry', 'Patrons',
    'Price', 'Raining', 'Reservation', 'Type', 'WaitEstimate']
    filename = 'input.arff'
    reader(filename)
