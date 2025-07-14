# Query 6: Find the most commonly used intervals by a composer (e,g, Bach)

"""
PREFIX meo: <http://www.semanticweb.org/musicEmotionOntology#>

SELECT ?mf (COUNT(?mf) as ?a) 
WHERE {
    ?meter meo:hasMusicalFeature ?i.
    ?i meo:hasInterval ?mf .
    ?i meo:hasIntervalCount ?c
    FILTER REGEX(STR(?meter), "Bach")
}
GROUP BY(?mf) ORDER BY DESC(?a)
"""

import pandas as pd
import re
import matplotlib.pyplot as plt


interval_order = ['unison', 'minorsecond', 'majorsecond', 'minorthird',
                  'majorthird', 'perfectfourth', 'augmentedfourth', 'perfectfifth',
                  'minorsixth', 'majorsixth', 'minorseventh', 'majorseventh',
                  'octave']

def get_mfs_and_counts(file_path):
    df = pd.read_csv(file_path)
    mfs = df['mf'].tolist()  # Get list of musical features (mf)
    counts = df['a'].tolist()  # Get list of counts
    l = []
    for c in counts:
        c = c  # total number of meters
        l.append(c)
    counts = l
    cleaned_mfs = []
    for mf in mfs:
        # Extract the relevant part of the mf using regex
        result = re.search(r"#(.*?)interval", mf).group(1)
        cleaned_mfs.append(result)

    return cleaned_mfs, counts


def plotThis(cleaned_mfs, counts, composer):
    # Ensure the intervals are in the correct order
    df = pd.DataFrame({'interval': cleaned_mfs, 'count': counts})
    df['interval'] = pd.Categorical(df['interval'], categories=interval_order, ordered=True)
    df = df.sort_values('interval')  # Sort by the predefined interval order

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(df['interval'], df['count'], color='green')  # Now the intervals are on the y-axis

    # Set labels and title
    plt.xlabel('Interval')
    plt.ylabel('Interval Count')
    plt.title('Sum of every interval used by ' + composer)
    plt.xticks(rotation=45)
    # Show the plot
    plt.tight_layout()
    plt.show()


bach_mfs, bach_counts = get_mfs_and_counts('Bach_intervals.csv')
beet_mfs, beet_counts = get_mfs_and_counts('Beethoven_intervals.csv')
chopin_mfs, chopin_counts = get_mfs_and_counts('Chopin_intervals.csv')
haydn_mfs, haydn_counts = get_mfs_and_counts('Haydn_intervals.csv')

#plotThis(bach_mfs, bach_counts, 'Bach')
#plotThis(beet_mfs, beet_counts, 'Beethoven')
#plotThis(chopin_mfs, chopin_counts, 'Chopin')
#plotThis(haydn_mfs, haydn_counts, 'Haydn')