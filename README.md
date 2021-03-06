## parallel_mowers

This repository contains three files:
- test.py ( Generate a random number of mowers with a random number of commands)
- main.py ( Sequential processing of the mowers)
- main_pool.py (Multhithreading processing of the mowers using ThreadPool)
- main.c++ ( Multithreading processing of the mowers)
 <br /> 
Note that I thought that the test would be on python, but, considering that python doesn't support real parallelism, I built a script on c++ that does approximately the same but way faster since c++ supports true parallelism.

## Main_pool.py

This file contains three important parts:
    - Class Mower
    - Thread function 
    - Main function
 <br /> 
Each mower is defined in a Class that has it's attributes (current x y positions , direction , commands assigned to him), and built-in function that makes the mower execute one instruction.
 <br /> 
Main function, responsible of reading the input and passes every two lines to an available thread to process the two lines.
 <br /> 
Thread function, responsible of receiving an empty mower and the two lines . It parses from two lines the position of the mower and the commands and then moves the mower.
 <br /> 
The race condition has been managed by two tables, one table called position_table that records the position of all the mowers at any given instant, 1 if a mower is present at that location , 0 if not. the other table is called lock_table that has locks for every position so that if a mower decides to move to a position x y, it locks that position, reads from position_table if it is allowed to move in, moves in if possible and delocks the position. The reason I decide to have a lock for every position is to allow other mowers to move aswell instead of locking the whole position_table with one lock.
 <br /> 
## Main.c++

Same logic as main_pool.py, with the only difference is that it's written in c++ and it creates a thread for each mower instead of having a TreadPool