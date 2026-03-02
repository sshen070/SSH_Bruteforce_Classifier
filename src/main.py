from simple_bruteforce_classifiation import * 
from pathlib import Path


def main():
    bruteforce_data = Path('../data/ip_bruteforce_summary.json')

    # Convert json data to Dataframe format
    bruteforce_df = pd.read_json(bruteforce_data)
    
    # Data unchanged (No scaling/PCA) 
    features_df, k_means = original_ssh_activity_classifier(bruteforce_df)
    visualize_ssh_activity(features_df, k_means)


    features_scaled, k_means = ssh_activity_classifier(bruteforce_df)
    visualize_ssh_activity(features_scaled, k_means, True)

    # print(bruteforce_df)
    # print(bruteforce_df.head())


if __name__ == "__main__":
    main()
