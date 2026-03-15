import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from mpl_toolkits.mplot3d import Axes3D


def ssh_activity_clustering(features_unscaled, n_clusters=4):
    # features_df = bruteforce_df[['conn_fail_ratio', 'mean_orig_pkts', 'pkt_consistency', 'dest_ip_ratio']]

    # Scale data (> total_conn values will skew clustering)
    scaled_features = StandardScaler()
    features_scaled = scaled_features.fit_transform(features_unscaled)

    # Run Kmeans to clusters for data
    k_means = KMeans(n_clusters, random_state=0, n_init="auto").fit(features_scaled)

    return features_scaled, k_means


def feature_selection(n_features):
    # Store all combinations of 3 features selected
    feature_combinations = []

    for i in range(len(n_features)):
        feature_set = []
        for j in range(len(n_features)):
            if i == j:
                continue
            feature_set.append(j)
        feature_combinations.append(feature_set)

    return feature_combinations


def visualize_ssh_activity(features_scaled, feature_names, k_means, pca=False):
    # # Run all possible combinations of selected features
    # feature_combinations = feature_selection(features_scaled)

    # 3d plot with no PCA (3 features)
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')

    x = features_scaled[:,0]
    y = features_scaled[:,1]
    z = features_scaled[:,2]
    c = k_means.labels_

    scatter = ax.scatter(x, y, z, c=c, cmap='viridis', alpha=0.7)

    ax.set_xlabel(feature_names[0])
    ax.set_ylabel(feature_names[1])
    ax.set_zlabel(feature_names[2])
    ax.set_title('SSH Bruteforce Activity (3D Clustering)')
    
    fig.colorbar(scatter, label='Cluster')
    plt.show()


    # fig = plt.figure(figsize=(8,6))
    # ax = fig.add_subplot(111, projection='3d')

    # x = features_scaled[:,0]  # conn_fail_ratio
    # y = features_scaled[:,1]  # pkt_consistency
    # z = features_scaled[:,2]  # dest_ip_ratio
    # c = k_means.labels_       # color by cluster

    # scatter = ax.scatter(x, y, z, c=c, cmap='viridis', alpha=0.7)
    # ax.set_xlabel('Connection Failure Ratio')
    # ax.set_ylabel('Packet Consistency')
    # ax.set_zlabel('Destination IP Ratio')
    # ax.set_title('SSH Bruteforce Activity (3D Clustering)')
    
    # fig.colorbar(scatter, label='Cluster')
    # plt.show()

    # Representing in 2d
    if pca:
        pca_model = PCA(n_components=2)
        features_pca = pca_model.fit_transform(features_scaled)
        plt.figure(figsize=(8,6))
        scatter = plt.scatter(
            features_pca[:,0],
            features_pca[:,1],
            c=k_means.labels_,
            cmap='viridis',
            alpha=0.7
        )
        plt.xlabel('PCA Component 1')
        plt.ylabel('PCA Component 2')
        plt.title('SSH Bruteforce Activity (2D PCA)')
        plt.colorbar(scatter, label='Cluster')
        plt.show()


def separate_clusters_df(bruteforce_df, k_means):

    bruteforce_df = bruteforce_df.copy()
    bruteforce_df["cluster"] = k_means.labels_

    cluster_1 = bruteforce_df[bruteforce_df["cluster"] == 0]
    cluster_2 = bruteforce_df[bruteforce_df["cluster"] == 1]
    cluster_3 = bruteforce_df[bruteforce_df["cluster"] == 2]
    cluster_4 = bruteforce_df[bruteforce_df["cluster"] == 3]

    return [cluster_1, cluster_2, cluster_3, cluster_4]


def save_clusters(clusters, idx):

    output_dir = Path("../data/feature_selection_clusters")
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, cluster_df in enumerate(clusters):
        # Print cluster details
        print(f"Cluster {i+1} size:", len(cluster_df))

        output_file = output_dir / f"feature_set_{idx}_cluster_{i}.json"
        cluster_df.to_json(output_file, orient="records", lines=True)

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report, confusion_matrix
# from sklearn.model_selection import train_test_split



# def train_attack_classifier(cluster_set, feature_names):

#     labeled_clusters = []

#     # Label clusters (cluster 3 = attack)
#     for i, cluster_df in enumerate(cluster_set):

#         cluster_df = cluster_df.copy()

#         if i == 2:  # cluster 3 (index 2)
#             cluster_df["attack"] = 1
#         else:
#             cluster_df["attack"] = 0

#         labeled_clusters.append(cluster_df)

#     # Combine clusters
#     df = pd.concat(labeled_clusters, ignore_index=True)

#     # Show class distribution
#     print("\nClass Distribution:")
#     print(df["attack"].value_counts())

#     # Feature matrix and labels
#     X = df[feature_names]
#     y = df["attack"]

#     # Scale features
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)

#     # Stratified train/test split
#     X_train, X_test, y_train, y_test = train_test_split(
#         X_scaled,
#         y,
#         test_size=0.2,
#         stratify=y,     # <-- key change
#         random_state=42
#     )

#     # Train classifier
#     model = RandomForestClassifier(random_state=42, class_weight='balanced')
#     model.fit(X_train, y_train)

#     # Predictions
#     preds = model.predict(X_test)

#     # Evaluation
#     print("\nClassifier Performance:")
#     print(classification_report(y_test, preds))

#     print("Confusion Matrix:")
#     print(confusion_matrix(y_test, preds))

#     return model, scaler

def cluster_heatmap(df, k_means, feature_names):

    df = df.copy()
    df["cluster"] = k_means.labels_

    cluster_stats = df.groupby("cluster")[feature_names].mean()

    plt.figure(figsize=(8,6))

    sns.heatmap(
        cluster_stats,
        annot=True,
        cmap="viridis"
    )

    plt.title("Cluster Feature Averages")
    plt.show()

