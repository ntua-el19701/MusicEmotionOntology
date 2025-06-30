from music21 import converter, stream

# Dictionary mapping measure ranges to new file names
measure_ranges = {
    "1-12": "Ionian",
    "13-20": "Dorian",
    "21-28": "Frygian",
    "29-40": "Lydian",
    "41-48": "Mixolydian",
    "49-56": "Aeolian",
    "57-64": "Locrian"
}

def split_musicxml_by_measures(input_file, measure_ranges):
    """
    Function that splits the modes xml file into many based on the measure ranges dictionary
    """
    # Parse the input MusicXML file
    score = converter.parse(input_file)

    # Get the part(s) (assumes single part for simplicity, can be extended)
    parts = score.parts

    for measure_range, name in measure_ranges.items():
        start, end = map(int, measure_range.split('-'))
        # Create a new score to hold the measures for this segment
        new_score = stream.Score()

        for part in parts:
            new_part = stream.Part()
            measures = part.measures(start, end)

           
            # Flatten to access elements directly
            measures = measures.flatten().makeMeasures()
            for i, m in enumerate(measures.getElementsByClass('Measure'), start=1):
                m.number = i
                new_part.append(m)
            
            new_score.append(new_part)

        # Write the new score to a MusicXML file
        output_filename = f"xmlFiles/{name}.xml"
        new_score.write('xml', fp=output_filename)
        print(f"Written: {output_filename}")

# Example usage
split_musicxml_by_measures("xmlFiles\Modes.xml", measure_ranges)