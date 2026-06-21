import numpy as np
import matplotlib.pyplot as plt
import json

if __name__ == '__main__':
    population_files_list = [
        '20260621/test/_GA_100_06212144'
    ]
    
    for file in population_files_list:
        plt.figure(figsize = (18, 7.3))
        plt.rcParams.update({'font.size': 14})

        fitness_history = []
        with open('log/' + file + '_population_record.jsonl') as f:
            for line in f:
                data = json.loads(line)
                fitness_history.append(data["fitness"])
        all_fitness = np.concatenate(fitness_history)
        f_max = all_fitness.max()
        f_min = all_fitness.min()

        bins = np.linspace(
            f_min,
            f_max,
            11
        )

        heatmap = []
        for pop in fitness_history:
            hist, _ = np.histogram(pop, bins=bins)
            print(hist)
            
            hist = hist / len(pop) # change into percentage

            heatmap.append(hist)
        heatmap = np.array(heatmap)
        img = plt.imshow(
            heatmap.T,
            aspect = 'auto',
            origin = 'lower',
            extent = (0, len(fitness_history), f_min, f_max),
            cmap = 'plasma'
        )    
        
        plt.title("Population distribution")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.colorbar(img)
        plt.show()
