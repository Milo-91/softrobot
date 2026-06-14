import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv


if __name__ == '__main__':
    MA_list = []
    # MA line 1
    df = None
    MA_list.append(pd.read_csv('log/20260608/popsize100/_MA_100_06080128_best_record.csv'))
    print(MA_list[0])
    df = MA_list[0]
    # MA line 2
    MA_list.append(pd.read_csv('log/20260608/popsize100/_MA_100_06080144_best_record.csv'))
    print(MA_list[1])
    df = pd.merge(df, MA_list[1], on='eval_count', how='outer')
    # MA line 3
    MA_list.append(pd.read_csv('log/20260608/popsize100/_MA_100_06080201_best_record.csv'))
    print(MA_list[2])
    df = pd.merge(df, MA_list[2], on='eval_count', how='outer')
    df = df.ffill()
    print(df)
    
    df = df.set_index('eval_count')
    df['mean'] = df.mean(axis=1)
    df['std'] = df.std(axis=1)
    print(df)
    # plot
    fig, ax = plt.subplots(figsize=(10, 6))
    df['mean'].plot(ax=ax, color='blue', marker='o', label='GA')
    ax.fill_between(
        df.index,
        np.clip(df["mean"] - df["std"], 0, None),
        df["mean"] + df["std"],
        color="blue",
        alpha=0.15,
    )
    plt.legend(loc='best', fontsize=10)
    plt.show()
