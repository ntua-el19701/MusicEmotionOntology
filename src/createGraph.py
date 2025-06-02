from rdflib import Graph, Namespace, RDF, URIRef, Literal
from rdflib.namespace import DC, XSD, RDF, RDFS
import os

def create_Graph(track, xml_file):
    """
    function that takes an MEO.Track instance and the xml file and creates a Knowledge Graph
    """
     # create an rdflib graph
    g = Graph()

    # define namespaces
    MEO = Namespace('http://www.semanticweb.org/musicEmotionOntology#')
    RDFNS = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    RDFSNS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
    DCNS = Namespace('http://purl.org/dc/elements/1.1/')

    # bind prefixes
    g.bind('meo', MEO)
    g.bind('rdf', RDFNS)
    g.bind('rdfs', RDFSNS)
    
    # extract the title of the xml file:
    base_name, extension = os.path.splitext(xml_file)
    title = os.path.basename(base_name)
    
    # create a uri for the track
    track_uri = URIRef(MEO + title)
    g.add((track_uri, RDF.type, MEO.Track))
    g.add((track_uri, DC.title, Literal(title)))

    