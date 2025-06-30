import matplotlib.pyplot as plt
import numpy as np

def smooth_curve(values, window_size=3):
    return np.convolve(values, np.ones(window_size) / window_size, mode='same')

def plot_valence_arousal(valence, arousal, num_meters, name):
    print(valence,arousal, len(valence), len(arousal))
    if len(valence) != num_meters or len(arousal) != num_meters:
        raise ValueError("Length of valence and arousal arrays must match num_meters")

    meters = list(range(1, num_meters + 1))  # e.g., [1, 2, 3, ..., num_meters]

    valence_smoothed = smooth_curve(valence, window_size=3)
    arousal_smoothed = smooth_curve(arousal, window_size=3)

    plt.figure(figsize=(10, 6))
    
    plt.plot(meters, valence_smoothed, label='Valence',  color='blue')
    plt.plot(meters, arousal_smoothed, label='Arousal',  color='red')
    
    plt.title(f'Valence and Arousal Over Time of {name}')
    plt.xlabel('Meter')
    plt.ylabel('Value')
    plt.xticks(meters)
    plt.ylim(min(min(valence), min(arousal)) - 0.1, max(max(valence), max(arousal)) + 0.1)
    plt.legend()
    plt.tight_layout()
    #plt.show()
    plt.savefig(f"Plots/{name}_plot.png")

