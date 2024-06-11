import os
import json
import pandas as pd
import matplotlib.pyplot as plt 

# Path to results file
data_path = os.path.join("IBM-Q","ibm_kyoto","1-result.json")

# Loading in results file
with open(data_path, 'r') as file:
    result = json.load(file)

# 5-qubit distribution result dictionary
quasi_dists = result["quasi_dists"][0]
quasi_df = pd.DataFrame.from_dict(quasi_dists,orient='index')

# Viewing the raw data
quasi_df.plot(kind='bar')
plt.show()

# Normalizing the data
norm_df = quasi_df.copy()
norm_df = norm_df.abs() / (norm_df.abs()).sum()

# Viewing the normalized data
norm_df.plot(kind='bar')
plt.show()