
# Log Processing Script Documentation

## Overview
This script processes log files, extracts specific header information, and captures timestamps for various events that occur during the operation of a device (such as a smart meter). It then calculates the elapsed time for each event and offers the ability to save these results to a CSV file. Additionally, the script generates a plot that visualizes the event timeline.

## Functions

### 1. `extract_header_info(log_content)`
- **Purpose**: Extracts key header information such as the meter ID, remaining battery, and modem details from the log file.
- **Parameters**: 
  - `log_content`: The content of the log file (list of lines).
- **Returns**: 
  - A dictionary containing the extracted header information.

- **Header Information Extracted**:
  - `g_meterId`: The meter's ID.
  - `g_mAhRemain`: The remaining battery capacity in mAh.
  - `modemIMEI`: The modem's IMEI number.
  - `modemIMSI`: The modem's IMSI number.
  - `g_stIccid.iccid_nu`: The ICCID number.
  - `PCB Type`: The type of PCB board.

### 2. `extract_timestamps(log_file_path)`
- **Purpose**: Reads the log file and extracts timestamps for specific events based on pre-defined keywords. It also extracts the header information from the file.
- **Parameters**: 
  - `log_file_path`: The full path to the log file.
- **Returns**: 
  - A dictionary containing the header information.
  - A dictionary containing timestamps for each event.
  - A list of all timestamps present in the log.

### 3. `calculate_elapsed_time(df)`
- **Purpose**: Calculates the elapsed time (in seconds) from the first timestamp for each event.
- **Parameters**: 
  - `df`: A pandas DataFrame containing the timestamps.
- **Returns**: 
  - A list of elapsed times in seconds.

### 4. `create_plot(timestamps, output_file)`
- **Purpose**: Plots the extracted timestamps for each event and saves the plot as a PNG file.
- **Parameters**:
  - `timestamps`: A dictionary of events and their corresponding timestamps.
  - `output_file`: The file path where the plot will be saved.

## Usage Instructions
1. **Input the Log File Path**: 
   When running the script, you will be prompted to enter the full path to your log file.
   
2. **Extract Header Information and Timestamps**: 
   The script will automatically extract the header information and the timestamps for key events.

3. **View Extracted Information**: 
   You can view the extracted timestamps, and you will be offered the option to save the data to a CSV file.

4. **Save Data**:
   If you choose to save the data, the script will prompt you for the output file path. You can either provide a custom path or use the suggested path.

5. **Plot Timeline**:
   The script will automatically generate a timeline plot of the events and save it as a PNG file in the same directory as the CSV output file.

## Example
```bash
Please enter the full path to your log file: /path/to/logfile.log

Do you want to save the extracted timestamps to a CSV file? (yes/no): yes
Enter the full path and filename for the output CSV (press Enter to use suggested: /path/to/logfile.log_output.csv): 
```

The timestamps and header information will be saved to the specified CSV file, and the plot will be generated and saved as a PNG file.

## Dependencies
- `pandas`
- `matplotlib`
- `re`
- `datetime`

Make sure these libraries are installed before running the script.

## Error Handling
- **File Not Found**: If the log file is not found, an error message is printed.
- **Missing Data**: If a particular event is not found in the log, it will not appear in the output. You can add more keywords to the search if needed.

