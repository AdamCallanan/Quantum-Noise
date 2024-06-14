import os
import pandas as pd
import matplotlib.pyplot as plt

# Loading dataframe
df = pd.read_csv("data.csv")

# Selecting the ibm_kyoto trials
kyoto_df = df[df["computer"]=="ibm_kyoto"]

# Plotting setup
fig,ax = plt.subplots()

# Selecting the first kyoto trial's distribution data
kyoto_trial_1 = kyoto_df.iloc[0,3:]

# Plotting said data
ax.bar(kyoto_trial_1.index, kyoto_trial_1.values)

# Plotting stuff
plt.xticks(rotation=90)

# Saving figure to Analysis folder
code_dir = os.path.dirname(os.path.realpath(__file__))
analysis_dir = os.path.join(code_dir,'..',"Analysis")
analysis_dir = os.path.normpath(analysis_dir)
plt.savefig(f"{analysis_dir}/kyoto_1.png")