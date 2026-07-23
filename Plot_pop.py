import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import json
import pandas as pd

if __name__ == '__main__':
    population_files_list = [
        "20260722/popsize100/ObstacleTraverser-v0T/MA+ES/ObstacleTraverser-v0T_MA_ES_100_07221453_1_1",
        "20260722/popsize100/ObstacleTraverser-v0T/MA+ES/ObstacleTraverser-v0T_MA_ES_100_07221510_1_1",
        "20260722/popsize100/ObstacleTraverser-v0T/MA+ES/ObstacleTraverser-v0T_MA_ES_100_07221518_1_1",
        "20260722/popsize100/ObstacleTraverser-v0T/MA+ES/ObstacleTraverser-v0T_MA_ES_100_07221501_1_1",
    ]
    
    for file in population_files_list:
        plt.rcParams.update({'font.size': 14})
        fig = plt.figure(figsize = (18, 7.3))
        gs = fig.add_gridspec(nrows=2, ncols=4, width_ratios=[20, 1, 20, 1], height_ratios=[2, 1])
        ax_heat = fig.add_subplot(gs[0, 0])
        ax_sim = fig.add_subplot(gs[1, 0])
        ax_sim.margins(x = 0)
        ax_colorbar = fig.add_subplot(gs[0, 1])
        ax_10heat = fig.add_subplot(gs[0, 2])
        ax_10colorbar = fig.add_subplot(gs[0, 3])
        ax_sim2 = fig.add_subplot(gs[1, 2])
        ax_sim2.margins(x = 0)

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
        img = ax_heat.imshow(
            heatmap.T,
            aspect = 'auto',
            origin = 'lower',
            extent = (0, len(fitness_history), f_min, f_max),
            cmap = 'plasma'
        )    
        
        ax_heat.set_title("Population Heatmap")
        ax_heat.set_xlabel("Generation")
        ax_heat.set_ylabel("Fitness")
        fig.colorbar(img, cax=ax_colorbar)

        
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
        top_10_img = ax_10heat.imshow(
            top_10_heatmap.T,
            aspect = 'auto',
            origin = 'lower',
            extent = (0, len(top_10_fitness_history), top_10_f_min, top_10_f_max),
            cmap = 'plasma'
        )    
        
        ax_10heat.set_title("Top 10 Heatmap")
        ax_10heat.set_xlabel("Generation")
        ax_10heat.set_ylabel("Fitness")
        fig.colorbar(top_10_img, cax=ax_10colorbar)


        # similarity
        similarity = pd.read_csv('log/' + file + '_similarity_record.csv')
        similarity = similarity.set_index('eval_count')
        print(similarity)
        similarity['similarity'].plot(ax=ax_sim, color='blue', marker='o', label='eval_count')
        ax_sim.set_xlabel("eval count")
        ax_sim.set_ylabel("Similarity")
        similarity['similarity'].plot(ax=ax_sim2, color='blue', marker='o', label='eval_count')
        ax_sim2.set_xlabel("eval count")
        ax_sim2.set_ylabel("Similarity")

        plt.tight_layout()
        plt.show()
