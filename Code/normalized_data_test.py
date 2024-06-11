import os
import json
import pandas as pd
import matplotlib.pyplot as plt 

def norm_data_plot(data_path, analysis_path, trial):
    # Path to trial results file
    trial_path = os.path.join(data_path,f"{trial}-result.json")

    # Loading in results file
    with open(trial_path, 'r') as file:
        trial_file = json.load(file)

    # Storing quasi state distribution data into a dataframe
    quasi_dists = trial_file["quasi_dists"][0]
    quasi_df = pd.DataFrame.from_dict(quasi_dists,orient='index')

    # Plotting the raw data
    quasi_df.plot(kind='bar',legend=False)
    plt.savefig(f"{analysis_path}/{trial}-raw.pdf")
    print(f"Trial {trial} raw graph complete")

    # Plotting the Normalized data
    norm_df = quasi_df.copy()
    norm_df = norm_df.abs() / (norm_df.abs()).sum()
    norm_df.plot(kind='bar',legend=False)
    plt.savefig(f"{analysis_path}/{trial}-norm.pdf")
    print(f"Trial {trial} norm graph complete")

def get_direct_path(code_path, target_dir):
    target_path = os.path.join(code_path,'..',target_dir)
    target_path = os.path.normpath(target_path)
    return target_path

# Getting direct path to subdirectories
code_path = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join('IBM-Q','ibm_kyoto')
analysis_dir = 'Analysis'
data_path = get_direct_path(code_path, data_dir)
analysis_path = get_direct_path(code_path, analysis_dir)
print(analysis_path)

# The good stuff
norm_data_plot(data_path, analysis_path, 1)