# Query 7: Find the musical features of very postiive valence meters


"""
PREFIX meo: <http://www.semanticweb.org/musicEmotionOntology#>

SELECT ?mf (COUNT(?meter) AS ?meterCount)
WHERE {
    ?meter a meo:VeryPositiveValenceMeter;
    meo:hasMusicalFeature ?mf.
}

GROUP BY ?mf
ORDER BY DESC(?meterCount)
"""