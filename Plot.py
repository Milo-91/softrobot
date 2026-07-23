import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import csv
from pathlib import Path


def data_draw(csv_list, ax, color, label, x_axis, cal_conv=False):
    df = csv_list[0]
    for i in range(1, len(csv_list)):
        df = pd.merge(df, csv_list[i], on=x_axis, how='outer', suffixes=('', f'_{i}'))

    df = df.sort_values(x_axis)
    df = df.set_index(x_axis)
    df = df.ffill()
    mean = df.mean(axis=1)
    std = df.std(axis=1)
    df['mean'] = mean
    df['std'] = std
    print(df)

    print('final point', end=" ")
    final_score = df['mean'][10000]
    print(final_score)

    # calculate convergence
    if cal_conv:
        tolerance = 0.1
        threshold = final_score * tolerance
        conv_point = df[df['mean'] < final_score - threshold].index[-1]
        print('conv point', end=' ')
        print(conv_point)
        print(df['mean'][conv_point])

    # plot
    df['mean'].plot(ax=ax, color=color, marker='o', label=label)
    ax.fill_between(
        df.index,
        np.clip(df["mean"] - df["std"], 0, None),
        df["mean"] + df["std"],
        color=color,
        alpha=0.15,
    )
    if cal_conv:
        ax.scatter(conv_point, df['mean'][conv_point], color=color, marker='*', s=200, zorder=10)

def import_from_folder(folder):
    best_robots = []
    for file in folder.glob("*_best_record.csv"):
        best_robots.append(pd.read_csv(str(file.resolve())))

    similarity = []
    for file in folder.glob("*_similarity_record.csv"):
        similarity.append(pd.read_csv(str(file.resolve())))

    # LS_avg_improvement = []
    LS_successful_rate = []
    for file in folder.glob("*_ls_record.csv"):
        # LS_avg_improvement.append(pd.read_csv(str(file.resolve()), usecols=['eval_count', 'LS_avg_improvement']))
        LS_successful_rate.append(pd.read_csv(str(file.resolve()), usecols=['eval_count', 'LS_successful_rate']))

    mutation_size = []
    for file in folder.glob("*_mutation_size_record.csv"):
        mutation_size.append(pd.read_csv(str(file.resolve())))
    return best_robots, similarity, mutation_size, LS_successful_rate, len(best_robots)


if __name__ == '__main__':
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(18, 7.3))
    robot_x_axis = 'eval_count'
    sim_x_axis = 'eval_count'
    LS_x_axis = 'eval_count'
    mu_x_axis = 'eval_count'

    
    # GA with pop shrink
    folders_list = [
        'log/20260721/popsize100/ObstacleTraverser-v0T/ES/',
        'log/Integrated_Experiments/popsize100/ObstacleTraverser-v0T/GA+Init_pop/',
        'log/20260722/popsize100/ObstacleTraverser-v0T/MA+ES/',
        'log/Integrated_Experiments/popsize100/ObstacleTraverser-v0T/MA+HC/',
        'log/Integrated_Experiments/popsize100/ObstacleTraverser-v0T/GA/',
        'log/Integrated_Experiments/popsize100/ObstacleTraverser-v0T/HC/',
        # 'log/20260702/popsize100/ObstacleTraverser-v0T/GA+TS/',
    ]

    count = len(folders_list)
    cmap = plt.cm.turbo
    norm = mpl.colors.Normalize(vmin=0, vmax=count)

    best_robots = []
    similarity = []
    i = 0
    for folder in folders_list:
        f = Path(folder)
        print(f)
        best_robots, similarity, mutation_size, LS_successful_rate, count = import_from_folder(f)
        print(best_robots)
        data_draw(best_robots, ax[0][0], cmap(norm(i)), f'{f.name} ({count} runs)', robot_x_axis, True)
        data_draw(similarity, ax[0][1], cmap(norm(i)), f'{f.name} ({count} runs)', sim_x_axis)
        # if f.name == 'ES':
        #     data_draw(mutation_size, ax[1][0], cmap(norm(i)), f.name, mu_x_axis)
        # if f.name != 'GA':
            # data_draw(LS_successful_rate, ax[1][1], cmap(norm(i)), f.name, LS_x_axis)
        i += 1
    
    
    ax[0][0].set_title('best robots')
    ax[0][1].set_title('similarity')
    ax[1][0].set_title('mutation size')
    ax[1][1].set_title('local search successful rate')

    # plot information
    ax[0][0].legend(loc='best', fontsize=10)
    ax[0][1].legend(loc='best', fontsize=10)
    ax[1][0].legend(loc='best', fontsize=10)
    ax[1][1].legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.show()

