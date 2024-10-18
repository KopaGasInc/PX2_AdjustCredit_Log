import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import os

# Load and clean data from Excel
# Load and clean data from Excel with dynamic sheet selection
def load_and_clean_data(file_path, default_sheet='Sheet4', backup_sheet='Sheet5', column_to_keep=['Time', 'DC Current']):
    print(f"Loading file: {file_path}")

    # Check available sheets
    available_sheets = pd.ExcelFile(file_path, engine='openpyxl').sheet_names
    print(f"Available sheets in file: {available_sheets}")

    # If Sheet5 is available, use it; otherwise, default to Sheet4
    if backup_sheet in available_sheets:
        sheet_to_use = backup_sheet
        print(f"Sheet '{backup_sheet}' found, using it.")
    elif default_sheet in available_sheets:
        sheet_to_use = default_sheet
        print(f"Sheet '{backup_sheet}' not found, using '{default_sheet}' instead.")
    else:
        # If neither sheet is found, raise an error
        raise ValueError(f"Neither '{default_sheet}' nor '{backup_sheet}' found in the file. Available sheets: {available_sheets}")

    # Load the Excel file from the appropriate sheet
    data = pd.read_excel(file_path, sheet_name=sheet_to_use, engine='openpyxl')

    # Print the column names to verify
    print("Columns available in the file:", data.columns)

    # Dynamically adjust the columns based on what exists
    if 'DC Current' not in data.columns:
        if 'DC Voltage' in data.columns:
            print("Warning: Expected 'DC Current' column not found, using 'DC Voltage' instead.")
            column_to_keep = ['Time', 'DC Voltage']  # Adjust columns if only 'DC Voltage' is present
        else:
            raise KeyError(f"Neither 'DC Current' nor 'DC Voltage' found in the file. Available columns: {data.columns}")

    # Keep only the relevant columns
    cleaned_data = data[column_to_keep].copy()

    # Convert 'Time' column to datetime format
    cleaned_data.loc[:, 'Time'] = pd.to_datetime(cleaned_data['Time'], errors='coerce', format='%H:%M:%S:%f')

    # Drop rows where Time or the key column is NaN
    cleaned_data = cleaned_data.dropna(subset=['Time', column_to_keep[1]])

    print(f"Data loaded and cleaned: {cleaned_data.shape[0]} rows")
    return cleaned_data

# Function to detect outliers in DC Current and Voltage using the interquartile range (IQR)
def detect_outliers(merged_data):
    print("Detecting outliers in DC Current and DC Voltage...")
    
    outliers = {}
    
    # Define a function to compute IQR and detect outliers
    def find_outliers(data, column):
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return data[(data[column] < lower_bound) | (data[column] > upper_bound)]

    outliers['DC Current'] = find_outliers(merged_data, 'DC Current')
    outliers['DC Voltage'] = find_outliers(merged_data, 'DC Voltage')

    total_outliers = len(outliers['DC Current']) + len(outliers['DC Voltage'])
    print(f"Total outliers found: {total_outliers}")

    return outliers

# Plot DC Current and DC Voltage over time and save the plot
def plot_dc_current_and_voltage(merged_data, plot_dir):
    print("Plotting DC Current and DC Voltage over Time...")
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot DC Voltage on the primary y-axis
    ax1.set_xlabel('Time', fontsize=14)
    ax1.set_ylabel('DC Voltage (V)', color='green', fontsize=14)
    ax1.plot(merged_data['Time'], merged_data['DC Voltage'], color='green', label='DC Voltage')
    ax1.tick_params(axis='y', labelcolor='green')

    # Create a secondary y-axis for DC Current
    ax2 = ax1.twinx()
    ax2.set_ylabel('DC Current (A)', color='blue', fontsize=14)
    ax2.plot(merged_data['Time'], merged_data['DC Current'], color='blue', label='DC Current')
    ax2.tick_params(axis='y', labelcolor='blue')

    plt.title('DC Current and DC Voltage Over Time', fontsize=16)
    fig.tight_layout()
    plt.grid(True)
    
    # Save the plot as an image
    plot_file = os.path.join(plot_dir, 'current_voltage_plot.png')
    plt.savefig(plot_file)  # Save the plot as a PNG file
    plt.close()  # Close the plot to free memory
    print(f"DC Current and Voltage plot saved to: {plot_file}")

# Calculate power in watts and save the plot
def calculate_power(merged_data, plot_dir):
    print("Calculating Power (W)...")
    # Multiply DC Current and DC Voltage to get power in Watts (W)
    merged_data['Power (W)'] = merged_data['DC Current'] * merged_data['DC Voltage']

    plt.figure(figsize=(12, 6))
    plt.plot(merged_data['Time'], merged_data['Power (W)'], color='purple', label='Power (W)')
    plt.title('Power (W) Over Time', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Power (W)', fontsize=14)
    plt.grid(True)
    
    # Save the plot as an image
    plot_file = os.path.join(plot_dir, 'power_plot.png')
    plt.savefig(plot_file)  # Save the plot as a PNG file
    plt.close()  # Close the plot
    print(f"Power plot saved to: {plot_file}")

# Apply forward and backward filling to handle remaining NaN values
def fill_missing_values(data, column):
    # First, apply forward fill
    data[column] = data[column].fillna(method='ffill')
    # Then, apply backward fill for any remaining NaN values
    data[column] = data[column].fillna(method='bfill')
    
    return data

def calculate_total_energy(merged_data, plot_dir):
    print("Calculating total energy consumption in Wh...")
    if not pd.api.types.is_datetime64_any_dtype(merged_data['Time']):
        merged_data['Time'] = pd.to_datetime(merged_data['Time'], errors='coerce')

    # Calculate the time delta in hours between consecutive measurements
    merged_data['Delta Time (h)'] = (merged_data['Time'] - merged_data['Time'].shift()).dt.total_seconds() / 3600

    # Safely fill missing Delta Time values with 0
    merged_data['Delta Time (h)'] = merged_data['Delta Time (h)'].fillna(0)

    # Calculate energy in Wh by multiplying Power (W) with Delta Time (h)
    merged_data['Energy (Wh)'] = merged_data['Power (W)'] * merged_data['Delta Time (h)']
    
    total_energy_Wh = merged_data['Energy (Wh)'].sum()
    print(f"Total Energy Consumption for the whole file: {total_energy_Wh} Wh")

    # Plot energy over time
    plt.figure(figsize=(10, 6))
    plt.plot(merged_data['Time'], merged_data['Energy (Wh)'], color='purple')
    plt.title('Time vs Energy Consumption (Wh)', fontsize=16)
    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Energy (Wh)', fontsize=14)
    plt.grid(True)

    # Save the energy consumption plot as an image
    plot_file = os.path.join(plot_dir, 'energy_consumption_plot.png')
    plt.savefig(plot_file)  # Save the plot as a PNG file
    plt.close()  # Close the plot
    print(f"Energy plot saved to: {plot_file}")
    return total_energy_Wh, merged_data.shape[0]

# Save the merged data to an Excel file
def save_merged_data_to_excel(merged_data, output_file='merged_current_voltage_data.xlsx'):
    print(f"Saving merged data to {output_file}...")
    try:
        # Ensure that Delta Time and Energy columns are included
        merged_data.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Merged data successfully saved to {output_file}")
    except Exception as e:
        print(f"Failed to save merged data to {output_file}. Error: {e}")

# Find the current and voltage files in the specified directory
def find_files_in_directory(directory):
    current_file = None
    voltage_file = None

    # Scan the directory for Excel files
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(directory, filename)
            if 'current' in filename.lower():
                current_file = file_path
            elif 'voltage' in filename.lower():
                voltage_file = file_path

    return current_file, voltage_file

# Function to detect outliers in DC Current and Voltage using the interquartile range (IQR)
def detect_outliers(merged_data):
    print("Detecting outliers in DC Current and DC Voltage...")
    
    outliers = {}
    
    # Define a function to compute IQR and detect outliers
    def find_outliers(data, column):
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return data[(data[column] < lower_bound) | (data[column] > upper_bound)]

    # Detect outliers in 'DC Current' and 'DC Voltage' columns
    outliers['DC Current'] = find_outliers(merged_data, 'DC Current')
    outliers['DC Voltage'] = find_outliers(merged_data, 'DC Voltage')

    # Print out the total number of outliers detected
    total_outliers = len(outliers['DC Current']) + len(outliers['DC Voltage'])
    print(f"Total outliers found: {total_outliers}")

    return outliers
  
# Function to save statistics to a file
def save_statistics(total_energy_Wh, num_merged_rows, outliers, output_file='energy_stats.txt'):
    print(f"Saving statistics to {output_file}...")

    try:
        with open(output_file, 'w') as f:
            f.write(f"Total Energy Consumption (Wh): {total_energy_Wh}\n")
            f.write(f"Number of Merged Rows: {num_merged_rows}\n")
            f.write(f"Outliers in DC Current: {len(outliers['DC Current'])}\n")
            f.write(f"Outliers in DC Voltage: {len(outliers['DC Voltage'])}\n")
        
        print(f"Statistics successfully saved to {output_file}")
    except Exception as e:
        print(f"Failed to save statistics. Error: {e}")

# Main function to run the steps
def main():
    dir_path = input("Please enter the directory path where the DC Current and DC Voltage files are located: ")

    while not os.path.isdir(dir_path):
        print(f"The directory '{dir_path}' does not exist. Please try again.")
        dir_path = input("Please enter the directory path where the DC Current and DC Voltage files are located: ")

    current_file, voltage_file = find_files_in_directory(dir_path)

    if not current_file or not voltage_file:
        print("Could not find both the DC Current and DC Voltage files in the directory.")
        return

    print(f"DC Current file: {current_file}")
    print(f"DC Voltage file: {voltage_file}")

    current_data = load_and_clean_data(current_file, column_to_keep=['Time', 'DC Current'])
    voltage_data = load_and_clean_data(voltage_file, column_to_keep=['Time', 'DC Voltage'])

    merged_data = pd.merge(current_data, voltage_data, on='Time', how='inner')

    # Interpolate missing values in the DC Voltage column
    merged_data['DC Voltage'] = merged_data['DC Voltage'].interpolate(method='polynomial', order=2)

    # Apply forward and backward filling to handle remaining NaN values
    merged_data = fill_missing_values(merged_data, 'DC Voltage')

    # Optionally, drop any rows that still have NaN values
    merged_data = merged_data.dropna()

    # Define the subfolder for saving plots
    plot_dir = os.path.join(dir_path, 'plots')
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    # Plot DC Current and DC Voltage and save the plot
    plot_dc_current_and_voltage(merged_data, plot_dir)

    # Calculate power and save the plot
    calculate_power(merged_data, plot_dir)

    # Calculate total energy and save the plot, return total energy and number of merged rows
    total_energy_Wh, num_merged_rows = calculate_total_energy(merged_data, plot_dir)

    # Detect outliers
    outliers = detect_outliers(merged_data)

    # Save the statistics, including total energy, merged rows, and outlier information
    stats_file = os.path.join(dir_path, 'energy_stats.txt')
    save_statistics(total_energy_Wh, num_merged_rows, outliers, stats_file)

    # Save merged data with Energy (Wh) and Delta Time (h)
    output_file = os.path.join(dir_path, 'merged_current_voltage_data.xlsx')
    save_merged_data_to_excel(merged_data, output_file)

if __name__ == '__main__':
    main()

#examples more 