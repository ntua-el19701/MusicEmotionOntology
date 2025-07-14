# Query 6: Find Very Positive Valence Meters that their next meter has Low Negative Valence
""" 
PREFIX meo: <http://www.semanticweb.org/musicEmotionOntology#>

SELECT ?meter1 ?v1 ?meter2 ?v2
WHERE{
    ?meter1 a meo:VeryPositiveValenceMeter ;
    		meo:hasValenceValue ?v1 ;
    		meo:hasNextMeter ?meter2 .
    ?meter2 a meo:LowNegativeValenceMeter ;
			meo:hasValenceValue ?v2 ;

}
"""