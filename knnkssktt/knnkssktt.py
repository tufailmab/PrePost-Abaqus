# Library Installation Guide
# The following Python libraries are required to run this script.
# If they are not already installed in your environment,
# install them using the pip command below:
# pip install numpy pandas openpyxl

import os
import numpy as np
import random
import pandas as pd

# User inputs (Carefully check them)
input_file = "BaseModel.inp"  # your input file in current directory
output_folder = "Generated Files"  # subfolder for new files
os.makedirs(output_folder, exist_ok=True)

num_copies = 5  # number of modified copies you want (For example you want 25 files)

# Define min and max for each cohesive behavior value (This is range of variables)
min_values = [50, 50, 50]           # [KnN_min, Kss_min, Ktt_min]
max_values = [10000, 5000, 5000]    # [KnN_max, Kss_max, Ktt_max]

# Base model name for output files (For example <M>_vi.inp)
base_name = "M"
# User inputs ended here (You don't need to edit something below)

# Generate evenly spaced base values for overall range
# Evenly spaced file is okay to consider (It helps in the detection of parameters)

knn_range = np.linspace(min_values[0], max_values[0], num_copies)
kss_range = np.linspace(min_values[1], max_values[1], num_copies)
ktt_range = np.linspace(min_values[2], max_values[2], num_copies)

# Read the original .inp file (Here Python opens your input_file)
with open(input_file, "r") as f:
    original_lines = f.readlines()

for i in range(num_copies):
    modified_lines = original_lines.copy()

    # Base evenly spaced values for this version
    base_knn = knn_range[i]
    base_kss = kss_range[i]
    base_ktt = ktt_range[i]

    # Track how many cohesive behaviors found
    # This line will make sure no matter how much cohessive behaviour you include
    # - this will handle them, independently.
    cohesive_count = 0

    for j in range(len(modified_lines) - 1):
        
        # This is custom rule i set so that it can edit the updated files
        if modified_lines[j].strip().startswith("*Cohesive Behavior"):
            cohesive_count += 1

            # For each block, make slightly random variations within ±5% range
            knn = random.uniform(base_knn * 0.95, base_knn * 1.05)
            kss = random.uniform(base_kss * 0.95, base_kss * 1.05)
            ktt = random.uniform(base_ktt * 0.95, base_ktt * 1.05)

            # Format the new cohesive values (1 decimal)
            # Abaqus need comma separated, spaced line in input file in keywords
            new_value_line = f"{knn:.1f}, {kss:.1f}, {ktt:.1f}\n"

            # Replace the next line (Using above keyword rules)
            modified_lines[j + 1] = new_value_line

    # Create descriptive filename using base values
    # This line is for your ease so that you recognize the parameters
    new_filename = (
        f"{base_name}_v{i+1}.inp"
    )
    output_path = os.path.join(output_folder, new_filename)

    # Save the modified file
    with open(output_path, "w") as f_out:
        f_out.writelines(modified_lines)

    print(f"Created: {output_path} ({cohesive_count} cohesive behaviors updated)")

print("\nAll files successfully generated in:", os.path.abspath(output_folder))

# Export to Excel

data = []

for i in range(num_copies):
    file_path = os.path.join(output_folder, f"{base_name}_v{i+1}.inp")

    with open(file_path, "r") as f:
        lines = f.readlines()

    cohesive_idx = 0
    for j in range(len(lines) - 1):
        if lines[j].strip().startswith("*Cohesive Behavior"):
            cohesive_idx += 1  # count cohesive blocks in order
            next_line = lines[j + 1].strip()

            # Split properly by commas and convert to float
            try:
                values = [float(x.strip().replace(" ", "").replace(".", ".", 1)) for x in next_line.split(",") if x.strip()]
                if len(values) >= 3:
                    knn, kss, ktt = values[:3]
                    data.append({
                        "File": f"{base_name}_v{i+1}.inp",
                        "Cohesive Block #": cohesive_idx,
                        "KnN": round(knn, 2),
                        "Kss": round(kss, 2),
                        "Ktt": round(ktt, 2)
                    })
            except ValueError:
                # skip malformed lines
                # Your current .inp file doesn't have any malfunctioned lines
                continue

# Convert list to DataFrame
df = pd.DataFrame(data)

# Save to Excel
excel_path = os.path.join(output_folder, "Cohesive Behavior Summary.xlsx")
df.to_excel(excel_path, index=False)

print(f"\nExcel summary saved at: {excel_path}")
print(f"Total cohesive blocks recorded: {len(df)}")


