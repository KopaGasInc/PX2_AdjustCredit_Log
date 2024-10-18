# Energy (DC Current and DC Voltage) Data Analysis Script

This Python script analyzes DC Current and DC Voltage data from Excel files, calculates power consumption in Watts (W) and energy consumption in Watt-hours (Wh), and generates plots for visualization. The results are saved in an Excel file, and plots are displayed.

## Features

- **Data Cleaning and Merging**: Merges DC Current and DC Voltage data based on the `Time` column.
- **Power and Energy Calculations**: Computes power consumption (W) and energy consumption (Wh).
- **Plotting**: 
  - DC Current and DC Voltage over time.
  - Power over time.
  - Energy consumption over time.
- **Output File**: Merged data saved in an Excel file (`merged_current_voltage_data.xlsx`).

## Prerequisites

Before running the script, ensure that you have the following:

- **Python 3.x**
- Required Python packages:
  - `pandas`
  - `matplotlib`
  - `openpyxl`

You can install the required packages using the following command:

```bash
pip install pandas matplotlib openpyxl




.
├── dc_analysis_auto.py    # Main Python script for analysis
├── README.md              # This readme file
└── /Power test            # Directory containing Excel files for current and voltage data
    ├── 24299990034 current test.xlsx
    └── 24299990030 voltage test.xlsx
Running the Script

To run the script, follow these steps:

Place your DC Current and DC Voltage Excel files in a folder. The script will automatically detect files with "current" and "voltage" in their filenames.
Open a terminal and navigate to the directory containing the script (dc_analysis_auto.py).
Run the script:
bash
Copy code
python dc_analysis_auto.py
The script will prompt you to enter the path of the directory containing the Excel files for DC Current and DC Voltage.
Example:

bash
Copy code
Please enter the directory path where the DC Current and DC Voltage files are located: /path/to/your/excel/files
After running, the following output files will be generated in the same directory:
Plots: PNG images for DC Current/Voltage and Energy Consumption will be saved in the plots/ subfolder.
Total Energy: A text file named total_energy.txt will contain the total energy consumption in Wh.
Merged Data: The merged data (including power and energy calculations) will be saved as merged_current_voltage_data.xlsx.
Output

Excel File (merged_current_voltage_data.xlsx):
Contains the merged data of DC Current and DC Voltage with computed Power (W) and Energy (Wh).
Plots (saved as PNG files in the plots subfolder):
current_voltage_plot.png: DC Current and DC Voltage over time.
energy_consumption_plot.png: Energy consumption over time.
Text File (total_energy.txt):
Contains the total energy consumption in Wh for the entire dataset.
Example of total_energy.txt:
txt
Copy code
Total Energy Consumption (Wh): 12.34
Example Output Files

Here’s a sample structure of the output after running the script:

bash
Copy code
.
├── merged_current_voltage_data.xlsx  # Merged data with power and energy
├── total_energy.txt                  # Total energy consumption (Wh)
├── /plots                            # Subfolder containing plots
    ├── current_voltage_plot.png      # Plot for DC Current and Voltage
    └── energy_consumption_plot.png   # Plot for Energy Consumption
Customization

File Names: You can customize the names of the output files by modifying the relevant sections in the script.
Plot Directory: By default, plots are saved in the plots/ subfolder. You can change this directory by modifying the plot_dir in the script.
License

