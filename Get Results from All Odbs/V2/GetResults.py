# Developer
# Engr. Tufail Mabood
# WhatsApp: +923440907874

# -*- coding: mbcs -*-

from abaqus import *
from abaqusConstants import *

import os
import csv

folder = os.getcwd()

outputFolder = os.path.join(folder, 'All Required Outputs')

if not os.path.exists(outputFolder):
    os.mkdir(outputFolder)

csvFile = os.path.join(outputFolder, 'Results.csv')

results = [[
    'ODB Name',
    'Instance',
    'Max Mises Stress',
    'Max Principal Stress',
    'Max S11',
    'Max S22',
    'Max S33',
    'Max CE (Max Principal)',
    'Max CE11',
    'Max CE22',
    'Max CE33',
    'Max PE (Max Principal)',
    'Max PE11',
    'Max PE22',
    'Max PE33',
    'Max PEEQ',
    'Max Displacement',
    'Max U1',
    'Max U2',
    'Max U3'
]]

def newRecord():
    return {
        'maxStress': -1.0,
        'maxPrincipalStress': -1.0,
        'maxS11': -1.0,
        'maxS22': -1.0,
        'maxS33': -1.0,
        'maxCE': -1.0,
        'maxCE11': -1.0,
        'maxCE22': -1.0,
        'maxCE33': -1.0,
        'maxPE': -1.0,
        'maxPE11': -1.0,
        'maxPE22': -1.0,
        'maxPE33': -1.0,
        'maxPEEQ': -1.0,
        'maxU': -1.0,
        'maxU1': -1.0,
        'maxU2': -1.0,
        'maxU3': -1.0
    }

for file in os.listdir(folder):

    if not file.lower().endswith('.odb'):
        continue

    print '----------------------------------------'
    print 'Processing:', file

    odb = session.openOdb(name=os.path.join(folder, file))

    instanceResults = {}

    for step in odb.steps.values():

        for frame in step.frames:

            # Stress
            if 'S' in frame.fieldOutputs.keys():
                for value in frame.fieldOutputs['S'].values:

                    inst = value.instance.name

                    if inst not in instanceResults:
                        instanceResults[inst] = newRecord()

                    r = instanceResults[inst]

                    if value.mises > r['maxStress']:
                        r['maxStress'] = value.mises

                    if value.maxPrincipal > r['maxPrincipalStress']:
                        r['maxPrincipalStress'] = value.maxPrincipal

                    if value.data[0] > r['maxS11']:
                        r['maxS11'] = value.data[0]

                    if value.data[1] > r['maxS22']:
                        r['maxS22'] = value.data[1]

                    if value.data[2] > r['maxS33']:
                        r['maxS33'] = value.data[2]

            # Creep Strain
            if 'CE' in frame.fieldOutputs.keys():
                for value in frame.fieldOutputs['CE'].values:

                    inst = value.instance.name

                    if inst not in instanceResults:
                        instanceResults[inst] = newRecord()

                    r = instanceResults[inst]

                    if value.maxPrincipal > r['maxCE']:
                        r['maxCE'] = value.maxPrincipal

                    if value.data[0] > r['maxCE11']:
                        r['maxCE11'] = value.data[0]

                    if value.data[1] > r['maxCE22']:
                        r['maxCE22'] = value.data[1]

                    if value.data[2] > r['maxCE33']:
                        r['maxCE33'] = value.data[2]

            # Plastic Strain
            if 'PE' in frame.fieldOutputs.keys():
                for value in frame.fieldOutputs['PE'].values:

                    inst = value.instance.name

                    if inst not in instanceResults:
                        instanceResults[inst] = newRecord()

                    r = instanceResults[inst]

                    if value.maxPrincipal > r['maxPE']:
                        r['maxPE'] = value.maxPrincipal

                    if value.data[0] > r['maxPE11']:
                        r['maxPE11'] = value.data[0]

                    if value.data[1] > r['maxPE22']:
                        r['maxPE22'] = value.data[1]

                    if value.data[2] > r['maxPE33']:
                        r['maxPE33'] = value.data[2]

            # Equivalent Plastic Strain
            if 'PEEQ' in frame.fieldOutputs.keys():
                for value in frame.fieldOutputs['PEEQ'].values:

                    inst = value.instance.name

                    if inst not in instanceResults:
                        instanceResults[inst] = newRecord()

                    r = instanceResults[inst]

                    if value.data > r['maxPEEQ']:
                        r['maxPEEQ'] = value.data

            # Displacement
            if 'U' in frame.fieldOutputs.keys():
                for value in frame.fieldOutputs['U'].values:

                    inst = value.instance.name

                    if inst not in instanceResults:
                        instanceResults[inst] = newRecord()

                    r = instanceResults[inst]

                    if value.magnitude > r['maxU']:
                        r['maxU'] = value.magnitude

                    if value.data[0] > r['maxU1']:
                        r['maxU1'] = value.data[0]

                    if value.data[1] > r['maxU2']:
                        r['maxU2'] = value.data[1]

                    if value.data[2] > r['maxU3']:
                        r['maxU3'] = value.data[2]

    for inst in sorted(instanceResults.keys()):

        r = instanceResults[inst]

        results.append([
            file,
            inst,
            r['maxStress'],
            r['maxPrincipalStress'],
            r['maxS11'],
            r['maxS22'],
            r['maxS33'],
            r['maxCE'],
            r['maxCE11'],
            r['maxCE22'],
            r['maxCE33'],
            r['maxPE'],
            r['maxPE11'],
            r['maxPE22'],
            r['maxPE33'],
            r['maxPEEQ'],
            r['maxU'],
            r['maxU1'],
            r['maxU2'],
            r['maxU3']
        ])

    odb.close()

f = open(csvFile, 'wb')
writer = csv.writer(f)
writer.writerows(results)
f.close()

print
print 'All ODB files processed successfully.'
print 'Results saved in:'
print ' ', outputFolder
