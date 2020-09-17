#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include<vector>  
using namespace std;
#include <mutex>
#include <list>

int** position_table;
std::mutex** lock_table;

class Mower {
   int j;
    int x, y;
    char direction;
  public:
   Mower(int j_x){
      j=j_x;
      x = 0;
      y=0;
      direction='N';
   }
    void set_values (int x_c,int y_c,char d){
      x=x_c;
      y=y_c;
      direction=d;
    };
    int get_x (void){
       return x;
    };
    int get_y (void){
       return y;
    };
      int get_j (void){
       return j;
    };
    char get_direction (void){
       return direction;
    };
};

std::vector<std::string> split(std::string stringToBeSplitted, std::string delimeter)
{
     std::vector<std::string> splittedString;
     int startIndex = 0;
     int  endIndex = 0;
     while( (endIndex = stringToBeSplitted.find(delimeter, startIndex)) < stringToBeSplitted.size() )
    {
       std::string val = stringToBeSplitted.substr(startIndex, endIndex - startIndex);
       splittedString.push_back(val);
       startIndex = endIndex + delimeter.size();
     }
     if(startIndex < stringToBeSplitted.size())
     {
       std::string val = stringToBeSplitted.substr(startIndex);
       splittedString.push_back(val);
     }
     return splittedString;
}

void mower_i(Mower* mower,string a,string b,int x_max,int y_max){
   int x_current=0;
   int y_current=0;
   char direction;
   std::vector<std::string> splittedString;
   splittedString = split(a," ");
   x_current = atoi(splittedString[0].c_str());
   y_current = atoi(splittedString[1].c_str());
   lock_table[x_current][y_current].lock();
   position_table[x_current][y_current] = 1;
   lock_table[x_current][y_current].unlock();
   direction = splittedString[2][0];
   for (int i=0 ; i<b.length() ; i++){
      char command = b[i];
      if(command =='R'){
         switch(direction){
            case 'N':
               direction = 'E';
               break;
            case 'E':
               direction = 'S';
               break;
            case 'S':
               direction = 'W';
               break;
            case 'W':
               direction = 'N';
               break;
            
         }
      }
      else if(command =='L'){
         switch(direction){
            case 'N':
               direction = 'W';
               break;
            case 'W':
               direction = 'S';
               break;
            case 'S':
               direction = 'E';
               break;
            case 'E':
               direction = 'N';
               break;
            
         }
      }
      else if(command =='F'){
         int new_x = x_current;
         int new_y = y_current;
         switch(direction){
            case 'N':
               new_y=y_current+1;
               break;
            case 'W':
               new_x=x_current-1;
               break;
            case 'S':
               new_y=y_current-1;
               break;
            case 'E':
               new_x=x_current+1;
               break;
         }
         
         try {
            int old_x=x_current;
            int old_y=y_current;
            if ((new_x < x_max) && (new_x >= 0)  && (new_y < y_max) && (new_y >= 0) ){
                  lock_table[new_x][new_y].lock();
                  if(position_table[new_x][new_y] != 1){
                     lock_table[old_x][old_y].lock();
                     position_table[new_x][new_y] = 1;
                     position_table[x_current][y_current] = 0;
                     lock_table[old_x][old_y].unlock();
                     x_current=new_x;
                     y_current=new_y;
                   }
                  lock_table[new_x][new_y].unlock();
            }
         }
         catch (const std::exception& e){
            cout << "error haha";
         }
         
         
      }
   }
   mower->set_values(x_current,y_current,direction);
}


int main(){
   fstream newfile;
   newfile.open("input.txt",ios::in); //open a file to perform read operation using file object
   if (newfile.is_open()){   //checking whether the file is open
      string tp;
      string header;
      
      int x_max,y_max;
      std::vector<std::thread> threads;
      // Extracts the dimensions of the map
      if (getline(newfile, tp)){ 
         string token1;
         string token2;
         token1 = tp.substr(0, tp.find(" "));
         token2 = tp.substr(tp.find(" ")+1, tp.find("\n"));
         x_max = atoi(token1.c_str())+1;
         y_max = atoi(token2.c_str())+1;

      }
      cout << x_max << y_max << " Header \n";

      // Initializing the table position_table and lock_table
      position_table = new int*[x_max];
      lock_table = new std::mutex*[x_max];
      for(int i = 0; i < x_max; ++i){
         position_table[i] = new int[y_max];
         lock_table[i] = new std::mutex[y_max];
      }
      for (int i; i<x_max+1;i++){
         for (int j; j<y_max+1;j++){
            position_table[i][j]=0;
         }
      }

      std::list <Mower*> mowers; // List of the mowers
      // Read every two lines of the file
      while(getline(newfile, tp)){ //read data from file object and put it inthread.
         try{
            string gg;
            getline(newfile, gg);
            Mower *new_mower = new Mower(j);
            threads.push_back(std::thread(mower_i,new_mower, tp,gg,x_max,y_max));
            mowers.push_back(new_mower); // add the mower to the list of mowers
         }
         catch(const std::exception& e) {
            cout << "something";
         }
        
      }
      // Waiting for the threads to finish
      for(auto& thread : threads){
         thread.join();
      }
      // Writing the results
      ofstream myfile;
      myfile.open ("output.txt");
      for(auto m : mowers){
         myfile << m->get_x()<<" " << m->get_y()<<" " << m->get_direction() <<"\n" ;
      }
      myfile.close();

      newfile.close(); //close the file object.
   }
}