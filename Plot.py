import matplotlib.pyplot as plt
import csv


if __name__ == '__main__':
    plt.rcParams.update({'font.size': 12})
    MA_eval_count = []
    MA_scores = []
    # MA line 1
    with open('log/20260531/_MA_05311216_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        MA_eval_count.append(temp_eval_count)
        MA_scores.append(temp_scores)
    # MA line 2
    with open('log/20260531/_MA_05311220_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        MA_eval_count.append(temp_eval_count)
        MA_scores.append(temp_scores)
    # MA line 3
    with open('log/20260531/_MA_05311224_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        MA_eval_count.append(temp_eval_count)
        MA_scores.append(temp_scores)

    GA_eval_count = []
    GA_scores = []
    # GA line 1
    with open('log/20260531/_GA_05311216_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA_eval_count.append(temp_eval_count)
        GA_scores.append(temp_scores)
    # GA line 2
    with open('log/20260531/_GA_05311221_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA_eval_count.append(temp_eval_count)
        GA_scores.append(temp_scores)
    # GA line 3
    with open('log/20260531/_GA_05311226_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA_eval_count.append(temp_eval_count)
        GA_scores.append(temp_scores)

    # plot
    markers = ['o', '^', 's']
    for i in range(len(MA_eval_count)):
        plt.plot(MA_eval_count[i], MA_scores[i], 'ro-', marker=markers[i], label=f'MA line {i}')
        plt.plot(GA_eval_count[i], GA_scores[i], 'go-', marker=markers[i], label=f'GA line {i}')
    plt.legend(loc='best', fontsize=10)
    plt.show()
