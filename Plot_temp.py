import matplotlib.pyplot as plt
import json


popsize = []
gen_count = []
with open('log/20260628/from_eclab/Climber-v0T/r0.3_t32.0/Climber-v0T_GA_100_06271525_0.3_32.0_population_record.jsonl') as f:
    for line in f:
        data = json.loads(line)
        popsize.append(len(data['fitness']))
        gen_count.append(data['gen'])

plt.plot(gen_count, popsize, linewidth=5)

plt.xlabel("Generation")
plt.ylabel("Population Size")
plt.show()
