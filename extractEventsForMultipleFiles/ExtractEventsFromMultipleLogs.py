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
    last_timestamp = None  # Keep track of the most recent timestamp

    try:
        with open(log_file_path, 'r') as log_file:
            log_lines = log_file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{log_file_path}' not found.")
        return None, None, None

    timestamp_pattern = r"\[(\d{2}:\d{2}:\d{2}\.\d{3})\]"
    
    # Iterate over log lines
    for i, line in enumerate(log_lines):
        # Check if the line contains a timestamp
        timestamp_match = re.search(timestamp_pattern, line)
        if timestamp_match:
            last_timestamp = timestamp_match.group(1)  # Update the last known timestamp

        # Now look for keywords
        for keyword, meaning in keywords.items():
            if re.search(re.escape(keyword.strip()), line.strip(), re.IGNORECASE):
                # If no timestamp found in this line, look back at previous lines
                if not last_timestamp:
                    for j in range(1, 4):  # Look back up to 3 lines
                        if i - j >= 0:  # Ensure index stays valid
                            previous_line = log_lines[i - j]
                            timestamp_match = re.search(timestamp_pattern, previous_line)
                            if timestamp_match:
                                last_timestamp = timestamp_match.group(1)
                                break

                if last_timestamp:
                    if keyword.lower() == "cpu_start:".lower() and meter_wake_time is None:
                        meter_wake_time = last_timestamp  # Set the meter wake-up time

                    extracted_data.append({
                        'timestamp': last_timestamp,
                        'keyword': keyword,
                        'line': line.strip(),
                        'meaning': meaning
                    })
                last_timestamp = None  # Reset the last timestamp after use

    if meter_wake_time is None:
        print("Warning: 'cpu_start:' (meter wake-up event) not found.")
    
    return extracted_data, meter_wake_time, meterId

# Function to calculate time elapsed since meter wakes up
def calculate_time_elapsed(data, meter_wake_time):
    if meter_wake_time is None:
        print("Warning: Cannot calculate time elapsed without meter wake-up time.")
        return data
    
    try:
        meter_wake_time_obj = datetime.strptime(meter_wake_time, '%H:%M:%S.%f')
    except ValueError as e:
        print(f"Error parsing meter wake-up time: {e}")
        return data
    
    for entry in data:
        try:
            event_time_obj = datetime.strptime(entry['timestamp'], '%H:%M:%S.%f')
            elapsed_time = (event_time_obj - meter_wake_time_obj).total_seconds()
            entry['time_elapsed'] = f"{elapsed_time:.3f}"
        except ValueError as e:
            entry['time_elapsed'] = 'N/A'
            print(f"Error parsing timestamp: {entry['timestamp']}, {e}")
    
    return data

# Function to save the extracted data into a CSV file with the specified table format
def save_extracted_data_to_file(extracted_data, meterId, log_file_path, extracted_values):
    log_file_name = os.path.basename(log_file_path).split('.')[0]
    log_dir = os.path.dirname(log_file_path)

    file_name = f"{log_file_name}_{meterId}_timestamps.csv"
    output_file_path = os.path.join(log_dir, file_name)

    headers = ['Timestamp', 'Time Elapsed Since Meter Wakes Up', 'Keyword', 'Data in the Line Found', 'Meaning']
    
    try:
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            file.write("Header Information:\n")
            writer.writerow(["Keyword", "Meaning", "Value"])
            for keyword, value in extracted_values.items():
                if value:
                    writer.writerow([keyword, value['meaning'], ', '.join(value['data'])])
            file.write("\n\n")
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
    
    for entry in extracted_data:
        if 'time_elapsed' in entry and entry['time_elapsed'] != 'N/A':
            plt.scatter(float(entry['time_elapsed']), entry['keyword'], s=100)

    plt.xlabel('Relative Time (in seconds)')
    plt.title('Keywords vs Relative Time')
    plt.grid(True)
    plt.tight_layout()

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

    for line in log_lines:
        for keyword in extracted_data:
            if re.search(re.escape(keyword.strip()), line.strip(), re.IGNORECASE):
                value = line.split(keyword)[-1].strip()
                extracted_data[keyword]["data"].append(value)

    return extracted_data

# Function to create a summary table for multiple files
def create_summary_stats_for_multiple_files(all_files_data, keywords, output_file_path):
    summary_data = {keyword: [] for keyword in keywords}
    
    # Collect the maximum time elapsed for each keyword from each file
    for file_name, extracted_data in all_files_data.items():
        file_summary = {}
        for entry in extracted_data:
            keyword = entry['keyword']
            if 'time_elapsed' in entry and entry['time_elapsed'] != 'N/A':
                elapsed_time = float(entry['time_elapsed'])
                if keyword not in file_summary or elapsed_time > file_summary[keyword]:
                    file_summary[keyword] = elapsed_time
        # Add max times for each keyword into the summary_data
        for keyword in summary_data:
            summary_data[keyword].append(file_summary.get(keyword, 'N/A'))
    
    # Write the summary table to CSV
    summary_file_path = os.path.join(output_file_path, "SummaryStats.csv")
    
    try:
        with open(summary_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(['Keyword'] + [file_name for file_name in all_files_data.keys()])
            # Write each keyword and its max times for each file
            for keyword, times in summary_data.items():
                writer.writerow([keyword] + times)
        
        print(f"Summary saved to {summary_file_path}")
    except Exception as e:
        print(f"Error saving summary to file: {e}")

# Function to process multiple log files in a folder and create a summary
def process_folder_with_summary(folder_path, keywords, header_keywords):
    all_files_data = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):  # Assuming log files are in .txt format
            log_file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_name}")
            
            # Extract times and keywords from the log file
            extracted_times, meter_wake_time, meterId = extract_times_from_log(log_file_path, keywords)

            # Extract header values
            extracted_values = extract_values_from_log(log_file_path, header_keywords)

            # Calculate the time elapsed since meter wakes up
            if meter_wake_time:
                extracted_times = calculate_time_elapsed(extracted_times, meter_wake_time)

            # Save the extracted data for this file
            all_files_data[file_name] = extracted_times

            # Save individual CSV and plot for each file
            save_extracted_data_to_file(extracted_times, meterId, log_file_path, extracted_values)
            plot_keywords_vs_time(extracted_times, log_file_path, meterId)

    # Create and save the summary stats for all files
    create_summary_stats_for_multiple_files(all_files_data, keywords, folder_path)

# Keywords for event tracking and headers
keywords = {
    "cpu_start:": "Meter Wakes up",
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

header_keywords = {
    "g_meterId": "Meter ID",
    "g_stIccid.iccid_nu": "ICCID",
    "PCB Type": "PCB Type",
    "bat_monitor": "Battery Voltage",
    "get network status": "Net Status"
}

# Ask for folder path
folder_path = input("Please enter the full path to the folder containing log files: ")

# Run the process for all log files in the folder
process_folder_with_summary(folder_path, keywords, header_keywords)
