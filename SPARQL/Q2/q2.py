#  Query 2: Find the most commonly used musical features by every composer (e.g. Bach)

"""
PREFIX meo: <http://www.semanticweb.org/musicEmotionOntology#>

SELECT ?mf (COUNT(?mf) as ?c)
WHERE{
    ?meter a meo:Meter;
		meo:hasMusicalFeature ?mf
	FILTER REGEX(str(?meter), "Bach") 
}
GROUP BY ?mf HAVING(?c > 2) ORDER BY DESC(?c)
"""


import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np


def get_mfs_and_counts(file_path):
    """ Function to clean MFs and extract counts for a composer """

    df = pd.read_csv(file_path).head(10)  # Limit to first 20 rows
    mfs = df['mf'].tolist()  # Get list of musical features (mf)
    counts = df['c'].tolist()  # Get list of counts

    cleaned_mfs = []
    for mf in mfs:
        # Extract the relevant part of the mf using regex
        result = re.search(r"#(.*?)_instance", mf).group(1)
        cleaned_mfs.append(result)

    return cleaned_mfs, counts


def plotThis(cleaned_mfs, counts, composer):
    plt.figure(figsize=(28,20))  # Keeping the larger figure size
    plt.barh(cleaned_mfs, counts, color='blue')

    # Set labels and title with larger font sizes
    plt.xlabel('Usage Count', fontsize=22)  # Increased font size for x-axis label
    plt.ylabel('Musical Features', fontsize=22)  # Increased font size for y-axis label
    #plt.title('Usage of Musical Features by ' + composer, fontsize=24)  # Increased font size for title

    # Increase font size for tick labels
    plt.tick_params(axis='both', labelsize=20)  # Adjusts size of tick labels on both axes

    # Show the plot
    #plt.show()
    plt.savefig('SPARQL/Q2/plot2_' + composer + '.pdf')  # Save the plot with composer name

# Read data for each composer
bach_mfs, bach_counts = get_mfs_and_counts('SPARQL/Q2/bach_mfs.csv')
#beet_mfs, beet_counts = get_mfs_and_counts('beet_mfs.csv')
#chopin_mfs, chopin_counts = get_mfs_and_counts('SPARQL\Q2\chopin_mfs.csv')
#haydn_mfs, haydn_counts = get_mfs_and_counts('haydn_mfs.csv')

plotThis(bach_mfs, bach_counts, 'Bach')
#plotThis(beet_mfs, beet_counts, 'Beethoven')
#plotThis(chopin_mfs, chopin_counts, 'Bach')
#plotThis(haydn_mfs, haydn_counts, 'Haydn')