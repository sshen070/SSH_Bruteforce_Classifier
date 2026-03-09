from simple_bruteforce_classifiation import * 
from ssh_feature_engineering import*
from pathlib import Path


def preprocess_data(bruteforce_df):
    # # Basic statistics of dataset
    # Q1 = bruteforce_df['total_conn'].quantile(0.25)
    # Q3 = bruteforce_df['total_conn'].quantile(0.75)
    # IQR = Q3 - Q1

    # upper_bound = Q3 + 1.5 * IQR

    # # Remove any outliers that will skew the clustering towards outliers (number of connections)
    # return bruteforce_df[(bruteforce_df['total_conn'] <= upper_bound)]

    return bruteforce_df[bruteforce_df['total_conn'] < 10000]


def main():

    input_file = input('Enter data file NAME: ')

    # Find input file in repo
    root = Path.cwd().resolve().parent
    
    # Input log file
    input_path = find_conn_log(root, input_file)
    print(f"Using conn.log at: {input_path}")

    bruteforce_data = Path(input_path)

    # Convert json data to Dataframe format
    bruteforce_df = pd.read_json(bruteforce_data)

    user_input = int(input('Preprocess? '))

    if (user_input):
        # Preprocessing (Remove outliers)
        bruteforce_df = preprocess_data(bruteforce_df)

    # Data unchanged (No scaling/PCA) 
    features_df, k_means = original_ssh_activity_classifier(bruteforce_df)
    visualize_ssh_activity(features_df, k_means)

    # Scaled data ~ No PCA
    features_scaled, k_means = ssh_activity_classifier(bruteforce_df)
    visualize_ssh_activity(features_scaled, k_means, True)


if __name__ == "__main__":
    main()
