import matplotlib.pyplot as plt
import json


popsize = []
gen_count = []
with open('log/20260622/popsize100/_GA_100_06221141_population_record.jsonl') as f:
    for line in f:
        data = json.loads(line)
        popsize.append(len(data['fitness']))
        gen_count.append(data['gen'])

plt.plot(gen_count, popsize, linewidth=5)

plt.xlabel("Generation")
plt.ylabel("Population Size")
plt.show()
