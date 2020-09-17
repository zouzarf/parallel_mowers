
input_file = open('input.txt','r')
import numpy as np
contents = input_file.readlines()


global position_table
global x_max
global y_max
global redirector
redirector = {'N':(0,1),'E':(1,0),'S':(0,-1),'W':(-1,0)}
global clockwise_directions
clockwise_directions = ['N','E','S','W']

class Mower():
    def __init__(self, x, y,direction,list_instructions):
        self.x = x
        self.y = y
        self.direction = direction
        self.instructions=list_instructions
        position_table[x][y]=1
        #print('Added instructions' + str(self.instructions))
    def iterate_once(self):
        if self.instructions:
            instr = self.instructions.pop(0)
            self.instruction(instr)
            return True
        return False
    def instruction(self,instr):
        if instr=='F':
            self.move_forward()
            #print('Forward !!')
        elif instr=='L':
            self.direction = clockwise_directions[(clockwise_directions.index(self.direction)-1)%4]
            #print('Changed direction to '+self.direction)
        elif instr=='R':
            self.direction = clockwise_directions[(clockwise_directions.index(self.direction)+1)%4]
    def move_forward(self):
        new_x = self.x
        new_y = self.y
        new_x,new_y = [sum(x) for x in zip((new_x,new_y), redirector[self.direction])]
        if (new_x < x_max and new_x >= 0  and new_y < y_max and new_y >= 0 and position_table[new_x][new_y] != 1):
            position_table[self.x][self.y]=0
            position_table[new_x][new_y]=1
            self.y=new_y
            self.x=new_x

#Loading the parameters of the map
try: 
    x_max, y_max =  map (int , contents.pop(0).rstrip('\n').split(' '))
    x_max +=1
    y_max +=1
    position_table = np.zeros((x_max,y_max))
    list_mowers=[]

except:
    print("Error while loading the parameters")
    exit()

#Loading the mowers
it = iter(contents)
for x in it:
    #try:
        input_coordinates = x
        input_instructions = next(it)
        m_x,m_y,m_direction= input_coordinates.rstrip('\n').split(' ')
        m_x = int(m_x)
        m_y = int(m_y)
        m_instructions = [k for k in input_instructions.rstrip('\n')]
        new_mower = Mower(m_x,m_y,m_direction,m_instructions)
        list_mowers.append(new_mower)
    # except:
    #     print("Error while loading the parameters. Make sure they have the correct format")
    #     exit()

#Starting the simulation
keep_iterating = True
while(keep_iterating):
    keep_iterating = False
    for current_mower in list_mowers:
        if (current_mower.iterate_once()):
            keep_iterating=True
            #print('Mower '+str(i)+' moved to position : '+str(current_mower.x)+','+str(current_mower.y)+','+ str(current_mower.direction))


outF = open("output.txt", "w")

for i in range(len(list_mowers)):
    current_mower = list_mowers[i]
    line = str(current_mower.x)+' '+str(current_mower.y)+' '+str(current_mower.direction+'\n')
    outF.write(line)
outF.close()
input_file.close()