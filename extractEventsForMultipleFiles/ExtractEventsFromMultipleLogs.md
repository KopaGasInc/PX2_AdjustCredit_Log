Log Processing Script

Overview

This script processes multiple log files from a specified folder, extracting important events and timestamps, calculating the time elapsed from a designated "wake-up" event, and summarizing the results. For each log file, the script:

Extracts event timestamps and calculates the time elapsed since the meter wakes up.
Saves the extracted data in a CSV file and generates a visual scatter plot.
Produces a SummaryStats CSV, showing the maximum time elapsed for each event across all log files in the folder.
Features

Multiple Log File Processing: The script processes all .txt files in a specified folder.
Flexible Timestamp Extraction: If the timestamp is not on the same line as the event, the script looks back at previous lines to find it.
Customizable Event Keywords: The script tracks specific keywords (e.g., "cpu_start:", "Signal quality") and associates them with the closest preceding timestamp.
Time Elapsed Calculation: The time elapsed since the meter wake-up event is calculated for each tracked event.
Individual File Outputs: For each log file, the script generates:
A CSV file with the timestamps, time elapsed, event keywords, and descriptions.
A scatter plot showing event keywords against relative time.
Summary Stats CSV: A SummaryStats.csv file is created to show the maximum time elapsed for each event across all log files.
Installation

Requirements:
Python 3.x
matplotlib: For generating plots
csv: Built-in Python module for CSV handling
re: Built-in Python module for regular expressions
To install matplotlib, run:

bash
Copy code
pip install matplotlib
Usage

Place your log files: Ensure that your log files are in .txt format and stored in a folder.
Run the script: The script will ask for the path to the folder containing the log files.
Example Command:
bash
Copy code
python log_processing_script.py
When prompted, enter the path to your folder:

bash
Copy code
Please enter the full path to the folder containing log files: /path/to/logfiles/
Outputs:
For each log file in the folder, the script will generate:
A CSV file with event information (timestamps, time elapsed, keywords).
A plot showing event times relative to the meter wake-up event.
A SummaryStats.csv file will be created in the same folder, summarizing the maximum time elapsed for each event across all files.
Detailed Explanation of Features

1. Timestamp Extraction
The script looks for timestamps using the pattern: "[HH:MM:SS.mmm]".
If a timestamp is not found on the same line as a keyword, the script looks back up to 3 lines to find the most recent timestamp.
2. Event Tracking
The script tracks the following key events (keywords):
cpu_start:: The meter wakes up.
get network status: The device attaches to the GSM network.
Signal quality: RSSI measurement.
get_clientcert: The device authenticates to the server.
aws_Connect: The device opens a protocol (TCP or MQTT).
coreMQTT: The device checks for jobs via MQTT ACK.
aws_Excute_Job: The device finishes executing a command.
aws_Publish: The device sends telemetry data.
aws_Disconnect: The device disconnects from the server.
pppos_disc: The device disconnects from the GSM network.
into low power!: The device enters deep sleep mode.
These keywords can be modified in the script to suit different log formats or events.

3. Time Elapsed Calculation
The time elapsed is calculated based on the timestamp of the cpu_start: event.
Each subsequent event's timestamp is compared with the wake-up time to calculate the time elapsed, which is recorded in seconds.
4. CSV Output
Each log file generates a CSV file with the following columns:
Timestamp: The time of the event.
Time Elapsed Since Meter Wakes Up: The relative time in seconds.
Keyword: The tracked event keyword.
Data in the Line Found: The entire line in which the event was found.
Meaning: A brief description of the event.
5. Plot Generation
A scatter plot is generated for each log file, showing keywords plotted against time elapsed since the meter wake-up event.
6. SummaryStats CSV
A SummaryStats.csv file is generated, which includes one column per log file. The rows represent the keywords, and the cells contain the maximum time elapsed for each keyword in each file.
Example of SummaryStats.csv:

Keyword	log1.txt	log2.txt	log3.txt
cpu_start:	0.000	0.000	0.000
get network status	15.300	14.850	16.200
Signal quality	20.500	19.750	21.000
aws_Disconnect	45.800	44.900	46.500
into low power!	50.300	49.750	51.200
Code Structure

extract_times_from_log: Extracts the timestamps and keywords from the log files, including the "look-back" mechanism for missing timestamps.
calculate_time_elapsed: Calculates the time elapsed from the wake-up event for each keyword.
save_extracted_data_to_file: Saves the extracted data into a CSV file for each log file.
plot_keywords_vs_time: Generates a scatter plot for each log file.
create_summary_stats_for_multiple_files: Creates the SummaryStats.csv file, summarizing the maximum time elapsed for each event across all log files.
process_folder_with_summary: The main function that processes all log files in the folder and generates individual outputs and the summary CSV.
Error Handling

If a log file is missing or cannot be read, an appropriate error message is printed, and the script continues processing the remaining files.
If a timestamp is missing, the script will look back up to 3 lines to find it. If no timestamp is found, the event will be skipped.