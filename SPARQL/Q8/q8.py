# Query 8: Find musical features in Very Positive Valence meters that have minor mode
"""
PREFIX : <http://www.semanticweb.org/musicEmotionOntology>

SELECT ?commonMf (COUNT(?meter) AS ?meterCount)
WHERE {
    # Find the meters that have a musical feature matching "minorm"
    {
        SELECT DISTINCT ?meter
        WHERE {
            ?meter a meo:VeryPositiveValenceMeter;
                   meo:hasMusicalFeature ?mf.
            FILTER (REGEX(str(?mf), "minorm"))
        }
    }

    # Retrieve all musical features of these meters
    ?meter meo:hasMusicalFeature ?commonMf.
}
GROUP BY ?commonMf
ORDER BY DESC(?meterCount)"""