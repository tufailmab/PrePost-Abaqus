# -*- coding: mbcs -*-

# Script: Extract SDV Images from ABAQUS ODB Files
# Purpose: Generate deformation contour images (SDV1-SDV10) from UMAT models for deep learning datasets
# Developer: Tufail Mabood
# Contact: +923440907874 | +923400740460 | Tufail_mabood@yahoo.com

# Some Notes (Adding after uploading):
# - Place this script in the folder containing your .odb files
# - Run the script in Abaqus CAE to extract contour images
# - Images are saved in "SDV" folder with organized subfolders for each ODB and SDV variable (SDV1-SDV10)

from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import os

executeOnCaeStartup()

# Get current working directory
cwd = os.getcwd()

# Create main SDV folder if it doesn't exist (For Images)
sdv_main_folder = os.path.join(cwd, "SDV")
if not os.path.exists(sdv_main_folder):
    os.makedirs(sdv_main_folder)

# Loop through all odb files in current directory (Works best for Batch Submissions, if you are using my repos:
# - Abaqus-Batch-Submit-Job: https://github.com/tufailmab/Abaqus-Batch-Submit-Job
# - Abaqus-OneInp-MultiFor: https://github.com/tufailmab/Abaqus-OneInp-MultiFor
# - Abaqus-MultiInp-OneFor: https://github.com/tufailmab/Abaqus-MultiInp-OneFor

for odb_file in os.listdir(cwd):
    if odb_file.endswith('.odb'):
        # Get odb filename without extension
        odb_name = os.path.splitext(odb_file)[0]
        
        # Create subfolder for this odb file
        odb_folder = os.path.join(sdv_main_folder, odb_name)
        if not os.path.exists(odb_folder):
            os.makedirs(odb_folder)
        
        # Open odb file
        odb_path = os.path.join(cwd, odb_file)
        o1 = session.openOdb(name=odb_path)
        session.viewports['Viewport: 1'].setValues(displayedObject=o1)
        
        # Setup viewport
        session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF,))
        session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM)
        session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(triad=OFF, legend=OFF, title=OFF, state=OFF, annotations=OFF, compass=OFF)
        session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=ON)
        session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legend=ON, title=OFF)
        session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legendFont='-*-times new roman-medium-r-normal-*-*-120-*-*-p-*-*-*')
        session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(numIntervals=6)
        session.graphicsOptions.setValues(backgroundStyle=SOLID, backgroundColor='#FFFFFF')
        
        # Loop through SDV1 to SDV10
        for sdv_num in range(1, 11):
            variable_label = 'SDV' + str(sdv_num)
            session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
                variableLabel=variable_label, outputPosition=INTEGRATION_POINT)
            
            # Create subfolder for each SDV
            sdv_folder = os.path.join(odb_folder, variable_label)
            if not os.path.exists(sdv_folder):
                os.makedirs(sdv_folder)
            
            # Save images for different views
            views = {
                'Iso': 'Iso',
                'Front': 'Front', 
                'Back': 'Back',
                'Top': 'Top',
                'Bottom': 'Bottom',
                'Left': 'Left',
                'Right': 'Right'
            }
            
            for view_name, view_key in views.items():
                session.viewports['Viewport: 1'].view.setValues(session.views[view_key])
                session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
                file_name = os.path.join(sdv_folder, view_name)
                session.printToFile(fileName=file_name, format=PNG, canvasObjects=(session.viewports['Viewport: 1'],))
        
        # Close odb file
        session.odbs[odb_path].close()

print("Image extraction complete for all ODB files and SDV1-SDV10")
