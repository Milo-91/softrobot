import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import csv
from pathlib import Path
import re


def sort_by_rho_tau(path):
    pattern = re.compile(r'r([0-9\.]+)_t([0-9\.]+)')
    sub_path = path.name
    print(path.name)
    match = pattern.match(sub_path)

    rho = float(match.group(1))
    tau = float(match.group(2))

    return rho, tau

def data_draw(csv_list, ax, color, label, x_axis):
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
    # print(df)

    # plot
    df['mean'].plot(ax=ax, color=color, marker='o', label=label)
    ax.fill_between(
        df.index,
        np.clip(df["mean"] - df["std"], 0, None),
        df["mean"] + df["std"],
        color=color,
        alpha=0.15,
    )


def import_from_folder(folder):
    best_robots = []
    for file in folder.glob("*_best_record.csv"):
        best_robots.append(pd.read_csv(str(file.resolve())))
    similarity = []
    for file in folder.glob("*_similarity_record.csv"):
        similarity.append(pd.read_csv(str(file.resolve())))

    return best_robots, similarity


if __name__ == '__main__':
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 7.3))
    robot_x_axis = 'eval_count'
    sim_x_axis = 'eval_count'
    LS_x_axis = 'eval_count'
    log_path = 'log/20260629/popsize100/'
    task = 'Climber-v0T'

    
    all_sim = Path(f'{log_path}{task}/')
    count = sum(1 for x in all_sim.glob("*"))
    print(f'count = {count}')
    cmap = plt.cm.turbo
    norm = mpl.colors.Normalize(vmin=0, vmax=count)
    i = 0
    for sim in sorted(all_sim.glob("*"), key=sort_by_rho_tau):
        # if i == 10:
        #     break
        print(sim)
        best_robots, similarity = import_from_folder(sim)
        data_draw(best_robots, ax[0], cmap(norm(i)), sim.name, robot_x_axis)
        data_draw(similarity, ax[1], cmap(norm(i)), sim.name, sim_x_axis)
        i += 1
    
    
    # ga no pop shrink
    ga_files_list = Path(f'{log_path}{task}/r1_t0/')
    print(ga_files_list)
    best_robots = []
    similarity = []
    best_robots, similarity = import_from_folder(ga_files_list)
    data_draw(best_robots, ax[0], "purple", "ga", robot_x_axis)
    data_draw(similarity, ax[1], "purple", "ga", sim_x_axis)
    
    ax[0].set_title('best robots')
    ax[1].set_title('similarity')
    

    # plot information
    ax[0].legend(loc='upper left', fontsize=10)
    ax[1].legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.show()
    
