# Log File Keyword Extraction Script

This Python script extracts timestamps and related log lines based on specific keywords from a log file. It also extracts the `meterId` from the log and saves the output to a file named `<meterId>_keywords.txt`.

## Features
- Extracts timestamps from log lines that match specific keywords.
- Automatically finds the `meterId` from the log file.
- Saves the extracted data to a file named after the `meterId`.

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
