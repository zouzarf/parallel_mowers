input_file = open('input.txt','w')


import random
added_coordinates = []
directions = ['N','E','W','S']
commands = ['F','L','R']
number_of_mowers = 10000
number_of_commands_per_mower=50
x_max = 1000
y_max = 1000
input_file.write(str(x_max)+' '+str(y_max)+'\n')
for i in range(number_of_mowers):
    x = random.randint(1,x_max)
    y = random.randint(1,y_max)
    while ( (x,y) in added_coordinates):
        x = random.randint(1,x_max)
        y = random.randint(1,y_max)
    added_coordinates.append((x,y))
    direction = random.randint(0,3)
    d=directions[direction]
    s = str(x) + ' ' + str(y) + ' ' + str(d)
    input_file.write(s+'\n')
    
    list_commands = ''
    nb_of_commands = random.randint(1,number_of_commands_per_mower)
    for j in range (nb_of_commands):
        command = random.randint(0,2)
        c = commands[command]
        list_commands = list_commands + c
    input_file.write(list_commands+'\n')
input_file.close()
