# Query 5 : Find musical features of a meter type (e.g. VeryPositiveValence Mete)
"""
PREFIX meo: <http://www.semanticweb.org/musicEmotionOntology#>

SELECT ?meter ?mf ?interval ?c
WHERE {
    ?meter a mfonto:LowPositiveValenceMeter;
           mfonto:hasMusicalFeature ?mf.

    OPTIONAL{
    	?mf mfonto:hasInterval ?interval .
    	?mf mfonto:hasIntervalCount ?c.
    }

}
"""