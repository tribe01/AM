from __future__ import print_function
import os, sys

# Construct Thermal Gradient vector and filter the thermal gradient at the liquid solid interface and the liquid solid interface velocity with help of cooling rate
OpenDatabase("MAIN-data.gmv.*.gmv database", 0)
DefineScalarExpression("Cooling_Rate", "(<dT/dt>)")
DefineVectorExpression("Thermal_Gradient_Vector", "{<dT/dx>,<dT/dy>,<dT/dz>}")
DefineScalarExpression("Thermal_Gradient_Magnitude", "magnitude(Thermal_Gradient_Vector)")
DefineScalarExpression("Thermal_Gradient_Interface", "if(and(and(lt(T,1610), gt(T,1600)),lt(Cooling_Rate,0)), abs(Thermal_Gradient_Magnitude), 0)")
DefineScalarExpression("LS_Interface_Velocity", "if(and(and(lt(T,1610), gt(T,1600)),gt(Thermal_Gradient_Magnitude,1)), abs(Cooling_Rate/(Thermal_Gradient_Magnitude)), 0)")

#Calculate number of time states
n=TimeSliderGetNStates()-1;
#Check for complete solidification
AddPlot("Pseudocolor", "T")
DrawPlots()
SetTimeSliderState(n)
Query("Max")
max_temp = GetQueryOutputValue()
MT = open("max_temp.txt", "wb+")
MT.write("Maximum Temperature at the last time step is: "+str(max_temp)+" K");
MT.close()
if max_temp > 1610:
    ER = open("postprocessing_failure.txt", "wb+")
    ER.write("PostProcessing has been terminated prematurely.\nMelt pool has not solidified completely when simulation ended. Try increasing bounds of Output_T in the simulation input file.\nMaximum Temperature at the last time step is: "+str(max_temp)+" K");
    ER.close()
    sys.exit()

#Export Interface Velocity in XYZ(.okc) format
DeleteAllPlots()
AddPlot("Pseudocolor","LS_Interface_Velocity")
DrawPlots()
for i in range(TimeSliderGetNStates()):
    SetActiveWindow(1)
    SetTimeSliderState(i)
    ExportDBAtts = ExportDBAttributes()
    ExportDBAtts.db_type = "Xmdv"
    ExportDBAtts.filename = "R%04d" %i
    ExportDBAtts.dirname = "."
    ExportDBAtts.variables = ("LS_Interface_Velocity")
    ExportDBAtts.opts.types = ()
    ExportDatabase(ExportDBAtts)

# Export Interface Thermal Gradient in XYZ (.okc) format
DeleteAllPlots()
AddPlot("Pseudocolor","Thermal_Gradient_Interface")
DrawPlots()
for i in range(TimeSliderGetNStates()):
    SetActiveWindow(1)
    SetTimeSliderState(i)
    ExportDBAtts = ExportDBAttributes()
    ExportDBAtts.db_type = "Xmdv"
    ExportDBAtts.filename = "G%04d" %i
    ExportDBAtts.dirname = "."
    ExportDBAtts.variables = ("Thermal_Gradient_Interface")
    ExportDBAtts.opts.types = ()
    ExportDatabase(ExportDBAtts)

sys.exit()

