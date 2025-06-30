# Music Emotion Ontology 

An ontology that links musical features with emotional responses. 

## Ontology file

The .owl file can be found under the ontology directory

## Python scripts

### MusicEmotionOntology.py

The ontology using the library owlready2

### parseXML.py

Takes as input a xml/musicxml file, parses it and creates ontology instances. Then it uses the properties linking them with emotions and calculates valence and arousal values for every meter. It also creates a plot that shows how valence and arousal change over time - measures.

## xmlFiles

Contains a small amount of xml files, including Greensleeves.