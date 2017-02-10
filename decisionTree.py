
if __name__ == '__main__':
    column_names = ['Alternative', 'Bar', 'Fri/Sat', 'Hungry', 'Patrons',
    'Price', 'Raining', 'Reservation', 'Type', 'WaitEstimate']
    filename = 'input.arff'
    file = open(filename)
    input = file.readlines()
    print(input[0])
