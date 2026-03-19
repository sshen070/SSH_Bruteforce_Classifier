# SSH Brute Force Detection using Unsupervised Learning Methods

## Overview

This project builds a machine learning pipeline to detect SSH brute-force attacks using network connection logs (Zeek `conn.log`) from datasets containing *real-world traffic*. It uses **unsupervised clustering** to distinguish malicious behavior without requiring labeled data upfront. 

To address the lack of ground-truth labels, this project is inspired by prior work including Hidden Markov Models (HMM) approaches (https://link.springer.com/chapter/10.1007/978-3-642-04989-7_13), which infer connection intent through packet & flow level behavior. Additionally, this work draws from research on separating benign and malicious traffic using connection failure ratios (https://dl.acm.org/doi/epdf/10.1145/2508859.2516719). 

Overall, the workflow follows the principle of pattern discovery → detection automation.

---

## Pipeline

The system follows a hybrid ML pipeline:

```
Zeek conn.log / JSON
        ↓
Feature Engineering
        ↓
KMeans Clustering (ML)
        ↓
Cluster Interpretation
        ↓
Attack Prediction (In Development)
```

---

## Features Engineered

Each source IP is summarized into behavioral features:

| Feature           | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `conn_fail_ratio` | Ratio of failed SSH over connections total connections made by a client                      |
| `mean_orig_pkts`  | Average packets sent per connection by the client                 |
| `pkt_consistency` | Coefficient of variation (std/mean) of packet counts |
| `dest_ip_ratio`   | Unique destination IPs over total connections made by client         |

These features capture patterns typical of brute-force attacks:

* High failure rates
* Consistent packet behavior
* Scanning across multiple destinations

---

## Clustering (Unsupervised Learning)

We apply **KMeans clustering** to group IPs by behavior:

* No labels are required
* Clusters naturally separate:

  * Normal users
  * Light traffic
  * Scanners
  * Brute-force attackers

Cluster statistics are analyzed to identify which cluster corresponds to attack activity.

---

## Label Generation

After clustering:

* Attack clusters are manually identified based on packet flows & connections made by a client (e.g., Cluster 3)
* These clusters are labeled as:

  * `1 → attack`
  * `0 → benign`

This converts unsupervised structure into  a supervised training structure.

---

## Visualization

The project includes multiple visualization tools:

* **3D Feature Plots** (cluster visualization)
* **PCA Projection** (2D representation)
* **Cluster Heatmaps** (feature averages among clusters)

These help interpret model behavior and validate feature effectiveness.

---

## Usage

### Required Files (from Zeek)

```
conn.log
```

### 1. Run Feature Engineering

```
python ssh_feature_engineering.py
```

### 2. Merge Features

```
python feature_merger.py
```

### 3. Run Classification Pipeline

```
python main.py
```

### 4. Output

* Clustered datasets
* Feature datasets
* Visualizations

## Key Insights

* Brute-force attacks form **distinct clusters** in 3 dimensional feature space
* `conn_fail_ratio` and `dest_ip_ratio` are the strongest indicators
* Even simple models perform well due to strong behavioral signals
* Class imbalance is the primary challenge in evaluation

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Matplotlib

---