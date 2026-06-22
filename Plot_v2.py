import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

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
    print(df)

    # plot
    df['mean'].plot(ax=ax, color=color, marker='o', label=label)
    ax.fill_between(
        df.index,
        np.clip(df["mean"] - df["std"], 0, None),
        df["mean"] + df["std"],
        color=color,
        alpha=0.15,
    )


if __name__ == '__main__':
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(18, 7.3))
    robot_x_axis = 'eval_count'
    sim_x_axis = 'gen_count'
    LS_x_axis = 'gen_count'

    
    # GA with pop shrink
    GA_files_list = [
        '20260622/popsize100/_GA_100_06221141',
        '20260622/popsize100/_GA_100_06221217',
        '20260622/popsize100/_GA_100_06221255',
        '20260622/popsize100/_GA_100_06221333',
        '20260622/popsize100/_GA_100_06221414'
    ]
    best_robots = []
    similarity = []
    for GA_file in GA_files_list:
        best_robots.append(pd.read_csv('log/' + GA_file + '_best_record.csv'))
        similarity.append(pd.read_csv('log/' + GA_file + '_similarity_record.csv'))
    data_draw(best_robots, ax[0][0], "blue", "GA with pop shrink", robot_x_axis)
    data_draw(similarity, ax[0][1], "blue", "GA with pop shrink", sim_x_axis)
    
    # GA no pop shrink
    GA_files_list = [
        '20260621/popsize100/_GA_100_06212250',
        '20260621/popsize100/_GA_100_06220004',
        '20260621/popsize100/_GA_100_06220127',
        '20260621/popsize100/_GA_100_06220242',
        '20260621/popsize100/_GA_100_06220359'
    ]
    best_robots = []
    similarity = []
    for GA_file in GA_files_list:
        best_robots.append(pd.read_csv('log/' + GA_file + '_best_record.csv'))
        similarity.append(pd.read_csv('log/' + GA_file + '_similarity_record.csv'))
    data_draw(best_robots, ax[0][0], "purple", "GA", robot_x_axis)
    data_draw(similarity, ax[0][1], "purple", "GA", sim_x_axis)
    
    # GA+TS
    TS_files_list = [
        '20260622/popsize100/pop_shrink/_MA_Hill_Climbing_100_06221514',
        '20260622/popsize100/pop_shrink/_MA_Hill_Climbing_100_06221528',
        '20260622/popsize100/pop_shrink/_MA_Hill_Climbing_100_06221541',
        '20260622/popsize100/pop_shrink/_MA_Hill_Climbing_100_06221553',
        '20260622/popsize100/pop_shrink/_MA_Hill_Climbing_100_06221605'
    ]
    best_robots = []
    similarity = []
    LS_avg_improvement = []
    LS_successful_rate = []
    for TS_file in TS_files_list:
        best_robots.append(pd.read_csv('log/' + TS_file + '_best_record.csv'))
        similarity.append(pd.read_csv('log/' + TS_file + '_similarity_record.csv'))
        LS_avg_improvement.append(pd.read_csv('log/' + TS_file + '_ls_record.csv', usecols=['gen_count', 'LS_avg_improvement']))
        print(pd.read_csv('log/' + TS_file + '_ls_record.csv'))
        LS_successful_rate.append(pd.read_csv('log/' + TS_file + '_ls_record.csv', usecols=['gen_count', 'LS_successful_rate']))
    data_draw(best_robots, ax[0][0], "green", "GA+HC with pop shrink", robot_x_axis)
    data_draw(similarity, ax[0][1], "green", "GA+HC with pop shrink", sim_x_axis)
    data_draw(LS_avg_improvement, ax[1][0], "green", "GA+HC with pop shrink", LS_x_axis)
    data_draw(LS_successful_rate, ax[1][1], "green", "GA+HC with pop shrink", LS_x_axis)

    # GA+HC
    HC_files_list = [
        '20260621/popsize100/_MA_Hill_Climbing_100_06211500',
        '20260621/popsize100/_MA_Hill_Climbing_100_06211337',
        '20260621/popsize100/_MA_Hill_Climbing_100_06211622',
        '20260621/popsize100/_MA_Hill_Climbing_100_06211749'
    ]
    best_robots = []
    similarity = []
    LS_avg_improvement = []
    LS_successful_rate = []
    for HC_file in HC_files_list:
        best_robots.append(pd.read_csv('log/' + HC_file + '_best_record.csv'))
        similarity.append(pd.read_csv('log/' + HC_file + '_similarity_record.csv'))
        LS_avg_improvement.append(pd.read_csv('log/' + HC_file + '_ls_record.csv', usecols=['gen_count', 'LS_avg_improvement']))
        LS_successful_rate.append(pd.read_csv('log/' + HC_file + '_ls_record.csv', usecols=['gen_count', 'LS_successful_rate']))
    data_draw(best_robots, ax[0][0], "red", "GA+HC", robot_x_axis)
    data_draw(similarity, ax[0][1], "red", "GA+HC", sim_x_axis)
    data_draw(LS_avg_improvement, ax[1][0], "red", "GA+HC", LS_x_axis)
    data_draw(LS_successful_rate, ax[1][1], "red", "GA+HC", LS_x_axis)
    
    ax[0][0].set_title('best robots')
    ax[0][1].set_title('similarity')
    ax[1][0].set_title('local search avg improvement')
    ax[1][1].set_title('local search successful rate')

    '''
    # GA+TS
    TS_files_list = [
        '20260621/popsize100/_MA_Hill_Climbing_100_06212249',
        '20260621/popsize100/_MA_Hill_Climbing_100_06220001',
        '20260621/popsize100/_MA_Hill_Climbing_100_06220123',
        '20260621/popsize100/_MA_Hill_Climbing_100_06220238',
        '20260621/popsize100/_MA_Hill_Climbing_100_06220355'
    ]
    best_robots = []
    similarity = []
    LS_avg_improvement = []
    LS_successful_rate = []
    for TS_file in TS_files_list:
        best_robots.append(pd.read_csv('log/' + TS_file + '_best_record.csv'))
        similarity.append(pd.read_csv('log/' + TS_file + '_similarity_record.csv'))
        LS_avg_improvement.append(pd.read_csv('log/' + TS_file + '_ls_record.csv', usecols=['gen_count', 'LS_avg_improvement']))
        print(pd.read_csv('log/' + TS_file + '_ls_record.csv'))
        LS_successful_rate.append(pd.read_csv('log/' + TS_file + '_ls_record.csv', usecols=['gen_count', 'LS_successful_rate']))
    data_draw(best_robots, ax[0][0], "blue", "LS3", robot_x_axis)
    data_draw(similarity, ax[0][1], "blue", "LS3", sim_x_axis)
    data_draw(LS_avg_improvement, ax[1][0], "blue", "LS3", LS_x_axis)
    data_draw(LS_successful_rate, ax[1][1], "blue", "LS3", LS_x_axis)
    '''
    # plot information
    ax[0][0].legend(loc='best', fontsize=10)
    ax[0][1].legend(loc='best', fontsize=10)
    ax[1][0].legend(loc='best', fontsize=10)
    ax[1][1].legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.show()

