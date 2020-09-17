from threading import Thread
import numpy as np
import threading
from multiprocessing import Process,Manager
from multiprocessing.pool import ThreadPool
import multiprocessing

global position_table
global x_max
global y_max
global redirector
global clockwise_directions
global lock_table

#helper variables 
redirector = {'N':(0,1),'E':(1,0),'S':(0,-1),'W':(-1,0)}
clockwise_directions = ['N','E','S','W']

import timeit

# Mower Class
class Mower():
    def __init__(self, x=0, y=0,direction='N',list_instructions=[]):
        self.x = x
        self.y = y
        self.direction = direction
        self.instructions=list_instructions
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
        global position_table
        global lock_table
        new_x = self.x
        new_y = self.y
        new_x,new_y = [sum(x) for x in zip((new_x,new_y), redirector[self.direction])]
        old_x = self.x
        old_y = self.y
        if (new_x < x_max and new_x >= 0  and new_y < y_max and new_y >= 0 and lock_table[new_x][new_y].acquire()):
            if(position_table[new_x][new_y] != 1):
                lock_table[old_x][old_y].acquire()
                position_table[old_x][old_y]=0
                lock_table[old_x][old_y].release()
                position_table[new_x][new_y]=1
                self.y=new_y
                self.x=new_x
            lock_table[new_x][new_y].release()
#Thread function that take a mower and executes its commands
def iterate_mower(mower,input_coordinates,instructions):
    global lock_table
    global position_table
    m_x,m_y,m_direction= input_coordinates.rstrip('\n').split(' ')
    m_x = int(m_x)
    m_y = int(m_y)
    m_instructions = [k for k in instructions.rstrip('\n')]
    mower.x=m_x
    mower.y=m_y
    mower.direction=m_direction
    mower.instructions = m_instructions
    lock_table[m_x][m_y].acquire()
    position_table[m_x][m_y]=1
    lock_table[m_x][m_y].release()
    while mower.iterate_once():
        pass

if __name__ == '__main__':
    global lock_table
    global position_table
    #Loading the file
    input_file = open('input.txt','r')
    first_line = input_file.readline()
    #Loading the parameters of the map
    try: 
        x_max, y_max =  map (int , first_line.rstrip('\n').split(' ')) # Parses the elements of the first line and extract the dimensions of the map
        x_max +=1
        y_max +=1
        position_table = np.zeros((x_max,y_max))
        list_mowers=[]
        #lock for each position in the map
        lock_table=[]
        for i in range (x_max):
            l = []
            for j in range (y_max):
                a = threading.Lock()
                l.append(a)
            lock_table.append(l)
    except:
        print("Error while loading the parameters")
        exit()

    # Defining the ThreadPool we will be
    pool = ThreadPool(16)
    jobs = []
    list_mowers=[]

    #Loading the mowers
    while(True):
        positions = input_file.readline()
        input_instructions = input_file.readline()
        if not positions or not input_instructions:
            break
        new_mower = Mower()
        list_mowers.append(new_mower)
        jobs.append(pool.apply_async(iterate_mower,(new_mower,positions,input_instructions,)))
    
    # Waiting for threads to finish
    for job in jobs:
        job.get()
    pool.close()
    pool.join()

    # Writing the results
    outF = open("output.txt", "w")

    for current_mower in list_mowers:
        line = str(current_mower.x)+' '+str(current_mower.y)+' '+str(current_mower.direction+'\n')
        outF.write(line)
    outF.close()
    input_file.close()