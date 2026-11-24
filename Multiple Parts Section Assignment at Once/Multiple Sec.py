# Usage Instructions:
# 1. Enter the common prefix of the part names (e.g., Brick for Brick-1, Brick-2, etc.).
# 2. Enter the total number of parts to process, starting from 1.
# 3. Existing section assignments will be deleted and replaced with the specified section.

from abaqusConstants import *
import regionToolset
from abaqus import getInputs

# Ask for user inputs through a dialog
inputs = getInputs(
    fields=(
        ('Part name prefix:', 'Instance Prefix'),
        ('Total number of parts:', 'Number of Instances')
    ),
    label='Section Assignment Settings',
    dialogTitle='Assign Section'
)

# Stop if Cancel is pressed
if inputs is None:
    print 'Operation cancelled.'
else:
    prefix = inputs[0].strip()
    count = int(inputs[1])

    model = mdb.models['Model-1']

    for i in range(1, count + 1):
        partName = '%s-%d' % (prefix, i)

        if partName not in model.parts:
            print 'Skipping: %s (not found)' % partName
            continue

        p = model.parts[partName]

        # Delete previous section assignments
        for j in range(len(p.sectionAssignments) - 1, -1, -1):
            del p.sectionAssignments[j]

        # Assign section
        cells = p.cells.getSequenceFromMask(mask=('[#1 ]',))
        region = regionToolset.Region(cells=cells)

        p.SectionAssignment(
            region=region,
            sectionName='Brick',
            offset=0.0,
            offsetType=MIDDLE_SURFACE,
            offsetField='',
            thicknessAssignment=FROM_SECTION
        )

    mdb.save()
    print 'Section assignment completed successfully!'
