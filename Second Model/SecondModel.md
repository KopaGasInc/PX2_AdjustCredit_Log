# Log File Keyword Extraction Script

This Python script extracts timestamps and related log lines based on specific keywords from a log file. It also extracts the `meterId` from the log and saves the output to a file named `<meterId>_keywords.txt`.

## Features
# Key Features of the Updated Script:

### Flexible Keyword Matching:
Uses case-insensitive matching (re.IGNORECASE) to find keywords regardless of casing.
Trims whitespaces from both the keyword and the log lines to ensure more flexible matching (ignoring accidental spaces).
Configurable Wake-up Event:
The keyword for the meter wake-up event has been updated to "cpu_start:" (previously "Calling app_main()"), and it can be adjusted easily to other keywords if needed.
Time Elapsed Calculation:
Calculates the time elapsed for each event in seconds based on the timestamp of the meter wake-up event (cpu_start:).
Handles errors during timestamp parsing and logs them without breaking the flow of the program.
CSV Output with Header Information:
Extracts values after specific keywords (e.g., g_meterId, g_stIccid.iccid_nu) and saves them as header information in the output CSV file.
Saves each event with its associated timestamp, time elapsed, keyword, and description in the CSV file.
Handling of Repeated Keywords:
Processes multiple occurrences of the same keyword (e.g., multiple "Signal quality" events) and logs each occurrence independently.
Each event is recorded with its own time elapsed and saved to the output CSV.
Plotting Events:
Generates a scatter plot showing the keywords vs relative time elapsed since the meter wake-up event.
Saves the plot in the same directory as the log file, with a filename that includes the meter ID for easy identification.
Robust Error Handling:
Handles common file-related errors such as file not found (FileNotFoundError) and issues with reading or writing to the file.
Logs any timestamp parsing errors and continues processing the log without crashing.

## Requirements
- Python 3.x

## How to Use

1. **Clone or download the script**:
    - Save the script `LogExtract.py` to your local machine.

2. **Run the script**:
    - Open a terminal or command prompt and run the script using Python.

    ```bash
    /usr/bin/python3 LogExtract.py
    ```

3. **Provide the log file path**:
    - When prompted, enter the full path to the log file you want to process. For example:
    
    ```bash
    Please enter the full path to the log file: /path/to/your/logfile.txt
    ```

4. **Keywords and Timestamps**:
    - The script will search for the following keywords in the log file:
        - `Send Ack`
        - `Meter Wakes up`
        - `get network status`
        - `Signal quality`
        - `Authenticates to Server`
        - `aws_Connect`
        - `MQTT ACK`
        - `aws_Excute_Job`
        - `aws_Publish`
        - `aws_Disconnect`
        - `run pppos_disc`
        - `into low power`

5. **Output**:
    - If the `meterId` is found in the log file, the extracted data will be saved to a file named `<meterId>_keywords.txt` in the current working directory.
    - Example of the file name: `24299990040_keywords.txt`.

6. **File Structure**:
    - The file will contain the matched keywords along with their respective timestamps and log lines.

## Example Output

```plaintext
Keyword: Send Ack
[14:15:29.275] -> Send Ack!  // after send ack we now know meter wake up

Keyword: Meter Wakes up
[14:15:29.275] -> Meter wakes up
