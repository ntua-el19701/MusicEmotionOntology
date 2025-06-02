import matplotlib.pyplot as plt


def plot_valence_arousal(valence, arousal, num_meters):
    print(valence,arousal, len(valence), len(arousal))
    if len(valence) != num_meters or len(arousal) != num_meters:
        raise ValueError("Length of valence and arousal arrays must match num_meters")

    meters = list(range(1, num_meters + 1))  # e.g., [1, 2, 3, ..., num_meters]

    plt.figure(figsize=(10, 6))
    
    plt.plot(meters, valence, label='Valence', marker='o', color='blue')
    plt.plot(meters, arousal, label='Arousal', marker='s', color='red')
    
    plt.title('Valence and Arousal Over Time')
    plt.xlabel('Meter')
    plt.ylabel('Value')
    plt.xticks(meters)
    plt.ylim(min(min(valence), min(arousal)) - 0.1, max(max(valence), max(arousal)) + 0.1)
    plt.legend()
    plt.tight_layout()
    plt.show()


