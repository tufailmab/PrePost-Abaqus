# GetResults.py (V2)

This project provides a Python script to automate the extraction of results from **multiple Abaqus `.odb` files**. The script scans the current working directory, processes every output database, extracts the required field outputs for each model instance, and consolidates the maximum values into a single **`Results.csv`** file. It is designed to simplify batch post-processing of Abaqus simulations and eliminate the need for manually opening and reviewing individual ODB files.

## Features

* **Batch Processing:** Automatically processes all `.odb` files in the current working directory.
* **Automatic Output Directory:** Creates an **All Required Outputs** folder if it does not already exist.
* **Maximum Value Extraction:** Determines the maximum values across all analysis steps and frames.
* **Supported Field Outputs:**

  * Stress (`S`)
  * Creep Strain (`CE`)
  * Plastic Strain (`PE`)
  * Equivalent Plastic Strain (`PEEQ`)
  * Displacement (`U`)
* **Instance-Based Results:** Stores results separately for every part instance.
* **CSV Export:** Combines all extracted results into a single `Results.csv` file.
* **Robust Processing:** Continues processing even if some field outputs are unavailable.

---

## Usage Instructions

1. Place the **`GetResults.py`** script in the folder containing your Abaqus **`.odb`** files.

2. Run the script using Abaqus Python:

   ```bash
   abaqus cae noGUI=GetResults.py
   ```

3. The script will automatically:

   * Detect all `.odb` files.
   * Create the **All Required Outputs** folder (if required).
   * Process every output database.
   * Extract the maximum values for the supported field outputs.
   * Generate a consolidated **`Results.csv`** file.

---

## Generated Output

The script creates an **All Required Outputs** directory containing:

* **`Results.csv`** – Consolidated results from all processed `.odb` files.

The CSV file contains:

* ODB File Name
* Instance Name
* Maximum von Mises Stress
* Maximum Principal Stress
* Stress Components (`S11`, `S22`, `S33`)
* Creep Strain Components (`CE11`, `CE22`, `CE33`)
* Plastic Strain Components (`PE11`, `PE22`, `PE33`)
* Equivalent Plastic Strain (`PEEQ`)
* Displacement Magnitude
* Displacement Components (`U1`, `U2`, `U3`)

---

## Conceptual Workflow

The following figure presents the conceptual workflow of the **GetResults.py (V2)** script. It illustrates the complete execution sequence, including ODB discovery, field output extraction, maximum value determination, result aggregation, and CSV generation.

<p align="center">
  <img src="Conceptual%20Workflow.png" alt="Conceptual workflow of GetResults.py" width="100%">
</p>

> **Figure:** High-level workflow illustrating the execution sequence of **GetResults.py (V2)**, from initialization and ODB discovery to field extraction, result aggregation, and CSV generation.

---

## Requirements

* Abaqus with Python scripting enabled.
* One or more valid Abaqus `.odb` files.

---

## License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this tool. Please provide appropriate credit if you build upon it.

---

## Developer Info

* **Developer:** Tufail Mabood
* **Contact:** <a href="https://wa.me/+923440907874">WhatsApp</a>
* **Note:** Contributions, suggestions, and improvements are always welcome.
