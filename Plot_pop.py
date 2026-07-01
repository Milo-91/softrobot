import numpy as np
import matplotlib.pyplot as plt
import json

if __name__ == '__main__':
    population_files_list = [
        "20260701/popsize100/from_eclab/3/ObstacleTraverser-v1T_ES_20_07020113_1_1"
    ]
    
    for file in population_files_list:
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize = (18, 7.3))
        plt.rcParams.update({'font.size': 14})

        fitness_history = []
        top_10_fitness_history = []
        with open('log/' + file + '_population_record.jsonl') as f:
            for line in f:
                data = json.loads(line)
                fitness_history.append(data["fitness"])
                top_10_fitness_history.append(data["fitness"][:max(int(len(top_10_fitness_history)*0.1), 1)])
        all_fitness = np.concatenate(fitness_history)
        f_max = all_fitness.max()
        f_min = all_fitness.min()

        bins = np.linspace(
            f_min,
            f_max,
            11
        )

        # all population heatmap
        heatmap = []
        for pop in fitness_history:
            hist, _ = np.histogram(pop, bins=bins)
            print(hist)
            hist = hist / len(pop) # change into percentage
            heatmap.append(hist)

        heatmap = np.array(heatmap)
        img = ax[0].imshow(
            heatmap.T,
            aspect = 'auto',
            origin = 'lower',
            extent = (0, len(fitness_history), f_min, f_max),
            cmap = 'plasma'
        )    
        
        ax[0].set_title("Population distribution")
        ax[0].set_xlabel("Generation")
        ax[0].set_ylabel("Fitness")
        fig.colorbar(img, ax=ax[0])

        
        # top 10 heatmap
        top_10_all_fitness = np.concatenate(top_10_fitness_history)
        top_10_f_max = top_10_all_fitness.max()
        top_10_f_min = top_10_all_fitness.min()

        top_10_bins = np.linspace(
            top_10_f_min,
            top_10_f_max,
            11
        )

        top_10_heatmap = []
        for pop in top_10_fitness_history:
            hist, _ = np.histogram(pop, bins=top_10_bins)
            print(hist)
            hist = hist / len(pop) # change into percentage
            top_10_heatmap.append(hist)

        top_10_heatmap = np.array(top_10_heatmap)
        top_10_img = ax[1].imshow(
            top_10_heatmap.T,
            aspect = 'auto',
            origin = 'lower',
            extent = (0, len(top_10_fitness_history), top_10_f_min, top_10_f_max),
            cmap = 'plasma'
        )    
        
        ax[1].set_title("Top 10 distribution")
        ax[1].set_xlabel("Generation")
        ax[1].set_ylabel("Fitness")
        fig.colorbar(top_10_img, ax=ax[1])

        plt.show()
