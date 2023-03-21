import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio
import matplotlib as mpl
import os
import shutil

WORK_DIR = '/Users/trsorensen/Code/EECS448/football'

def plot_frame(frameId, df):
        df = df[df['frameId'] == frameId]
        field = np.zeros((120, 54))
        field[df['grid_x'][df['team'] == 'away'], df['grid_y'][df['team'] == 'away']] = 2
        field[df['grid_x'][df['team'] == 'home'], df['grid_y'][df['team'] == 'home']] = 4
        field[df['grid_x'][df['team'] == 'football'], df['grid_y'][df['team'] == 'football']] = 6
        
        # make a color map of fixed colors
        cmap = mpl.colors.ListedColormap(['palegreen','coral','deepskyblue', 'saddlebrown'])
        bounds=[-1,1,3,5,7]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        plt.imshow(field, cmap=cmap, norm=norm)
        plt.axhline(y=10, color='black', linestyle='-')
        plt.axhline(y=110, color='black', linestyle='-')
        plt.savefig(f'{WORK_DIR}/img/img{frameId}.png')
        plt.close()

def main():
    # plays = pd.read_csv(WORK_DIR + '/data/data-bowl/plays.csv')
    # games = pd.read_csv(WORK_DIR + '/data/data-bowl/games.csv')

    df = pd.read_csv(WORK_DIR + '/data/data-bowl/week16.csv')

    games = df['gameId'].unique()
    
    # Looking at first game of the season
    df = df[df['gameId'] == 2018122300]

    df = df[df['playId'] == 838]

    # Assign each player to grid coordinates. field size is grid with x: 0 to 120, y: 0 to 53.3
    grid_x = np.floor(df['x']).astype(int)
    grid_y = np.floor(df['y']).astype(int)
    grid_x[grid_x < 0] = 0
    grid_x[grid_x > 119] = 119
    grid_y[grid_y < 0] = 0
    grid_y[grid_y > 53] = 53
    df['grid_x'] = grid_x
    df['grid_y'] = grid_y

    # Create img folder and save each frame to it
    os.mkdir(WORK_DIR + '/img/')
    frameIds = df['frameId'].unique()
    for frameId in frameIds:
         plot_frame(frameId, df)

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