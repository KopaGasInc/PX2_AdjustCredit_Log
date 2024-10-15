import re
import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Function to extract timestamps for specific keywords
def extract_times_from_log(log_file_path, keywords):
    extracted_data = []
    meter_wake_time = None
    meterId = None

    # Try to open and read the log file
    try:
        with open(log_file_path, 'r') as log_file:
            log_lines = log_file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{log_file_path}' not found.")
        return None, None, None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None, None
    
    # Regex pattern to match the timestamp and the log message
    timestamp_pattern = r"\[(\d{2}:\d{2}:\d{2}\.\d{3})\]"
    
    # Iterate over log lines to find matches
    for line in log_lines:
        # Extract meterId
        if "g_meterId" in line:
            meterId_match = re.search(r"g_meterId\s*:\s*(\d+)", line)
            if meterId_match:
                meterId = meterId_match.group(1)

        # Extract timestamp
        timestamp_match = re.search(timestamp_pattern, line)
        if timestamp_match:
            timestamp = timestamp_match.group(1)

            # Check for each keyword and store relevant data
            for keyword, meaning in keywords.items():
                if keyword in line:
                    # Check if it's the meter wake-up time
                    if keyword == "Calling app_main()" and meter_wake_time is None:
                        meter_wake_time = timestamp  # Set the meter wake-up time
                    extracted_data.append({
                        'timestamp': timestamp,
                        'keyword': keyword,
                        'line': line.strip(),
                        'meaning': meaning
                    })
    
    if meter_wake_time is None:
        print("Warning: 'Calling app_main()' (meter wake-up event) not found.")
    
    return extracted_data, meter_wake_time, meterId

# Function to calculate time elapsed since meter wakes up
def calculate_time_elapsed(data, meter_wake_time):
    if meter_wake_time is None:
        print("Warning: Cannot calculate time elapsed without meter wake-up time.")
        return data
    
    try:
        # Convert meter_wake_time to a datetime object
        meter_wake_time_obj = datetime.strptime(meter_wake_time, '%H:%M:%S.%f')
    except ValueError as e:
        print(f"Error parsing meter wake-up time: {e}")
        return data
    
    for entry in data:
        try:
            # Convert event time to a datetime object
            event_time_obj = datetime.strptime(entry['timestamp'], '%H:%M:%S.%f')
            
            # Calculate elapsed time in seconds
            elapsed_time = (event_time_obj - meter_wake_time_obj).total_seconds()
            entry['time_elapsed'] = f"{elapsed_time:.3f}"  # Elapsed time in seconds
        except ValueError as e:
            # If there's a format issue, log it or handle it
            entry['time_elapsed'] = 'N/A'
            print(f"Error parsing timestamp: {entry['timestamp']}, {e}")
    
    return data

# Function to save the extracted data into a CSV file with the specified table format
def save_extracted_data_to_file(extracted_data, meterId, log_file_path, extracted_values):
    # Get log file name (without extension) and directory
    log_file_name = os.path.basename(log_file_path).split('.')[0]
    log_dir = os.path.dirname(log_file_path)

    # File name is a combination of the log file name and meterId
    file_name = f"{log_file_name}_{meterId}_timestamps.csv"
    output_file_path = os.path.join(log_dir, file_name)

    # Define headers for the CSV file
    headers = ['Timestamp', 'Time Elapsed Since Meter Wakes Up', 'Keyword', 'Data in the Line Found', 'Meaning']
    
    try:
        # Write to the CSV file
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Save header info first
            file.write("Header Information:\n")
            writer.writerow(["Keyword", "Meaning", "Value"])
            for keyword, value in extracted_values.items():
                if value:
                    writer.writerow([keyword, value['meaning'], ', '.join(value['data'])])
            file.write("\n\n")

            # Write timestamp data
            writer.writerow(headers)
            for entry in extracted_data:
                writer.writerow([
                    entry['timestamp'],
                    entry.get('time_elapsed', 'N/A'),
                    entry['keyword'],
                    entry['line'],
                    entry['meaning']
                ])
        
        print(f"Data saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving data to file: {e}")
    return output_file_path

# Function to plot the keywords vs relative time
def plot_keywords_vs_time(extracted_data, log_file_path, meterId):
    plt.figure(figsize=(10, 6))
    
    # Now, plot each keyword with its relative time
    for entry in extracted_data:
        if 'time_elapsed' in entry and entry['time_elapsed'] != 'N/A':
            plt.scatter(float(entry['time_elapsed']), entry['keyword'], s=100)

    plt.xlabel('Relative Time (in seconds)')
    plt.title('Keywords vs Relative Time')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot in the same directory as the log file
    log_file_name = os.path.basename(log_file_path).split('.')[0]
    plot_file_name = f"{log_file_name}_{meterId}_plot.png"
    plot_file_path = os.path.join(os.path.dirname(log_file_path), plot_file_name)
    
    try:
        plt.savefig(plot_file_path)
        print(f"Plot saved to {plot_file_path}")
    except Exception as e:
        print(f"Error saving plot: {e}")
    
    plt.show()

# Function to extract values after specific keywords for header information
def extract_values_from_log(log_file_path, keywords):
    extracted_data = {keyword: {"meaning": meaning, "data": []} for keyword, meaning in keywords.items()}

    try:
        with open(log_file_path, 'r') as log_file:
            log_lines = log_file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{log_file_path}' not found.")
        return extracted_data

    # Iterate over log lines to find the keywords and extract their values
    for line in log_lines:
        for keyword in extracted_data:
            if keyword in line:
                # Extract the part of the line after the keyword and store as the value
                value = line.split(keyword)[-1].strip()
                extracted_data[keyword]["data"].append(value)

    return extracted_data

# Updated Keywords and their corresponding meanings
keywords = {
    "Calling app_main()": "Meter Wakes up",
    "get network status": "Attaches to GSM Network",
    "Signal quality": "RSSI measurement",
    "get_clientcert": "Authenticates to Server",
    "aws_Connect": "Opens Protocol (TCP or MQTT)",
    "coreMQTT": "Check for Job via MQTT ACK",
    "aws_Excute_Job": "Meter finishes executing command",
    "aws_Publish": "Send Telemetry Data",
    "aws_Disconnect": "Disconnection from Server",
    "pppos_disc": "Disconnection from GSM Network",
    "into low power!": "Deep Sleep"
}

# Define the keywords you want to search for in the header
header_keywords = {
    "g_meterId": "Meter ID",
    "g_stIccid.iccid_nu": "ICCID",
    "PCB Type": "PCB Type",
    "bat_monitor": "Battery Voltage",
    "get network status": "Net Status"
}

# Ask the user for the log file path
log_file_path = input("Please enter the full path to the log file: ")

# Run the function to extract times and keywords
extracted_times, meter_wake_time, meterId = extract_times_from_log(log_file_path, keywords)

# Extract header values after specific keywords
extracted_values = extract_values_from_log(log_file_path, header_keywords)

# Calculate the time elapsed since meter wakes up
if meter_wake_time:
    extracted_times = calculate_time_elapsed(extracted_times, meter_wake_time)

# Save the extracted data to a CSV file, including the header info
output_file_path = save_extracted_data_to_file(extracted_times, meterId, log_file_path, extracted_values)

# Plot keywords vs relative time and save the plot in the same folder
plot_keywords_vs_time(extracted_times, log_file_path, meterId)
