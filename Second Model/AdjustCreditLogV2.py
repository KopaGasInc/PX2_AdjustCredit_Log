import re
import os
import matplotlib.pyplot as plt

# Function to extract timestamps for specific keywords
def extract_times_from_log(log_file_path, keywords):
    # Open and read the log file
    with open(log_file_path, 'r') as log_file:
        log_lines = log_file.readlines()
    
    # Regex pattern to match the timestamp and the log message
    timestamp_pattern = r"\[\d{2}:\d{2}:\d{2}\.\d{3}\]"
    
    # Store results in a dictionary
    extracted_data = {keyword: [] for keyword in keywords}
    meterId = None
    
    # Iterate over log lines to find matches
    for line in log_lines:
        # Extract meterId
        if "g_meterId" in line:
            meterId_match = re.search(r"g_meterId\s*:\s*(\d+)", line)
            if meterId_match:
                meterId = meterId_match.group(1)

        # Extract keyword-related lines and timestamps
        for keyword in keywords:
            if keyword in line:
                # Extract timestamp
                timestamp_match = re.search(timestamp_pattern, line)
                if timestamp_match:
                    timestamp = timestamp_match.group(0)
                    extracted_data[keyword].append((timestamp, line.strip()))
    
    return extracted_data, meterId

# Function to save the extracted data to a file
def save_extracted_data_to_file(extracted_data, meterId, log_file_path):
    # File name based on meterId, saved in the same directory as the log file
    log_dir = os.path.dirname(log_file_path)
    file_name = f"{meterId}_keywords.txt"
    output_file_path = os.path.join(log_dir, file_name)
    
    # Write to the file
    with open(output_file_path, 'w') as file:
        for keyword, entries in extracted_data.items():
            file.write(f"Keyword: {keyword}\n")
            if entries:
                for timestamp, line in entries:
                    file.write(f"{timestamp} -> {line}\n")
            else:
                file.write("No matches found.\n")
            file.write("\n")
    
    print(f"Data saved to {output_file_path}")

# Function to plot the keywords vs time
def plot_keywords_vs_time(extracted_data):
    plt.figure(figsize=(10, 6))
    
    for keyword, entries in extracted_data.items():
        times = []
        for timestamp, _ in entries:
            # Convert time format [HH:MM:SS.mmm] into seconds for plotting
            time_parts = re.findall(r"\d+", timestamp)
            hours, minutes, seconds, milliseconds = map(int, time_parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
            times.append(total_seconds)
        
        # Plot times for the current keyword
        if times:
            plt.scatter(times, [keyword] * len(times), label=keyword, s=100)

    plt.xlabel('Time (in seconds)')
    plt.title('Keywords vs Time')
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

# Function to extract values after specific keywords
def extract_values_from_log(log_file_path, keywords):
    # Open and read the log file
    with open(log_file_path, 'r') as log_file:
        log_lines = log_file.readlines()
    
    # Dictionary to store the extracted values
    extracted_data = {keyword: [] for keyword in keywords}

    # Iterate over log lines to find the keywords and extract their values
    for line in log_lines:
        for keyword in keywords:
            if keyword in line:
                # Extract the part of the line after the keyword
                value = line.split(keyword)[-1].strip()
                extracted_data[keyword].append(value)

    return extracted_data

# Define the keywords you want to search for (timestamps)
keywords_to_search = [
    "Send Ack", 
    "Meter Wakes up", 
    "get network status", 
    "Signal quality", 
    "Authenticates to Server", 
    "aws_Connect", 
    "MQTT ACK", 
    "aws_Excute_Job", 
    "aws_Publish", 
    "aws_Disconnect", 
    "run pppos_disc", 
    "into low power"
]

# Define the keywords you want to search for (values after keyword)
keywords_to_extract_values = [
    "g_meterId", 
    "g_stIccid.iccid_nu", 
    "PCB Type", 
    "bat_monitor", 
    "get network status", 
    "Signal quality"
]

# Ask the user for the log file path
log_file_path = input("Please enter the full path to the log file: ")

# Run the function to extract times and meterId
extracted_times, meterId = extract_times_from_log(log_file_path, keywords_to_search)

# Check if the meterId was found
if meterId:
    # Save the extracted data to a file named with meterId
    save_extracted_data_to_file(extracted_times, meterId, log_file_path)
    # Plot keywords vs time
    plot_keywords_vs_time(extracted_times)
else:
    print("Meter ID not found in the log file.")

# Extract values after specific keywords
extracted_values = extract_values_from_log(log_file_path, keywords_to_extract_values)

# Display extracted values
print("\nExtracted Values After Specific Keywords:")
for keyword, values in extracted_values.items():
    print(f"Keyword: {keyword}")
    for value in values:
        print(f"Extracted value: {value}")
    print("\n")
