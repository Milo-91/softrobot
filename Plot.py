import matplotlib.pyplot as plt
import csv


if __name__ == '__main__':
    plt.rcParams.update({'font.size': 12})
      
    MA_eval_count = []
    MA_scores = []
    # MA line 1
    with open('log/20260608/popsize100/_MA_100_06080128_best_record.csv', newline='') as f:
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
    with open('log/20260608/popsize100/_MA_100_06080144_best_record.csv', newline='') as f:
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
    with open('log/20260608/popsize100/_MA_100_06080201_best_record.csv', newline='') as f:
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
    with open('log/20260609/popsize100/_MA_Hill_Climbing_100_06081552_best_record.csv', newline='') as f:
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
    with open('log/20260609/popsize100/_MA_Hill_Climbing_100_06081605_best_record.csv', newline='') as f:
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
    with open('log/20260609/popsize100/_MA_Hill_Climbing_100_06081618_best_record.csv', newline='') as f:
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
    with open('log/20260609/popsize100/_MA_Tabu_Search_100_06081553_best_record.csv', newline='') as f:
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
    with open('log/20260609/popsize100/_MA_Tabu_Search_100_06081606_best_record.csv', newline='') as f:
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
    with open('log/20260609/popsize100/_MA_Tabu_Search_100_06081618_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA200_eval_count.append(temp_eval_count)
        GA200_scores.append(temp_scores)
    '''
    GA200_eval_count = []
    GA200_scores = []
    # GA line 1
    with open('log/20260608/popsize100/_GA_Tabu_Search_100_06080232_best_record.csv', newline='') as f:
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
    with open('log/20260608/popsize100/_GA_Tabu_Search_100_06080238_best_record.csv', newline='') as f:
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
    with open('log/20260608/popsize100/_GA_Tabu_Search_100_06080251_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA200_eval_count.append(temp_eval_count)
        GA200_scores.append(temp_scores)


    GA_eval_count = []
    GA_scores = []
    # GA line 1
    with open('log/20260608/popsize200/_GA_Tabu_Search_200_06081055_best_record.csv', newline='') as f:
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
    with open('log/20260608/popsize200/_GA_Tabu_Search_200_06081117_best_record.csv', newline='') as f:
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
    with open('log/20260608/popsize200/_GA_Tabu_Search_200_06081105_best_record.csv', newline='') as f:
        spamreader = csv.reader(f)
        next(spamreader)
        temp_eval_count = []
        temp_scores = []
        for row in spamreader:
            temp_eval_count.append(int(row[0]))
            temp_scores.append(float(row[1][:5]))
        GA_eval_count.append(temp_eval_count)
        GA_scores.append(temp_scores)
    '''
    # plot
    markers = ['o', '^', 's']
    for i in range(len(GA_eval_count)):
        plt.plot(MA_eval_count[i], MA_scores[i], 'ro-', marker=markers[i], label=f'GA {i}')
        plt.plot(GA_eval_count[i], GA_scores[i], 'go-', marker=markers[i], label=f'GA+HC {i}')
        plt.plot(GA200_eval_count[i], GA200_scores[i], 'bo-', marker=markers[i], label=f'GA+TS {i}')
    plt.legend(loc='best', fontsize=10)
    plt.show()
