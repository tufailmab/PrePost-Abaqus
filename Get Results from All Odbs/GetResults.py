# Developer
# Engr. Tufail Mabood
# WhatsApp: +923440907874

# -*- coding: mbcs -*-

from abaqus import *
from abaqusConstants import *

import os
import csv

# Current working directory
folder = os.getcwd()

# Create output folder
outputFolder = os.path.join(folder, 'All Required Outputs')

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

# CSV file
csvFile = os.path.join(outputFolder, 'Results.csv')

# CSV Header
results = []
results.append([
    'ODB Name',
    'Max Mises Stress',
    'Max CE (Max Principal)',
    'Max Displacement'
])

# Process every ODB in the current directory
for file in os.listdir(folder):

    if file.lower().endswith('.odb'):

        print '----------------------------------------'
        print 'Processing:', file

        odb = session.openOdb(
            name=os.path.join(folder, file)
        )

        # First analysis step
        step = odb.steps.values()[0]

        maxStress = -1.0
        maxCE = -1.0
        maxU = -1.0

        # Loop through every frame
        for frame in step.frames:
            
            # Von Mises Stress
            
            if 'S' in frame.fieldOutputs.keys():
                for value in frame.fieldOutputs['S'].values:
                    if value.mises > maxStress:
                        maxStress = value.mises
                        
            # CE (Maximum Principal)
            
            if 'CE' in frame.fieldOutputs.keys():
                for value in frame.fieldOutputs['CE'].values:
                    if value.maxPrincipal > maxCE:
                        maxCE = value.maxPrincipal

            # Displacement Magnitude

            if 'U' in frame.fieldOutputs.keys():
                for value in frame.fieldOutputs['U'].values:
                    if value.magnitude > maxU:
                        maxU = value.magnitude

        # Store results
        results.append([
            file,
            maxStress,
            maxCE,
            maxU
        ])

        odb.close()

# Write CSV file
f = open(csvFile, 'wb')
writer = csv.writer(f)
writer.writerows(results)
f.close()

print
print ' All ODB files processed successfully.'
print ' Results saved in:'
print ' ', outputFolder
