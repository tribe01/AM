#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <string>
#include <cstring>
#include <sstream>
#include <cassert>
#include <cmath>
#include <iomanip>
#include <time.h>
#include "/home/n22/scripts/array.h"
using namespace std;

int main()
{
 vector <double> X;
 vector <double> Y;
 vector <double> Z;
 vector <double> R;
 vector <double> G;
 vector <double> GnR;
 vector <double> phi;
 // Change the values in the next three lines. No other changes required. 
 int start_time_step=0,end_time_step=200, num_columns, coord_count; //Change only the values for time steps
 double abs_X_mesh_size = 2.0E-05, abs_Y_mesh_size = 2.0E-05;       //Change only the values for mesh sizes to extract XY, XZ plane phi data
 double N_o = 2.0E14, a = 1.25E6, n = 3.4;                          //Original Gaumann: Nucleation density (per m3)
//double N_o = 1.18E15, a = 2.03E6, n = 5.3;                        //Optimized Debroy Paper: Nucleation density (per m3)
 double temp;
 string dummy;
 ofstream output_file;
 ifstream data_file;
 ostringstream oss;

//Create consolidated XYZ Interface Velocity file
 data_file.open("R0000.okc");
 while (data_file.fail())
 {
   cout<<endl<<"File R000.okc not found. Generate okc files before executing this script"<<endl;
   exit (0);
 }
  data_file>> num_columns;
  data_file>> coord_count;
  for(int i=0; i<17; i++)
  {
    data_file>> dummy;
  }
  X.create(1,coord_count);
  Y.create(1,coord_count);
  Z.create(1,coord_count);
  R.create(1,coord_count);
  for(int i=1;i<=coord_count;i++)
  {
    data_file>>X(i);
    data_file>>Y(i);
    data_file>>Z(i);
    data_file>>R(i);
  }
  data_file.close();
  for(int i=start_time_step;i<=end_time_step;i++)
  {
     oss<<"R"<<setfill('0')<<setw(4)<<i<<".okc";
     string file_name=oss.str();
     data_file.open(file_name.c_str());
     while (data_file.fail())
      {
        cout<<endl<<"File "<<file_name<<" is not found."<<endl;
        exit (0);
      }
     for(int j=0;j<19;j++)
     {
       data_file>>dummy;
     }
     for(int i=1;i<=coord_count;i++)
       {
            data_file>>X(i);
            data_file>>Y(i);
            data_file>>Z(i);
            data_file>>temp;
            if(temp>0) R(i)=temp;
            else continue;
        }
     oss.str("");
     data_file.close();
  }
  output_file.open("R_v1.txt");
  for(int i=1;i<=coord_count;i++)
  {
    output_file<<setprecision(20)<<X(i)<<"	"<<setprecision(20)<<Y(i)<<"	"<<setprecision(20)<<Z(i)<<"	"<<setprecision(20)<<R(i)<<endl;
  }
  output_file.close();
  X.free();
  Y.free();
  Z.free();

//Create a consolidated XYZ Gradient File
 data_file.open("G0000.okc");
 while (data_file.fail())
 {
   cout<<endl<<"File G000.okc not found. Generate okc files before executing this script"<<endl;
   exit (0);
  }
  data_file>> num_columns;
  data_file>> coord_count;
  for(int i=0; i<17; i++)
  {
    data_file>> dummy;
  }
  X.create(1,coord_count);
  Y.create(1,coord_count);
  Z.create(1,coord_count);
  G.create(1,coord_count);
  for(int i=1;i<=coord_count;i++)
  {
    data_file>>X(i);
    data_file>>Y(i);
    data_file>>Z(i);
    data_file>>G(i);
  }
  data_file.close();
  for(int i=start_time_step;i<=end_time_step;i++)
  {
     oss<<"G"<<setfill('0')<<setw(4)<<i<<".okc";
     string file_name=oss.str();
     data_file.open(file_name.c_str());
     while (data_file.fail())
      {
        cout<<endl<<"File "<<file_name<<" is not found."<<endl;
        exit (0);
      }
     for(int j=0;j<19;j++)
     {
       data_file>>dummy;
     }
     for(int i=1;i<=coord_count;i++)
       {
            data_file>>X(i);
            data_file>>Y(i);
            data_file>>Z(i);
            data_file>>temp;
            if(temp>0) G(i)=temp;
            else continue;
        }
     oss.str("");
     data_file.close();
  }
  output_file.open("G_v1.txt");
  for(int i=1;i<=coord_count;i++)
  {
    output_file<<setprecision(20)<<X(i)<<"	"<<setprecision(20)<<Y(i)<<"	"<<setprecision(20)<<Z(i)<<"	"<<setprecision(20)<<G(i)<<endl;
  }
  output_file.close();
//Generate GR file 3 dimenrion 
  output_file.open("GR_phi_3D.txt");
  GnR.create(1,coord_count); // G^n/R vector
  phi.create(1,coord_count); // Probability of stray grain formation vector
  int non_zero_volume_ele_count=0;
  double cumulative_phi =0; // in cubic microns
  output_file<<"X Y Z Interface_Velocity Thermal_Gradient G^n/R phi"<<endl;
  for(int i=1;i<=coord_count;i++)
  { 
     if(R(i)>0&&G(i)>0)
       {
         GnR(i) = pow(G(i),n)/R(i);
         phi(i) = 1-(exp((-4*22/7*N_o/3*pow(1/(n+1)/pow((GnR(i)/a),(1/n)),3))));
         output_file<<setprecision(20)<<X(i)<<"	"<<setprecision(20)<<Y(i)<<"	"<<setprecision(20)<<Z(i)<<"	"<<setprecision(20)<<R(i)<<"	"<<setprecision(20)<<G(i)<<"	"<<setprecision(20)<<GnR(i)<<"	"<<setprecision(20)<<phi(i)<<endl;
         non_zero_volume_ele_count = non_zero_volume_ele_count + 1;
         cumulative_phi = cumulative_phi + phi(i);
       }
     else continue; 
  } 
  output_file.close();
//Calculate and Write volume fraction of equiaxed grains formed: one vale in one simulation
  double PHI = cumulative_phi/non_zero_volume_ele_count;
  output_file.open("PHI.txt");
  output_file<<"The volume fraction of equiaxed grains in this simulation is:  "<<PHI<<endl;
  output_file.close(); 
//Generate GR file for XZ plane
  output_file.open("GR_phi_XZ_plane.txt");
  cout<<"Writing GR_phi_XZ_plane.txt"<<endl;
  output_file<<"X Y Z Interface_Velocity Thermal_Gradient G^n/R phi"<<endl;  
  for(int i=1;i<=coord_count;i++)
  {
     if(R(i)>0&&G(i)>0&&Y(i)<abs_Y_mesh_size&&Y(i)>0.0)  //Change according to mesh size
       {
         output_file<<setprecision(20)<<X(i)<<"	"<<setprecision(20)<<Y(i)<<"	"<<setprecision(20)<<Z(i)<<"	"<<setprecision(20)<<R(i)<<"	"<<setprecision(20)<<G(i)<<"	"<<setprecision(20)<<GnR(i)<<"	"<<setprecision(20)<<phi(i)<<endl;
       }
     else continue;
  }
  output_file.close();
//Generate GR for YZ plane
  output_file.open("GR_phi_YZ_plane.txt");
  cout<<"Writing GR_phi_YZ_plane.txt"<<endl;
  output_file<<"X Y Z Interface_Velocity Thermal_Gradient G^n/R phi"<<endl;
  for(int i=1;i<=coord_count;i++)
  {
     if(R(i)>0&&G(i)>0&&X(i)<abs_X_mesh_size&&X(i)>0.0)  //Change according to mesh size
       {
         output_file<<setprecision(20)<<X(i)<<"	"<<setprecision(20)<<Y(i)<<"	"<<setprecision(20)<<Z(i)<<"	"<<setprecision(20)<<R(i)<<"	"<<setprecision(20)<<G(i)<<"	"<<setprecision(20)<<GnR(i)<<"	"<<setprecision(20)<<phi(i)<<endl;
       }
     else continue;
  }
  output_file.close();
  cout<<endl<<"Number of coordinate points in the domain is: "<<coord_count<<endl;
  return 0;
}
                                                                                                    
