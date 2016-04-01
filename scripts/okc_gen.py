import os, sys

# Construct Thermal Gradient vector and filter the thermal gradient at the liquid solid interface and the liquid solid interface velocity with help of cooling rate
OpenDatabase("MAIN-data.gmv.*.gmv database", 0)
DefineScalarExpression("Cooling_Rate", "(<dT/dt>)")
DefineVectorExpression("Thermal_Gradient_Vector", "{<dT/dx>,<dT/dy>,<dT/dz>}")
DefineScalarExpression("Thermal_Gradient_Magnitude", "magnitude(Thermal_Gradient_Vector)")
DefineScalarExpression("Thermal_Gradient_Interface", "if(and(and(lt(T,1610), gt(T,1600)),lt(Cooling_Rate,0)), abs(Thermal_Gradient_Magnitude), 0)")
DefineScalarExpression("LS_Interface_Velocity", "if(and(and(lt(T,1610), gt(T,1600)),gt(Thermal_Gradient_Magnitude,1)), abs(Cooling_Rate/(Thermal_Gradient_Magnitude)), 0)")

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
'''
#Create a contour plot to track meltpool
DeleteAllPlots()
AddPlot("Contour", "T", 1, 1)
CA = ContourAttributes()
CA.minFlag = 1
CA.min =1610
SetPlotOptions(CA)
DrawPlots()

Source("/home/n22/softwares/visit/visit2_7_3.linux-x86_64/2.7.3/linux-x86_64/bin/makemovie.py")
ToggleCameraViewMode()

#Create the images of the meltpool for each time step and make movie out of it
for i in range(TimeSliderGetNStates()):
    SetTimeSliderState(i)
    RA = RenderingAttributes()
    RA.antialiasing = 0
    RA.multiresolutionMode = 0
    RA.multiresolutionCellSize = 0.002
    RA.geometryRepresentation = RA.Surfaces  # Surfaces, Wireframe, Points
    RA.displayListMode = RA.Auto  # Never, Always, Auto
    RA.stereoRendering = 0
    RA.stereoType = RA.CrystalEyes  # RedBlue, Interlaced, CrystalEyes, RedGreen
    RA.notifyForEachRender = 0
    RA.scalableActivationMode = RA.Auto  # Never, Always, Auto
    RA.scalableAutoThreshold = 2000000
    RA.specularFlag = 0
    RA.specularCoeff = 0.6
    RA.specularPower = 10
    RA.specularColor = (255, 255, 255, 255)
    RA.doShadowing = 0
    RA.shadowStrength = 0.5
    RA.doDepthCueing = 0
    RA.depthCueingAutomatic = 1
    RA.startCuePoint = (-10, 0, 0)
    RA.endCuePoint = (10, 0, 0)
    RA.compressionActivationMode = RA.Never  # Never, Always, Auto
    RA.colorTexturingFlag = 1
    RA.compactDomainsActivationMode = RA.Never  # Never, Always, Auto
    RA.compactDomainsAutoThreshold = 256
    SetRenderingAttributes(RA)
    SWA = SaveWindowAttributes()
    SWA.outputToCurrentDirectory = 0
    SWA.outputDirectory = "/home/n22/IN718/pulse/20mA_1ms/delayedspot/400u_dia/4ms/test_output/Meltpool-0"
    SWA.fileName = "Meltpool%04d" %i
    SWA.family = 0
    SWA.format = SWA.PPM  # BMP, CURVE, JPEG, OBJ, PNG, POSTSCRIPT, POVRAY, PPM, RGB, STL, TIFF, ULTRA, VTK, PLY
    SWA.width = 848
    SWA.height = 784
    SWA.screenCapture = 0
    SWA.saveTiled = 0
    SWA.quality = 80
    SWA.progressive = 0
    SWA.binary = 0
    SWA.stereo = 0
    SWA.compression = SWA.PackBits  # None, PackBits, Jpeg, Deflate
    SWA.forceMerge = 0
    SWA.resConstraint = SWA.NoConstraint  # NoConstraint, EqualWidthHeight, ScreenProportions
    SWA.advancedMultiWindowSave = 0
    SetSaveWindowAttributes(SWA)
    SaveWindow()
RenderingAtts = RenderingAttributes()
RenderingAtts.antialiasing = 0
RenderingAtts.multiresolutionMode = 0
RenderingAtts.multiresolutionCellSize = 0.002
RenderingAtts.geometryRepresentation = RenderingAtts.Surfaces  # Surfaces, Wireframe, Points
RenderingAtts.displayListMode = RenderingAtts.Auto  # Never, Always, Auto
RenderingAtts.stereoRendering = 0
RenderingAtts.stereoType = RenderingAtts.CrystalEyes  # RedBlue, Interlaced, CrystalEyes, RedGreen
RenderingAtts.notifyForEachRender = 0
RenderingAtts.scalableActivationMode = RenderingAtts.Auto  # Never, Always, Auto
RenderingAtts.scalableAutoThreshold = 2000000
RenderingAtts.specularFlag = 0
RenderingAtts.specularCoeff = 0.6
RenderingAtts.specularPower = 10
RenderingAtts.specularColor = (255, 255, 255, 255)
RenderingAtts.doShadowing = 0
RenderingAtts.shadowStrength = 0.5
RenderingAtts.doDepthCueing = 0
RenderingAtts.depthCueingAutomatic = 1
RenderingAtts.startCuePoint = (-10, 0, 0)
RenderingAtts.endCuePoint = (10, 0, 0)
RenderingAtts.compressionActivationMode = RenderingAtts.Never  # Never, Always, Auto
RenderingAtts.colorTexturingFlag = 1
RenderingAtts.compactDomainsActivationMode = RenderingAtts.Never  # Never, Always, Auto
RenderingAtts.compactDomainsAutoThreshold = 256
SetRenderingAttributes(RenderingAtts)
'''
sys.exit()

