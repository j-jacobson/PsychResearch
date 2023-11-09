#! /usr/bin/python3

import os, sys, re
import glob
import pandas as pd

def merge_csv_files(folder_path):
    """ Merge the CSV files
    param: folder_path: The path to the folder holding the .csv files.
    returns: A pandas DataFrame holding all of the data. """
    
    # Get a list of all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    # Initialize an empty DataFrame to store the merged data
    merged_df = pd.DataFrame()

    # Merge all CSV files into one DataFrame
    for idx, file in enumerate(csv_files):
      df = pd.read_csv(file)

      # Exclude the second row from each CSV file after the first
      if idx == 0:
        merged_df = pd.concat([merged_df, df.iloc[:1]], ignore_index=True)
      
      df = df.iloc[1:]

      # Define the regular expression pattern
      pattern = r'(^\d+)[_\s]'
      # Extract value from the filename using regular expressions
      match = re.search(pattern, os.path.basename(file))
      if match:
        df['ID'] = match.group(1)

      # Exclude rows based on a specific response in the 'ResponseColumn'
      df = df.loc[df['Finished'] != 'False']

      # Extract only the numeric part from columns not matching certain patterns
      excluded_cases = ['RecordedDate', 'Duration (in seconds)', 'ID']

      # Modify the regex pattern to exclude the specified cases
      pattern = f'^(?!(?:{"|".join(re.escape(case) for case in excluded_cases)}))'

      # Extract only the numeric part from columns matching the modified pattern
      for col in df.filter(regex=pattern).columns:
        temp = df[col].str.extract(r'(\d+)', expand=False)
        # Check if the column contains numeric values
        if temp.notnull().all():
          df[col] = temp.astype(int)
        else:
          # Substitute text values with corresponding numbers
          df[col].replace({'A great deal': 5,
                           'A lot': 4,
                           'Often': 4,
                           'A fair amount': 3, 
                           'Occasionally': 3,
                           'A little': 2,
                           'Once or twice': 2,
                           'None': 1,
                           'Not at all': 1
                           }, inplace=True)

      merged_df = pd.concat([merged_df, df], ignore_index=True)
    return merged_df

def remove_columns(df, columns_to_remove):
    # Remove specified columns
    df = df.drop(columns=columns_to_remove, errors='ignore')
    return df

def create_2d_table(df, excel_filename='output/output.xlsx'):
    # Display the 2D table
    print(df)

    # Save the DataFrame to an Excel file with the 'xlsxwriter' engine
    df.to_excel(excel_filename, index=False, engine='xlsxwriter')
    print(f"Data saved to {excel_filename}")

def reorganize_columns(df):
  # Reorganize columns with ID first, followed by specific columns, Qs, ValueFromFilename, IsFirstFile, and then other columns
  # Extract the numeric part and sort Qs in numerical order
  sorted_q_cols = sorted([col for col in df.columns if col.startswith('Q')], key=lambda x: int(re.search(r'\d+', x).group()))

  # Reorganize columns with ID first, followed by specific columns, sorted Qs, ValueFromFilename, IsFirstFile, and then other columns
  cols = ['ID', 'RecordedDate', 'Duration (in seconds)'] + sorted_q_cols + [col for col in df.columns if not (col.startswith('Q') or col.startswith('Attention')) and col not in ['ID', 'RecordedDate', 'Duration (in seconds)']] + [col for col in df.columns if col.startswith('Attention')]
  df = df[cols]

  return df

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python3 formatter.py <folder_path>")
        sys.exit(1)

    # Get folder path from command-line arguments
    folder_path = sys.argv[1]

    # Merge CSV files in the folder
    merged_data = merge_csv_files(folder_path)

    # Reorganize columns
    merged_data = reorganize_columns(merged_data)

    # Remove specific columns
    columns_to_remove = ['StartDate', 
                         'EndDate', 
                         'Status', 
                         'IPAddress', 
                         'Progress', 
                         'ResponseId', 
                         'RecipientLastName',
                         'RecipientFirstName',
                         'RecipientEmail',
                         'ExternalReference',
                         'LocationLatitude',
                         'LocationLongitude',
                         'DistributionChannel',
                         'UserLanguage',
                         'Finished', # We already excluded ones where they didn't finish
                         ]

    merged_data = remove_columns(merged_data, columns_to_remove)

    # Display the 2D table
    create_2d_table(merged_data)