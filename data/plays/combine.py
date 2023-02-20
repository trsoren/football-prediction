import pandas as pd
import os
import glob

# Get a list of all CSV files in the current directory
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

# Combine all CSV files into a single DataFrame
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

# Export the combined CSV file
combined_csv.to_csv("play_features.csv", index=False, encoding='utf-8-sig')