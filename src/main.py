from ssh_feature_engineering import find_conn_log
from simple_bruteforce_classifiation import *
from pathlib import Path


def preprocess_data(bruteforce_df):
    # Only compute upper bound
    upper_bound = bruteforce_df['pkt_consistency'].quantile(0.99)

    # Remove only extreme high outliers
    filtered_df = bruteforce_df[bruteforce_df['pkt_consistency'] <= upper_bound]


    print("Original size:", len(bruteforce_df))
    print("Filtered size:", len(filtered_df))
    print("Upper bound:", upper_bound)

    return filtered_df


def main():
    input_file = input('Enter data file NAME: ')

    # Find input file in repo
    root = Path.cwd().resolve().parent
    
    # Input log file
    input_path = find_conn_log(root, input_file)
    print(f"Using conn.log at: {input_path}")

    # Convert json data to Dataframe format
    bruteforce_df = pd.read_json(input_path)

    user_input = int(input('Preprocess? '))

    if (user_input):
        # Preprocessing (Remove outliers)
        bruteforce_df = preprocess_data(bruteforce_df)

    # Define all features
    all_features = ['conn_fail_ratio', 'mean_orig_pkts', 'pkt_consistency', 'dest_ip_ratio']

    # Generate 3-feature combinations
    features_selection_arr = feature_selection(all_features)

    for idx, feature_combo in enumerate(features_selection_arr):
        feature_names = []
        for j in feature_combo:
            feature_names.append(all_features[j])

        # Scaled data ~ No PCA
        features_scaled, k_means = ssh_activity_clustering(bruteforce_df[feature_names])

        visualize_ssh_activity(features_scaled, feature_names, k_means, True)

        if (idx == 1):
            cluster_set = separate_clusters_df(bruteforce_df, k_means)
            save_clusters(cluster_set, idx)



if __name__ == "__main__":
    main()
