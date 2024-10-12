import os
import re
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Function to extract specific variables from the log file for the header
def extract_header_info(log_content):
    header_info = {
        "g_meterId": None,
        "g_mAhRemain": None,
        "modemIMEI": None,
        "modemIMSI": None,
        "g_stIccid.iccid_nu": None,
        "PCB Type": None
    }

    # Regex patterns to extract the variable values
    header_patterns = {
        "g_meterId": r"g_meterId\s*:\s*(\d+)",
        "g_mAhRemain": r"g_mAhRemain\s*:\s*(\d+)",
        "modemIMEI": r"modemIMEI\s*:\s*\"(\d+)\"",
        "modemIMSI": r"modemIMSI\s*:\s*\"(\d+)\"",
        "g_stIccid.iccid_nu": r"g_stIccid\.iccid_nu\s*:\s*(\d+)",
        "PCB Type": r"PCB Type is ([A-Z]+ Board!)"
    }

    # Search for these patterns in the log content
    for line in log_content:
        for key, pattern in header_patterns.items():
            match = re.search(pattern, line)
            if match:
                header_info[key] = match.group(1)
    
    return header_info

# Function to extract all timestamps for each step
def extract_timestamps(log_file_path):
    # Define search terms for each step (as lists to handle multiple keywords per step)
    steps_keywords = {
        "Meter Wakes up": [r"DEEPSLEEP_RESET"],
        "Attaches to GSM Network": [r"resetModem", r"get network status"],
        "Opens Protocol (TCP or MQTT)": [r"Modem Connect to PPP Server", r"MQTT ACK"],
        "Authenticates to Server": [r"get_cacert"],
        "Check for Job / Commands": [r"handleIncomePublish.*jobs/get/accepted"],
        "Meter Finishes Executing Command": [r"AdjustCredit"],
        "Send Telemetry Data": [r"aws_Publish.*successed", r"meter-status"],
        "Disconnection from Server": [r"aws_Disconnect"],
        "Disconnection from GSM Network": [r"PPP state changed event 5"],
        "Deep Sleep": [r"into low power"]
    }

    # Reading the log file
    try:
        with open(log_file_path, 'r') as file:
            log_content = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found. Please check the file path and try again.")
        return None, None, None

    # Extract the header information
    header_info = extract_header_info(log_content)

    # Regex to capture timestamps in the format [HH:MM:SS.SSS]
    timestamp_pattern = re.compile(r"\[\d{2}:\d{2}:\d{2}\.\d{3}\]")

    # Dictionary to store the extracted timestamps (as lists to capture multiple matches per step)
    timestamps = {step: [] for step in steps_keywords}
    time_list = []

    # Iterate through log file and find matching entries
    for line in log_content:
        timestamp_match = timestamp_pattern.search(line)
        if timestamp_match:
            timestamp_str = timestamp_match.group(0)
            # Convert to datetime object with milliseconds for time calculation
            timestamp = datetime.strptime(timestamp_str[1:-1], "%H:%M:%S.%f")  # Include milliseconds parsing
            time_list.append(timestamp)
            for step, keywords in steps_keywords.items():
                # Check each keyword for the current step
                for keyword in keywords:
                    if re.search(keyword, line):
                        timestamps[step].append(timestamp)
                        break  # Move to the next step once a keyword is found

    # Return the extracted information
    return header_info, timestamps, time_list

# Function to calculate elapsed time based on timestamps in DataFrame
def calculate_elapsed_time(df):
    first_time = pd.Timestamp(df['Timestamp'].iloc[0])  # Get the first timestamp from the DataFrame
    elapsed_times = [(pd.Timestamp(t) - first_time).total_seconds() for t in df['Timestamp']]
    return elapsed_times

# Function to plot the timestamps
def create_plot(timestamps, output_file):
    plt.figure(figsize=(10, 6))
    
    for event, times in timestamps.items():
        plt.plot(times, [event] * len(times), 'o', label=event)
    
    plt.xlabel("Time")
    plt.ylabel("Event")
    plt.title("Event Timeline")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plot_file = output_file.replace(".csv", ".png")
    plt.savefig(plot_file)
    plt.show()
    print(f"Plot saved to {plot_file}")

# Prompt the user for the log file path
log_file_path = input("Please enter the full path to your log file: ")

# Process the log file
header_info, timestamps, time_list = extract_timestamps(log_file_path)
if timestamps:
    # Prepare DataFrame with multiple entries for each step
    data = [(step, timestamp.strftime("%H:%M:%S")) for step, ts_list in timestamps.items() for timestamp in ts_list]
    timestamps_df = pd.DataFrame(data, columns=['Event', 'Timestamp'])

    # Calculate elapsed time
    elapsed_times = calculate_elapsed_time(timestamps_df)
    timestamps_df['Elapsed Time (s)'] = elapsed_times

    # Display extracted timestamps
    print("\nExtracted Timestamps:")
    print(timestamps_df)

    # Suggest output file path
    suggested_output_file = f"{log_file_path}_output.csv"
    print(f"Suggested output file path: {suggested_output_file}")

    # Optionally save the results to a CSV file with headers
    save_to_csv = input("\nDo you want to save the extracted timestamps to a CSV file? (yes/no): ").strip().lower()
    if save_to_csv == 'yes':
        output_file = input(f"Enter the full path and filename for the output CSV (press Enter to use suggested: {suggested_output_file}): ").strip() or suggested_output_file
        
        # Write to CSV with headers
        with open(output_file, 'w') as f:
            # Write the header info at the top of the CSV file
            f.write("Header Information:\n")
            for key, value in header_info.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")

        # Append the timestamps DataFrame to the CSV
        timestamps_df.to_csv(output_file, mode='a', index=False)
        print(f"Timestamps saved to {output_file}")

        # Create and save the plot
        create_plot(timestamps, output_file)
    else:
        print("Timestamps not saved.")