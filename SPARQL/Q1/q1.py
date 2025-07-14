
#  Query 1:Find the overall valence and arousal values of musical pieces written by a specific composer (e.g. Bach)

"""
PREFIX meo: <http://www.semanticweb.org/musicEmotionOntology#>

SELECT (Avg(?valence) as ?avgval) (AVG(?arousal) as ?avgar)
    WHERE {
        SELECT ?meter ?valence ?arousal {
            ?meter a meo:Track ;
                    meo:trackHasAverageValence ?valence ;
                    meo:trackHasAverageArousal ?arousal
            FILTER REGEX(str(?meter), "Bach")
        }
    }
"""

from matplotlib import pyplot as plt


beet_val = 2.022482142857142857142857
beet_ar = -0.256660714285714285714286

bach_val = 0.187491228070175438596491
bach_ar = -2.251649122807017543859649

haydn_val = 2.583181818181818181818182
haydn_ar = -0.128090909090909090909091

chop_val = 0.413
chop_ar = 0.819368421052631578947368

# Composer names
composers = ['Beethoven', 'Bach', 'Haydn', 'Chopin']

# Valence and arousal values
valence = [beet_val, bach_val, haydn_val, chop_val]
arousal = [beet_ar, bach_ar, haydn_ar, chop_ar]

# Create scatter plot
plt.figure(figsize=(8,6))
plt.scatter(valence, arousal, color='blue')

# Annotate each point with the composer's name
for i, composer in enumerate(composers):
    plt.text(valence[i] + 0.05, arousal[i] + 0.05, composer, fontsize=12)

# Set labels and title
plt.xlabel('Valence')
plt.ylabel('Arousal')
plt.title('Average Valence and Arousal values of Composers')

# Show grid
plt.grid(True)

# Show the plot
plt.show()