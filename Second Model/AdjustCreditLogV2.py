import re

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
        if "meterId" in line:
            meterId_match = re.search(r"meterId\s*:\s*(\d+)", line)
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

def save_extracted_data_to_file(extracted_data, meterId):
    # File name based on meterId
    file_name = f"{meterId}_keywords.txt"
    
    # Write to the file
    with open(file_name, 'w') as file:
        for keyword, entries in extracted_data.items():
            if entries:
                file.write(f"Keyword: {keyword}\n")
                for timestamp, line in entries:
                    file.write(f"{timestamp} -> {line}\n")
                file.write("\n")
    
    print(f"Data saved to {file_name}")

# Define the keywords you want to search for
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

# Ask the user for the log file path
log_file_path = input("Please enter the full path to the log file: ")

# Run the function to extract times and meterId
extracted_times, meterId = extract_times_from_log(log_file_path, keywords_to_search)

# Check if the meterId was found
if meterId:
    # Save the extracted data to a file named with meterId
    save_extracted_data_to_file(extracted_times, meterId)
else:
    print("Meter ID not found in the log file.")
