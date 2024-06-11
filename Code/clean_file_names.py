import os

def clean_file_names(data_path):
    for subdir, _, files in os.walk(data_path):

        # Sorting the files to ensure consistent numbering
        files.sort()

        # Loop through the files and rename them
        prefix = ""
        n = 1
        for filename in files:

            # Split the filenames at the hyphen
            parts = filename.split('-', 1)

            # Remove non .json files
            name, extension = os.path.splitext(filename)
            if extension != ".json":
                old_file_path = os.path.join(subdir, filename)
                os.remove(old_file_path)

            # Give same prefix files the same number
            elif parts[0] == prefix:
                suffix = parts[1]
                new_filename = f"{new_prefix}-{suffix}"
                
                # Create the full old and new file paths
                old_file_path = os.path.join(subdir, filename)
                new_file_path = os.path.join(subdir, new_filename)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)

            # Ensure the filename has at least one hyphen
            elif len(parts) == 2:
                prefix = parts[0]
                new_prefix = str(n)
                suffix = parts[1]
                new_filename = f"{new_prefix}-{suffix}"
                
                # Create the full old and new file paths
                old_file_path = os.path.join(subdir, filename)
                new_file_path = os.path.join(subdir, new_filename)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                n += 1

# Getting direct path to data directory
data_dir = 'IBM-Q'
code_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(code_path,'..',data_dir)
data_path = os.path.normpath(data_path)

# The good stuff
clean_file_names(data_path)