# Query 4: Count meters with dynamic shape by a composer (e.g. Beethoven)

"""
PREFIX meo: <http://www.semanticweb.org/musicEmotionOntology#>

SELECT ?mf (COUNT(?meter) as ?count)
WHERE {
    ?meter meo:hasMusicalFeature ?mf .
    ?meter meo:hasArousalValue ?a
    VALUES ?mf { meo:crescendo_instance meo:diminuendo_instance }
    FILTER REGEX(str(?meter), "Beethoven")

} GROUP BY(?mf)
"""

import matplotlib.pyplot as plt
import numpy as np

# Data for composers
composers = ['Beethoven', 'Bach', 'Haydn', 'Chopin']
crescendo = [64, 0, 13, 98]
diminuendo = [125, 0, 19, 95]

# Create figure and axis
fig, ax = plt.subplots()

# Set positions for bars
bar_width = 0.35
index = np.arange(len(composers))

# Crescendo bars (left group)
cres_bars = ax.bar(index, crescendo, bar_width, label='Crescendo', color='skyblue')

# Diminuendo bars (right group)
dim_bars = ax.bar(index + bar_width, diminuendo, bar_width, label='Diminuendo', color='salmon')

# Add labels, title, and ticks
ax.set_xlabel('Composers')
ax.set_ylabel('Dynamic Shape Values')
ax.set_title('Crescendo and Diminuendo for Various Composers')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(composers)

# Add legend
ax.legend()

# Display the graph
plt.tight_layout()
plt.show()