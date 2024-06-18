# Description: command line python script to update existing dataframe using match point of 1st column, updating any existing rows and then adding any new rows and finally deduplicating before writing out updated dataframe
import pandas as pd
import sys
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <old_file> <new_file>")
        sys.exit(1)
    
    old_file = sys.argv[1]
    new_file = sys.argv[2]

    old_delimiter = input(f"Please enter the delimiter for the file {old_file}: ")
    new_delimiter = input(f"Please enter the delimiter for the file {new_file}: ")

    try:
        oldDF = pd.read_csv(old_file, delimiter=old_delimiter, dtype=str, encoding='utf-8')
        newDF = pd.read_csv(new_file, delimiter=new_delimiter, dtype=str, encoding='utf-8')
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)

    # Set the first column as the index for both DataFrames for easy updating
    oldDF.set_index(oldDF.columns[0], inplace=True)
    newDF.set_index(newDF.columns[0], inplace=True)

    # Update oldDF with newDF
    oldDF.update(newDF)

    # Concatenate oldDF and newDF to add new rows
    combinedDF = pd.concat([oldDF, newDF])

    # Drop duplicates, keeping the last occurrence (from newDF)
    combinedDF = combinedDF[~combinedDF.index.duplicated(keep='last')]

    # Reset index to restore the first column as a normal column
    combinedDF.reset_index(inplace=True)

    # Write updated DataFrame to a new file with the correct extension
    output_file = os.path.splitext(old_file)[0] + '-updated' + os.path.splitext(old_file)[1]
    combinedDF.to_csv(output_file, sep=old_delimiter, index=False, encoding='utf-8')
    print(f"Updated file has been written to {output_file}")

if __name__ == "__main__":
    main()
