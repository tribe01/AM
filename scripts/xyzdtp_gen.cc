// Program to generate ptg file for the new point net tile matrix pattern 
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cstring>
#include <sstream>
#include <cmath>
#include <limits>
using namespace std;

int main ()
{ 
  
  float on_time,power,wait_time; //wait time between return in milliseconds
  cout<<"Enter ON time in seconds: "; cin>>on_time;
  cout<<endl<<"Enter power in watts: "; cin>>power;
  cout<<endl<<"Enter wait time in seconds: "; cin>>wait_time;
  ofstream myfile_1;
  myfile_1.open("xyzdtp.dat");
  myfile_1<<"0 0 0 0"<<endl;
  myfile_1<<"-0.0004 -0.0004 "<<on_time<<" "<<power<<endl;
  myfile_1<<"+0.0004 +0.0004 "<<on_time<<" "<<power<<endl;
  myfile_1<<"-0.0004 +0.0004 "<<on_time<<" "<<power<<endl;
  myfile_1<<"+0.0004 -0.0004 "<<on_time<<" "<<power<<endl;
  myfile_1<<"+0.0000 +0.0000 "<<wait_time<<" 0"<<endl;
  myfile_1<<"+0.0000 +0.0000 "<<on_time<<" "<<power<<endl;
  myfile_1.close();
 
  return 0;
}


