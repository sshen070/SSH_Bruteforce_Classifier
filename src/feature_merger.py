from ssh_feature_engineering import find_conn_log

import pandas as pd
from pathlib import Path
from functools import reduce

def merge_features(files_arr):
    dfs = []

    seen_total_conn = False
    for file in files_arr:
        df = pd.read_json(file)

        # Drop 'total_conn' if we've already seen it --> Remove duplicates
        if seen_total_conn and "total_conn" in df.columns:
            df = df.drop(columns=["total_conn"])
        elif "total_conn" in df.columns:
            # Keep total_conn from first occurance
            seen_total_conn = True

        dfs.append(df)

    # Merge all DataFrames on 'ip'
    merged_df = reduce(lambda left, right: pd.merge(left, right, on="ip", how="outer"), dfs)

    # Fill missing values with 0
    merged_df.fillna(0, inplace=True)

    # Sort by conn_fail_ratio
    merged_df = merged_df.sort_values(by="conn_fail_ratio", ascending=False)
    return merged_df


def main():
    num_files = int(input("How many JSON files to merge? "))
    try:
        files_arr = []
        root = Path.cwd().resolve().parent  # root to search for files

        for i in range(num_files):
            filename = input(f"Enter name of file {i+1}: ")
            file_path = find_conn_log(root, filename)
            print(f"Using file: {file_path}")
            files_arr.append(file_path)

        # Merge the feature files
        merged_df = merge_features(files_arr)

        # Ask user for output file names
        output_json = input("Enter name for output JSON file: ")
        output_path = Path('../data/ip_bruteforce_summary_logs') / output_json

        # Save merged dataset
        merged_df.to_json(output_path, orient="records", indent=2)

        print(f"Merged dataset written to:\n- JSON: {output_json}")
        print(f"Generated {len(merged_df.columns)-1} features for {len(merged_df)} IPs.")

    except:
        print("File name invalid.")


if __name__ == "__main__":
    main()