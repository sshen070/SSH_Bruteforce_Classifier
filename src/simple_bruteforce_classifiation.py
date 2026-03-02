import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import random as rand

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def original_ssh_activity_classifier(bruteforce_df):
    features_df = bruteforce_df[['total_conn', 'conn_fail_ratio']]
    # print(features_df.head())

    # Run Kmeans to clusters for data 
    k_means = KMeans(n_clusters=4, random_state=0, n_init="auto").fit(features_df)
    # print(k_means.labels_)
    # bruteforce_df['cluster'] = k_means.labels_

    return features_df.values, k_means


def ssh_activity_classifier(bruteforce_df):
    features_df = bruteforce_df[['total_conn', 'conn_fail_ratio']]
    # print(features_df.head())

    # Scale data (> total_conn values will skew clustering)
    scaled_features = StandardScaler()
    features_scaled = scaled_features.fit_transform(features_df)
    print(features_scaled[0:5])

    # # Converts scaled features into two components
    # pca = PCA(n_components=2)
    # features_pca = pca.fit_transform(features_scaled)
    # print(features_pca[0:5])

    # Run Kmeans to clusters for data 
    k_means = KMeans(n_clusters=4, random_state=0, n_init="auto").fit(features_scaled)
    # print(k_means.labels_)
    bruteforce_df['cluster'] = k_means.labels_

    return features_scaled, k_means


def visualize_ssh_activity(features_scaled, k_means, scaled=False):
    plt.figure(figsize=(8,6))
    plt.scatter(

        # features_df['total_conn'], 
        # features_df['conn_fail_ratio'], 
        # c=bruteforce_df['cluster'],

        features_scaled[:, 0],
        features_scaled[:, 1], 
        c=k_means.labels_,
        cmap='viridis',               
        alpha=0.7
    )

    if (scaled):
        # Number of attempts
        plt.xlabel('Scaled Total Connections')

        # SSH Bruteforce Failure Ratio
        plt.ylabel('Scaled Failure Ratio')
        plt.title('KMeans Clustering of SSH Bruteforce Activity')
        plt.legend()
        plt.show()
        
    else:
        plt.xlabel('Total Connections')
        plt.ylabel('SSH Bruteforce Failure Ratio')
        plt.title('KMeans Clustering of SSH Bruteforce Activity')
        plt.legend()
        plt.show()

