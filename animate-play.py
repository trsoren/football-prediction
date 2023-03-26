import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
import matplotlib as mpl
import os
import shutil

WORK_DIR = '/Users/trsorensen/Code/EECS448/football'

def plot_frame(frameId, df, x_range_size, y_range_size):
        """ Plots a single frame of a play. Called many times to build animations. """
        df = df[df['frameId'] == frameId]
        field = np.zeros((x_range_size+1, y_range_size+1))
        field[df['grid_x'][df['team'] == 'away'], df['grid_y'][df['team'] == 'away']] = 2
        field[df['grid_x'][df['team'] == 'home'], df['grid_y'][df['team'] == 'home']] = 4
        field[df['grid_x'][df['team'] == 'football'], df['grid_y'][df['team'] == 'football']] = 6
        
        # make a color map of fixed colors
        cmap = mpl.colors.ListedColormap(['palegreen','coral','deepskyblue', 'saddlebrown'])
        bounds=[-1,1,3,5,7]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        plt.imshow(field, cmap=cmap, norm=norm)
        plt.axhline(y=x_range_size*(1.0/12.0), color='black', linestyle='-')
        plt.axhline(y=x_range_size-x_range_size*(1.0/12.0) , color='black', linestyle='-')
        plt.savefig(f'{WORK_DIR}/img/img{frameId}.png')
        plt.close()

def main():
    # plays = pd.read_csv(WORK_DIR + '/data/data-bowl/plays.csv')
    # games = pd.read_csv(WORK_DIR + '/data/data-bowl/games.csv')

    df = pd.read_csv(WORK_DIR + '/data/data-bowl/week6.csv')

    games = df['gameId'].unique()
    
    # Specify game and play to look at
    df = df[df['gameId'] == 2018101500]
    df = df[df['playId'] == 424]

    print(df['playDirection'])

    # Assign each player to grid coordinates. Old x range: (0, 120). Old y range: (0, 53.3)
    new_x_range = (0, 48)
    new_y_range = (0, 20)
    x_range_size = new_x_range[1] - new_x_range[0]
    y_range_size = new_y_range[1] - new_y_range[0]
    x_scaled = df['x'] / 120.0
    y_scaled = df['y'] / 53.3
    new_x = np.round(x_scaled * x_range_size).astype(int)
    new_y = np.round(y_scaled * y_range_size).astype(int)
    # Flip coords based on play direction so offense always drives same direction
    new_x[df['playDirection'] == 'right'] = new_x_range[1] - new_x   
    new_y[df['playDirection'] == 'right'] = new_y_range[1] - new_y
    df['grid_x'] = new_x
    df['grid_y'] = new_y


    # Create img folder and save each frame to it
    os.mkdir(WORK_DIR + '/img/')
    frameIds = df['frameId'].unique()
    for frameId in frameIds:
         plot_frame(frameId, df, x_range_size, y_range_size)

    # Put frames all together
    frames = []
    for frameId in frameIds:
        image = imageio.v2.imread(f'/Users/trsorensen/Code/EECS448/football/img/img{frameId}.png')
        frames.append(image)

    # Save gif and remove the directory of frames
    imageio.mimsave('/Users/trsorensen/Code/EECS448/football/play.gif',
                    frames,
                    fps = 10)
    shutil.rmtree(WORK_DIR + '/img')


if __name__ == '__main__':
    main()