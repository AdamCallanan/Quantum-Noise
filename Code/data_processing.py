import os
import json
import pandas as pd
import numpy as np

def process_data(data_dir):

    # Getting total number of trials
    num_trials = 0
    for current_dir,sub_dirs,dir_files in os.walk(data_dir):

        # Each trial produces 2 files
        num_trials += len(dir_files)/2
    
    # Checking for an even number of files
    if num_trials%2 != 0:
        print("Error: Odd number of files.")
        return

    # Shit
    got_info = False
    got_dists = False
    info_labels = ['computer','date','shots']
    data = np.zeros(int(num_trials),dtype=object)
    trial = 0

    # Iterates through directories, top down, n=0 is data_dir
    for current_dir,sub_dirs,dir_files in os.walk(data_dir):
        dir_files = sorted(dir_files)

        # Iterates through data files, if any exist in current directory
        for file in dir_files:
            if file.endswith('.json'):

                # Processing info file
                if "info" in file:

                    # Loading in info data
                    file_path = os.path.join(current_dir,file)
                    with open(file_path, 'r') as info_json:
                        info_data = json.load(info_json)

                    # Extracting relevant info
                    desired_entries = ["backend","ended","params"]
                    info = [info_data.get(desired_entry) for desired_entry in desired_entries]
                    info[-1] = info[-1]["run_options"]["shots"]

                    # Labelling data
                    info = dict(zip(info_labels,info))

                    # Info check
                    got_info = True


                # Processing result file
                elif "result" in file:
                    # Loading in result data
                    file_path = os.path.join(current_dir,file)
                    with open(file_path, 'r') as result_json:
                        result_data = json.load(result_json)

                    # Extracting only the distribution results
                    dists = result_data["quasi_dists"][0]

                    # Getting the absolute sum of the distribution values
                    abs_sum = 0
                    for state,value in dists.items():
                        abs_sum += abs(value)
                    
                    # Normalizing the distribution
                    for state,value in dists.items():
                        dists[state] = abs(value)/abs_sum

                    # Result check
                    got_dists = True

                # Adding a given trial's processed data to the dataframe
                if got_info and got_dists:
                    data[trial] = info|dists

                    # Setting index for next trial
                    trial += 1

                    # Resetting checks
                    got_info = False
                    got_dists = False

    # Storing data in dataframe
    data = data.tolist()
    df = pd.DataFrame(data)

    # Organizing state columns in numerical order
    dist_columns = df.columns[3:]
    dist_columns = sorted(dist_columns,key=lambda col: int(col,2))

    # Reorganzing dataframe
    info_columns = list(df.columns[:3])
    df = df[info_columns+dist_columns]

    # Filling blanks with zeros
    df = df.fillna(0)

    # Exporting dataframe to csv
    df.to_csv("data.csv",index=False)


# Getting this python file's directory
code_dir = os.path.dirname(os.path.realpath(__file__))

# Getting data directory relative path
data_dir_name = 'IBM-Q'
data_dir = os.path.join(code_dir,'..',data_dir_name)

# Getting data directory absolute path
data_dir = os.path.normpath(data_dir)

# The good stuff
process_data(data_dir)