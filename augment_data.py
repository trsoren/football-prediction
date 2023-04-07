import numpy as np
import pandas as pd
import time


WORK_DIR = '/Users/trsorensen/Code/EECS448/football'
    

def main():
    startTime = time.time()

    # Read in the unaugmented test dataset
    df = pd.read_csv('nn_data_train.csv')

    # Mirror each play and save to new dataframe
    # Do NOT try to do this with a for loop
    def getFieldMirror(row):
        field = np.reshape(row[9:513].tolist(), (18, 28))
        return np.fliplr(field).flatten().tolist()
    fields = df.apply(getFieldMirror, axis=1).tolist()
    df_mirror = df
    df_mirror.iloc[:, 9:513] = fields
    
    # Mirror the play outcomes
    df_mirror['outcome'] = df_mirror['outcome'].str.replace(r'\bright\b', 'balls')
    df_mirror['outcome'] = df_mirror['outcome'].str.replace(r'\bleft\b', 'right')
    df_mirror['outcome'] = df_mirror['outcome'].str.replace(r'\bballs\b', 'left')

    # Combine original plays with the mirrored ones
    df = pd.concat([df, df_mirror], axis=0, ignore_index=True)
        
    # Write the augmented test data to a new csv file
    df.to_csv('nn_data_train_augmented.csv', index=False)
    print(time.time() - startTime)

if __name__ == '__main__':
    main()
