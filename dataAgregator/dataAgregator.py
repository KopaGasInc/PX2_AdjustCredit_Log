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
    Processes all 'SummaryStats.csv' files in subfolders, 
    inserting the folder name above each dataset and combining them into one dataframe.
    """
    all_data = []

    # Traverse through all subdirectories of the main folder
    for subdir, dirs, files in os.walk(main_folder):
        print(f"Checking folder: {subdir}")  # Debug: Print each folder being checked
        # Look for the SummaryStats.csv file in each subfolder
        for file in files:
            if file == "SummaryStats.csv":
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
        print("No SummaryStats.csv files found or all files are empty.")
        return None

# Main execution
if __name__ == "__main__":
    # Prompt the user for the main folder path
    main_folder = input("Please provide the full path to the main folder: ")

    # Process all SummaryStats.csv files and combine the data
    combined_data_with_headers = process_summary_files(main_folder)

    if combined_data_with_headers is not None:
        # Prompt the user for a location to save the combined CSV
        output_file = input("Please provide the full path and filename to save the combined CSV: ")
        # Save the combined dataframe to a CSV file
        combined_data_with_headers.to_csv(output_file, index=False)
        print(f"Combined data has been saved to {output_file}.")
    else:
        print("No data to save.")
