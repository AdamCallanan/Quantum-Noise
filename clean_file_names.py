import os

def clean_file_names(root_directory):
    for subdir, _, files in os.walk(root_directory):

        # Sort the files to ensure consistent numbering
        files.sort()

        # Loop through the files and rename them
        prefix = ""
        n = 1
        for filename in files:

            # Split the filename at the first hyphen
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

# Example usage
root_directory = 'IBM-Q'
clean_file_names(root_directory)