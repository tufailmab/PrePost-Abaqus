# -*- coding: mbcs -*-

from abaqus import *
from abaqusConstants import *
import os


# Get current working directory

working_dir = os.getcwd()

print("Current working directory:")
print(working_dir)
print("")

# Output text file

output_file = os.path.join(working_dir, 'IstMode Freq.txt')

out = open(output_file, 'w')

# Header
out.write("ODB_File\tFrequency_Hz\n")

# Find all ODB files in current working directory

odb_files = []

for filename in os.listdir(working_dir):
    if filename.lower().endswith('.odb'):
        odb_files.append(filename)

# Sort alphabetically
odb_files.sort()

# Process each ODB

for filename in odb_files:

    odb_path = os.path.join(working_dir, filename)

    print("Processing: " + filename)

    try:

        # Open ODB
        odb = session.openOdb(name=odb_path)

        # Get step names
        step_names = odb.steps.keys()

        if len(step_names) == 0:
            print("  No steps found.")
            out.write("%s\tNO_STEP\n" % filename)
            odb.close()
            continue

        # Use the first step
        first_step_name = step_names[0]
        step = odb.steps[first_step_name]

        # Get first mode frequency
        #
        # For a Frequency step, the frame frequency is normally
        # stored in frame.frequency.
        #
        # Frame 0 is the initial frame, so we search subsequent
        # frames for the first available frequency.

        first_frequency = None

        for frame in step.frames:

            try:
                frequency = frame.frequency

                if frequency is not None and frequency > 1.0e-12:
                    first_frequency = frequency
                    break

            except:
                pass

        # Write result

        if first_frequency is not None:

            print("  First mode frequency = %s Hz" % first_frequency)

            out.write("%s\t%.10g\n" %
                      (filename, first_frequency))

        else:

            print("  No frequency found.")

            out.write("%s\tNO_FREQUENCY\n" % filename)

        # Close ODB
        odb.close()

    except:

        print("  ERROR while processing " + filename)

        out.write("%s\tERROR\n" % filename)

# Close output file

out.close()


print("")
print("Finished.")
print("Results saved to:")
print(output_file)
