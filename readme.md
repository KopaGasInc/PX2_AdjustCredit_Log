# Log Analysis Script

This Python script processes log files, extracts timestamps for specific events, calculates the time elapsed since the first event, and generates a plot showing the event timeline. It also outputs the results to a CSV file, making it easy to analyze in Excel or other tools.

## Features

- **Friendly Time Output**: Extracts timestamps in an `HH:MM:SS` format, which is suitable for Excel.
- **Elapsed Time Calculation**: Adds a column in the output CSV showing the time elapsed (in seconds) since the first event.
- **Event Timeline Plot**: Generates a scatter plot showing the event timeline as a function of time and saves it as a PNG file.
- **CSV Output**: Exports the extracted timestamps and elapsed time into a CSV file, with additional header information such as `g_meterId`, `modemIMEI`, and more.

## Prerequisites

- Python 3.x
- The following Python packages:
  - `pandas`
  - `matplotlib`

You can install the required packages using pip:

```bash
pip install pandas matplotlib
