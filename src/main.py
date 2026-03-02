# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import random as rand
from pathlib import Path

from sklearn.cluster import KMeans 

def main():

    bruteforce_data = Path('../data/ip_bruteforce_summary.json')

    # Convert json data to Dataframe format
    bruteforce_df = pd.read_json(bruteforce_data)
    
    # print(bruteforce_df)
    print(bruteforce_df.head())



if __name__ == "__main__":
    main()
