
# Python Script: Combine SummaryStats CSV Files with Folder Name as Header

## Description:
This Python script processes all `summaryStats.csv` files located in subfolders of a specified main folder. It inserts the subfolder name as a new row above each dataset and combines all the data into a single CSV file.

## Steps in the Script:
1. **Prompt for Folder Path**: The script asks the user to input the location of the main folder containing subfolders.
2. **Find CSV Files**: The script looks inside each subfolder for a file named `summaryStats.csv`.
3. **Insert Folder Name**: For each file, it inserts the subfolder's name as a header row above the first row of data.
4. **Combine Data**: It combines all the data into one large dataframe.
5. **Save Output**: The script saves the combined dataframe as a CSV file in a user-specified location.

## Error Handling:
- **Empty Files**: If any `summaryStats.csv` files are empty, a warning is displayed, and the file is skipped.
- **File Read Errors**: If an error occurs while reading a file, the script catches and displays the error without stopping execution.

## Code:
```python
import os
import pandas as pd

def insert_folder_name_as_header(df, folder_name):
    """
    Inserts the folder name as a new header row above the first row of the dataframe.
    """
    folder_row = pd.DataFrame([[folder_name] + [''] * (df.shape[1] - 1)], columns=df.columns)
    df_with_folder = pd.concat([folder_row, df], ignore_index=True)
    return df_with_folder

def process_summary_files(main_folder):
    """
    Processes all 'summaryStats.csv' files in subfolders, 
    inserting the folder name above each dataset and combining them into one dataframe.
    """
    all_data = []

    # Traverse through all subdirectories of the main folder
    for subdir, dirs, files in os.walk(main_folder):
        print(f"Checking folder: {subdir}")  # Debug: Print each folder being checked
        # Look for the summaryStats.csv file in each subfolder
        for file in files:
            if file == "summaryStats.csv":
                file_path = os.path.join(subdir, file)
                print(f"Found file: {file_path}")  # Debug: Print each file found
                try:
                    # Read the CSV file
                    df = pd.read_csv(file_path)
                    if df.empty:
                        print(f"Warning: {file_path} is empty.")  # Warn if the file is empty
                    else:
                        # Get the folder name (last part of the path)
                        folder_name = os.path.basename(subdir)
                        # Insert the folder name as a header row
                        df_with_header = insert_folder_name_as_header(df, folder_name)
                        # Append the modified dataframe to the list
                        all_data.append(df_with_header)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")  # Catch and print any errors reading the file

    # Check if there is any data to concatenate
    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        return combined_data
    else:
        print("No summaryStats.csv files found or all files are empty.")
        return None

# Main execution
if __name__ == "__main__":
    # Prompt the user for the main folder path
    main_folder = input("Please provide the full path to the main folder: ")

    # Process all summaryStats.csv files and combine the data
    combined_data_with_headers = process_summary_files(main_folder)

    if combined_data_with_headers is not None:
        # Prompt the user for a location to save the combined CSV
        output_file = input("Please provide the full path and filename to save the combined CSV: ")
        # Save the combined dataframe to a CSV file
        combined_data_with_headers.to_csv(output_file, index=False)
        print(f"Combined data has been saved to {output_file}.")
    else:
        print("No data to save.")
```

## How to Use:
1. **Run the Script**: Execute the script in your Python environment.
2. **Provide Folder Path**: When prompted, input the path to the main folder containing subfolders with `summaryStats.csv`.
3. **Save Combined CSV**: The script will combine the data and save the output in the specified file location.

## Example Output:
If the main folder contains two subfolders `Subfolder1` and `Subfolder2`, the output will contain the data from both `summaryStats.csv` files with the folder name added as the first row in each section.
