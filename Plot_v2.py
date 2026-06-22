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

    '''
    # GA
    GA_files_list = [
        '20260620/popsize100/_GA_100_06210649',
        '20260620/popsize100/_GA_100_06210601',
        '20260620/popsize100/_GA_100_06210513',
        '20260620/popsize100/_GA_100_06210424',
        '20260620/popsize100/_GA_100_06210339'
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
        '20260620/popsize100/_GA_100_06191656',
        '20260620/popsize100/_GA_100_06191727',
        '20260620/popsize100/_GA_100_06191758',
        '20260620/popsize100/_GA_100_06191828',
        '20260620/popsize100/_GA_100_06191900'
    ]
    best_robots = []
    similarity = []
    for GA_file in GA_files_list:
        best_robots.append(pd.read_csv('log/' + GA_file + '_best_record.csv'))
        similarity.append(pd.read_csv('log/' + GA_file + '_similarity_record.csv'))
    data_draw(best_robots, ax[0][0], "red", "GA no pop shrink", robot_x_axis)
    data_draw(similarity, ax[0][1], "red", "GA no pop shrink", sim_x_axis)
    '''
    # GA+TS
    TS_files_list = [
        '20260621/popsize100/_MA_Hill_Climbing_100_06211337',
        '20260621/popsize100/_MA_Hill_Climbing_100_06211500',
        '20260621/popsize100/_MA_Hill_Climbing_100_06211622',
        '20260621/popsize100/_MA_Hill_Climbing_100_06211749'
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
    data_draw(best_robots, ax[0][0], "green", "LS2", robot_x_axis)
    data_draw(similarity, ax[0][1], "green", "LS2", sim_x_axis)
    data_draw(LS_avg_improvement, ax[1][0], "green", "LS2", LS_x_axis)
    data_draw(LS_successful_rate, ax[1][1], "green", "LS2", LS_x_axis)

    # GA+HC
    HC_files_list = [
        '20260620/popsize100/_MA_Hill_Climbing_100_06191658',
        '20260620/popsize100/_MA_Hill_Climbing_100_06191730',
        '20260620/popsize100/_MA_Hill_Climbing_100_06191802',
        '20260620/popsize100/_MA_Hill_Climbing_100_06191834',
        '20260620/popsize100/_MA_Hill_Climbing_100_06191906'
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
    data_draw(best_robots, ax[0][0], "red", "LS1", robot_x_axis)
    data_draw(similarity, ax[0][1], "red", "LS1", sim_x_axis)
    data_draw(LS_avg_improvement, ax[1][0], "red", "LS1", LS_x_axis)
    data_draw(LS_successful_rate, ax[1][1], "red", "LS1", LS_x_axis)
    
    ax[0][0].set_title('best robots')
    ax[0][1].set_title('similarity')
    ax[1][0].set_title('local search avg improvement')
    ax[1][1].set_title('local search successful rate')

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

    # plot information
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    plt.show()



'''
    # different popsize
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    robot_x_axis = 'eval_count'
    sim_x_axis = 'gen_count'
    # popsize20
    popsize20 = []
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141428_best_record.csv'))
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141519_best_record.csv'))
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141612_best_record.csv'))
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141705_best_record.csv'))
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141757_best_record.csv'))
    data_draw(popsize20, ax[0], "blue", "popsize20", robot_x_axis)
    # popsize100
    popsize100 = []
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141427_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141516_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141608_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141700_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141753_best_record.csv'))
    data_draw(popsize100, ax[0], "red", "popsize100", robot_x_axis)
    # popsize200
    popsize200 = []
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141427_best_record.csv'))
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141517_best_record.csv'))
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141610_best_record.csv'))
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141702_best_record.csv'))
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141754_best_record.csv'))
    data_draw(popsize200, ax[0], "green", "popsize200", robot_x_axis)
    

    # popsize20
    popsize20 = []
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141428_similarity_record.csv'))
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141519_similarity_record.csv'))
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141612_similarity_record.csv'))
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141705_similarity_record.csv'))
    popsize20.append(pd.read_csv('log/20260614/popsize20/_GA_20_06141757_similarity_record.csv'))
    data_draw(popsize20, ax[1], "blue", "popsize20", sim_x_axis)
    # popsize100
    popsize100 = []
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141427_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141516_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141608_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141700_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141753_similarity_record.csv'))
    data_draw(popsize100, ax[1], "red", "popsize100", sim_x_axis)
    # popsize200
    popsize200 = []
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141427_similarity_record.csv'))
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141517_similarity_record.csv'))
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141610_similarity_record.csv'))
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141702_similarity_record.csv'))
    popsize200.append(pd.read_csv('log/20260614/popsize200/_GA_200_06141754_similarity_record.csv'))
    data_draw(popsize200, ax[1], "green", "popsize200", sim_x_axis)

    ax[0].set_title('GA best robot different popsize')
    ax[1].set_title('GA similarity in different popsize')


    # different algorithms
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))
    robot_x_axis = 'eval_count'
    sim_x_axis = 'gen_count'
    # GA+HC
    popsize100 = []
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06150009_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06142348_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06142330_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06142312_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06142255_best_record.csv'))
    data_draw(popsize100, ax[0], "red", "GA+HC", robot_x_axis)
    popsize100 = []
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06150009_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06142348_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06142330_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06142312_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Hill_Climbing_100_06142255_similarity_record.csv'))
    data_draw(popsize100, ax[1], "red", "GA+HC", sim_x_axis)
    # GA
    popsize100 = []
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141427_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141516_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141608_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141700_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141753_best_record.csv'))
    data_draw(popsize100, ax[0], "blue", "GA", robot_x_axis)
    popsize100 = []
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141427_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141516_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141608_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141700_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_GA_100_06141753_similarity_record.csv'))
    data_draw(popsize100, ax[1], "blue", "GA", sim_x_axis)
    # GA+TS
    popsize100 = []
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150510_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150405_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150301_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150159_best_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150106_best_record.csv'))
    data_draw(popsize100, ax[0], "green", "GA+TS", robot_x_axis)
    popsize100 = []
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150510_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150405_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150301_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150159_similarity_record.csv'))
    popsize100.append(pd.read_csv('log/20260614/popsize100/_MA_Tabu_Search_100_06150106_similarity_record.csv'))
    data_draw(popsize100, ax[1], "green", "GA+TS", sim_x_axis)
    ax[0].set_title('popsize100 best robot')
    ax[1].set_title('popsize100 similarity')
'''
