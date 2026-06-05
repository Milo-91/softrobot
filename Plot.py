import matplotlib.pyplot as plt
import csv


if __name__ == '__main__':
    plt.rcParams.update({'font.size': 12})
    MA_eval_count = []
    MA_scores = []
    # MA line 1
    with open('log/20260604/popsize100/_GA_06041633_best_record.csv', newline='') as f:
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
    with open('log/20260604/popsize100/_GA_06041639_best_record.csv', newline='') as f:
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
    with open('log/20260604/popsize100/_GA_06041645_best_record.csv', newline='') as f:
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
    with open('log/20260604/popsize20/_GA_06041749_best_record.csv', newline='') as f:
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
    with open('log/20260604/popsize20/_GA_06041756_best_record.csv', newline='') as f:
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
    with open('log/20260604/popsize20/_GA_06041803_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA_eval_count.append(temp_eval_count)
        GA_scores.append(temp_scores)

    GA200_eval_count = []
    GA200_scores = []
    # GA line 1
    with open('log/20260604/popsize200/_GA_06051313_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA200_eval_count.append(temp_eval_count)
        GA200_scores.append(temp_scores)
    # GA line 2
    with open('log/20260604/popsize200/_GA_06051319_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA200_eval_count.append(temp_eval_count)
        GA200_scores.append(temp_scores)
    # GA line 3
    with open('log/20260604/popsize200/_GA_06051325_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA200_eval_count.append(temp_eval_count)
        GA200_scores.append(temp_scores)

    # plot
    markers = ['o', '^', 's']
    for i in range(len(MA_eval_count)):
        plt.plot(GA200_eval_count[i], GA200_scores[i], 'bo-', marker=markers[i], label=f'GA popsize=200 {i}')
        plt.plot(MA_eval_count[i], MA_scores[i], 'ro-', marker=markers[i], label=f'GA popsize=100 {i}')
        plt.plot(GA_eval_count[i], GA_scores[i], 'go-', marker=markers[i], label=f'GA popsize=20 {i}')
    plt.legend(loc='best', fontsize=10)
    plt.show()
