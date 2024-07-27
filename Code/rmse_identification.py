import os
import pandas as pd
import numpy as np

def get_comp_avgs(df):

    # Reducing distribution columns by using ".agg"s built-in "mean" function
    dist_cols = df.columns[3:]
    reduction = {dists: 'mean' for dists in dist_cols}

    # Converting dates from String to Timestamps
    df["date"] = pd.to_datetime(df["date"])
    df = df.rename(columns={"date":"time"})

    # Reducing the date column by defining a function to calculate trial time span
    def time_span(date):
        return date.max() - date.min()
    reduction["time"] = time_span

    # Grouping trials by computer and reducing their date and distributions as defined above
    return df.groupby(["computer"]).agg(reduction)

def get_trial_rmse(df, comp_avgs):

    # Setting up rmse dataframe
    computers = comp_avgs.index
    trial_rmse = pd.DataFrame(columns=computers)

    # Saving the trial's true computer for reference
    trial_rmse["computer"] = df["computer"]

    # Calculating each trial's rmse with the averaged computer distribution
    dist_cols = df.columns[3:]

    # Iterating rmse calculation for each computer
    for computer in computers:
        comp_err = np.zeros(df.shape[0])

        # Iterating through each state distribution for every trial
        for dist in dist_cols:
            trial_vals = df[dist].values
            comp_avg_val = comp_avgs.loc[computer,dist]
        
        # Compiling error for all of a trial's states
            comp_err += (trial_vals - comp_avg_val)**2
        
        # Calculating rmse for every trial against current computer
        trial_rmse[computer] = np.sqrt(comp_err/len(dist_cols))
    
    # Guessing each trial came from the computer producing the lowest rmse
    trial_rmse["guess"] = trial_rmse[computers].idxmin(axis=1)

    trial_rmse.index.names = ["Trial"]
    return trial_rmse

# Loading data as "df"
# Assuming "data.csv" in same directory as this code
code_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(code_dir,"data.csv")
df = pd.read_csv(data_path)

# The good stuff
comp_avgs = get_comp_avgs(df)
trial_rmse = get_trial_rmse(df, comp_avgs)

print("Computer Averages")
print(comp_avgs)
print("Trial RMSE")
print(trial_rmse)