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
    plt.figure(figsize=(15,10))
    plt.barh(cleaned_mfs, counts, color='red')

    # Set labels and title
    plt.xlabel('Usage Count')
    plt.ylabel('Musical Features')
    plt.title('Usage of Musical Features by ' + composer)

    # Show the plot
    plt.show()

# Read data for each composer
bach_mfs, bach_counts = get_mfs_and_counts('bach_mfs.csv')
beet_mfs, beet_counts = get_mfs_and_counts('beet_mfs.csv')
chopin_mfs, chopin_counts = get_mfs_and_counts('chopin_mfs.csv')
haydn_mfs, haydn_counts = get_mfs_and_counts('haydn_mfs.csv')

#plotThis(bach_mfs, bach_counts, 'Bach')
#plotThis(beet_mfs, beet_counts, 'Beethoven')
#plotThis(chopin_mfs, chopin_counts, 'Chopin')
#plotThis(haydn_mfs, haydn_counts, 'Haydn')