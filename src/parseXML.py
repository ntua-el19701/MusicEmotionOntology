from owlready2 import sync_reasoner_pellet
import MusicEmotionOntology as meo
import os
from music21 import converter, analysis, tempo, dynamics
import xml.etree.ElementTree as ET
from pathlib import Path
from create_plot import plot_valence_arousal

# create a graph and create instances of the relative Ontology classes of the musical features found in the file
# use these instanes to calculate valence and arousal scores

# function that finds the total number of measures
def count_measures(xml_file):
    # Parse the MusicXML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # Find all measure elements
    measures = root.findall(".//measure")
    # Count the number of measure elements
    measure_count = len(measures)

    first_measure_number = measures[0].get("number") if measures else None

    return measure_count, int(first_measure_number)

def get_mode(score):
    """
    function that uses KrumhanslSchumckler algorithm to find the mode of a musical score
    """
    # Iterate through metadata elements in the score
    key_analyzer = analysis.discrete.KrumhanslSchmuckler()
    # Analyze the key using the analyzer
    key = key_analyzer.getSolution(score)

    mode = key.mode
    if mode == 'major':
        return meo.MajorMode
    elif mode == 'minor':
        return meo.MinorMode

    return None

def get_tempo(score):
    """
    function that finds the tempo of musical score
    """

    tempo_marks = score.recurse().getElementsByClass(tempo.MetronomeMark)
    if tempo_marks:
        bpm = tempo_marks[0].number
        if bpm is None:
            return None, None
        if bpm != 0:
            if 20 <= bpm <= 40:
                return meo.Grave, bpm
            elif 40 < bpm <= 55:
                return meo.LargoTempo, bpm
            elif 55 < bpm <= 71:
                return meo.Adagio, bpm
            elif 71 < bpm <= 108:
                return meo.Andante, bpm
            elif 108 < bpm <= 120:
                return meo.Moderato, bpm
            elif 120 < bpm <= 156:
                return meo.AllegroTempo, bpm
            elif 156 < bpm <= 168:
                return meo.Vivace, bpm
            elif 168 < bpm <= 200:
                return meo.PrestoTempo, bpm
            else:
                return meo.Prestissimo, bpm
    return None, None

def find_dynamic_shape_time_signature(file_path, target_measure_number):
    """
    Function that finds dynamic shape, rhythmic change and time signature of a meter 
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    measure_xpath = f'.//measure[@number="{target_measure_number}"]'
    target_measure = root.find(measure_xpath)
    rhythm_change = None
    dynamic_shape = None
    time_signature = None
    if target_measure is not None:

        attributes_elem = target_measure.find('attributes')
        if attributes_elem is not None:
            time_elem = attributes_elem.find('time')
            if time_elem is not None:
                beats_per_measure = int(time_elem.find('beats').text)
                beat_type = int(time_elem.find('beat-type').text)
                time_signature = (beats_per_measure, beat_type)
        # Iterate through directions within the measure
        for direction in target_measure.findall('.//direction'):
            # Check for direction-type element within the direction
            direction_type = direction.find('./direction-type')
            if direction_type is not None:
                # Iterate through all wedge elements within direction-type
                for wedge in direction_type.findall('./wedge'):
                    wedge_type = wedge.attrib.get('type', '')
                    if wedge_type == "crescendo":
                        dynamic_shape = meo.Crescendo
                    elif wedge_type == "diminuendo":
                        dynamic_shape = meo.Diminuendo
                for words in direction_type.findall(
                        './words'):  # to find words on the staff often related with rhythm change
                    if words.text == 'accel' or words.text == 'accel.':
                        rhythm_change = meo.Accelerando
                    elif words.text == 'rit' or words.text == 'rit.':
                        rhythm_change = meo.Ritardando
                    elif words.text == 'riten.' or words.text == 'riten':
                        rhythm_change = meo.Ritenuto
                    elif words.text == 'cresc':
                        dynamic_shape = meo.Crescendo
                    elif words.text == 'dim':
                        dynamic_shape = meo.Diminuendo
    return dynamic_shape, rhythm_change, time_signature

def find_articulations(note_element):
    # Check if the note element has articulations
    arts = []
    articulations = note_element.articulations
    if articulations is not None:
        for a in articulations:
            art_name = a.__class__.__name__
            if art_name == "Accent":
                arts.append(meo.Accent)
            elif art_name == "Staccato":
                arts.append(meo.Staccato)
            elif art_name == "Legato":
                arts.append(meo.Legato)
            elif art_name == "Tenuto":
                arts.append(meo.Tenuto)
    return arts


def note_in_chord(chord_notes):
    """
    function that gets a chord and returns the chord with the highset pitch 
    """
    highest_chord_note = chord_notes[0]
    # print(chord_notes)
    for n in chord_notes:
        if 'Note' in n.classes:
            if n.octave > highest_chord_note.octave:  # find the note with the highest pitch
                highest_chord_note = n
            elif n.octave == highest_chord_note.octave and n.pitch > highest_chord_note.pitch:
                highest_chord_note = n
    return highest_chord_note

def find_dynamics(element):
    """
    function that finds the dynamics
    """
    if isinstance(element, dynamics.Dynamic):
        dyn = element.value
        if dyn == 'pp':
            return meo.Pianissimo
        elif dyn == 'p':
            return meo.Piano
        elif dyn == 'mp' or dyn == 'm':
            return meo.MezzoPiano
        elif dyn == 'mf':
            return meo.MezzoForte
        elif dyn == 'f':
            return meo.Forte
        elif dyn == 'ff':
            return meo.Fortissimo
    return None

def get_measure_notes(file, score, i):
    """
    Function that gets the score and a measure number and finds for the first part:
        - notes 
        - chords
        - dynamics
        - articulations
    """

    # find the first part
    first_part = score.parts[0]
    # if there are 2 staves, we find the second part as well 
    second_part = None  
    if len(score.parts) == 2:  
        second_part = score.parts[1]

    # the function will find these:
    notes = []
    chords = []
    rests = []
    dynamics = []
    articulations = []

    # if there is no measure numbered i in the first part then we exit the function
    if first_part.measure(i) is None:
        return None, None, None, None, None
    
    # get measure's first part
    measure_first_part = first_part.measure(i)
    # flag to know if the measure uses the voice feature   
    voice_found = False

    # iterate through each element of the measure (first part)
    for element in measure_first_part.recurse():  
        if 'Voice' in element.classes:
            voice_found = True
        # if the element is a chord
        if 'Chord' in element.classes:  
            chords.append(element)
            # use this chord if the voice that it follows is '1' or if it does not follow any voice
            parent_voice = element.getContextByClass('Voice')
            voice = None
            if parent_voice is not None:
                voice = parent_voice.id
            if voice == '1' or voice == None or voice_found == False:
                # find the melody note of the chord and append it to the notes list
                n = note_in_chord(element)
                notes.append(n)  

        # if the element is a rest
        if 'Rest' in element.classes:  
            rests.append(element)

        # if the element is a dynamic
        if 'Dynamic' in element.classes:
            dyn = find_dynamics(element)  
            dynamics.append(dyn)
        
        # find the notes only for the first voice, or if there are no voices
        if 'Note' in element.classes:  
            parent_voice = element.getContextByClass('Voice')
            voice = None
            if parent_voice is not None:
                voice = parent_voice.id
            if voice == '1' or voice == "None" or voice_found == False:
                notes.append(element)  
            
            # find also if there are any artivculations    
            art = find_articulations(element)
            if art:
                for a in art:
                    articulations.append(a)

    # if the measure has a second part, we use this to only find dynamics and articulations
    if second_part:  
        measure_second_part = second_part.measure(i)  
        if measure_second_part is not None:
            for element in measure_second_part.recurse():
                if 'Note' in element.classes:  
                    art = find_articulations(element)
                    if art:
                        for a in art:
                            articulations.append(a)
                dyn = find_dynamics(element)  # find second part dynamics
                if dyn is not None:  # if they exist append it to dynamics list
                    dynamics.append(dyn)

    return notes, chords, rests, dynamics, articulations

def higher_lower(note1, note2):
    if note1.octave > note2.octave:
        return -1
    elif note1.octave < note2.octave:
        return +1
    else:
        if note1.pitch < note2.pitch:
            return +1
        elif note2.pitch < note1.pitch:
            return -1
        else:
            return 0


def note_to_midi(pitch):
    """Converts a music21 pitch object to a MIDI number."""
    return pitch.midi

def find_melody_direction_pitch_and_pitch_range(meter_notes, last_note):

    average_direction = 0
    average_pitch = None  # integer that will be returned
    avg_pitch = []  # list contain midi values for every note - middle C is 60
    sum_pitch = 0  # used to find the average pitch
    pitch_range = None  # value that will be returned
    for m_note in meter_notes:
        avg_pitch.append(note_to_midi(m_note.pitch))  # calls function to create the midi values
    if last_note is not None:
        average_direction += higher_lower(last_note, meter_notes[0])  # compute last note in the direction
    for i in range(0, len(meter_notes) - 1):
        average_direction += higher_lower(meter_notes[i], meter_notes[i + 1])
    if avg_pitch:
        for p in avg_pitch:
            sum_pitch += p
        average_pitch = sum_pitch / len(avg_pitch)  # calculate the average pitch
        highest_pitch = max(avg_pitch)
        lowest_pitch = min(avg_pitch)
        pitch_range = highest_pitch - lowest_pitch

    return average_direction, average_pitch, pitch_range

def calculate_interval(note1, note2):
    """
    function that takes 2 midi numbers as the notes and finds the interval between them
    """
    # Define the interval patterns
    interval_patterns = {
        0: meo.UnisonInterval,
        1: meo.MinorSecondInterval,
        2: meo.MajorSecondInterval,
        3: meo.MinorThirdInterval,
        4: meo.MajorThirdInterval,
        5: meo.PerfectFourthInterval,
        6: meo.AugmentedFourthInterval,
        7: meo.PerfectFifthInterval,
        8: meo.MinorSixthInterval,
        9: meo.MajorSixthInterval,
        10: meo.MinorSeventhInterval,
        11: meo.MajorSeventhInterval,
        12: meo.OctaveInterval

    }
    interval = abs(note1 - note2)
    if interval > 12:
        return interval_patterns[interval % 12]
    return interval_patterns[interval]

def find_intervals(note1, note2):

    # find the duration (e.g. quarter)
    d1 = note1.duration.type  
    d2 = note2.duration.type

    # find the biggest duration of the 2 notes
    if d1 >= d2:  
        interval_duration = d1  # this is now equal to the interval duration
    else:
        interval_duration = d2

    # caluclate the interval
    interval = calculate_interval(note_to_midi(note1.pitch), note_to_midi(note2.pitch)) 
    if interval != 'Invalid note':

        # append the duration in the hasDuration property
        interval.hasDuration = interval_duration  

        return interval
    return 'Invalid interval'

def find_weight(interval):  
    """
    function that takes an interval and assigns a weight based on its duration
    """
    # print("mf in weight", mf.hasDuration)
    if "whole" in interval.hasDuration:
        return 1.5
    elif "half" in interval.hasDuration:
        return 1.25
    elif "quarter" in interval.hasDuration:
        return 1
    elif "eighth" in interval.hasDuration:
        return 0.3
    elif "16th" in interval.hasDuration:
        return 0.15
    elif "32nd" in interval.hasDuration:
        return 0.075
    else:
        return 1

def bpm_to_arousal(bpm, min_bpm=30, max_bpm=220, min_arousal=-10, max_arousal=10):
    """
    function that takes a bom value ans calculates the change in arousal
    """
    # Ensure the bpm is within the expected range
    if bpm < min_bpm or bpm > max_bpm:
        raise ValueError(f"BPM should be between {min_bpm} and {max_bpm}")

    # Normalize the bpm to a value between 0 and 1
    normalized_bpm = (bpm - min_bpm) / (max_bpm - min_bpm)

    # Scale the normalized BPM to the arousal range
    arousal = normalized_bpm * (max_arousal - min_arousal) + min_arousal
    # print(arousal)
    return arousal

def calculate_tempo(tempo_cl):
    """
    used to calculate how much we increase/ decrease the arousal arousal
    """  
    print("tempo class", tempo_cl)
    increase = round(bpm_to_arousal(tempo_cl.hasBPM[0]), 3)

    return increase

def calculate_valence_arousal(track):
        """
        function that calculates valence and arousal based on the musical features of a track/meter
        """
        ar_value = 0
        val_value = 0
        mode_flag = None
        tempo_class = None
        for mf in track.hasMusicalFeature:

            if issubclass(mf.is_a[0], meo.Tempo):  # if it's about tempo we will calculate it later
                if mf.is_a[0] != meo.FastTempo and mf.is_a[0] != meo.SlowTempo and mf.is_a[0] != meo.MediumTempo:
                    tempo_class = mf.is_a[0]
                    continue

            # major Second Interval in major mode triggers different emotional stimuli
            if mode_flag == 'Major' and (mf == instances[meo.MajorSecondInterval] or mf == instances[meo.MinorSeventhInterval]):
                mf.triggers = []

            # major and minor modes are more important, so we check them separately
            if mf == instances[meo.MajorMode]:
                mode_flag = 'Major'
                val_value += 3
                continue
            if mf == instances[meo.MinorMode]:
                mode_flag = 'Minor'
                val_value -= 3
                continue
            if isinstance(mf, meo.Intervals):
                # find the weight depending on the duration of he interval
                weight = find_weight(mf)  
            else:
                weight = 1
            
            # for tone we don't want tone to change dramatically the outcome
            if isinstance(mf, meo.Tone): 
                weight = 0.5

            # set the rules for changing the values of valence and arousal
            for emotion in mf.triggers:
                if emotion == meo.VeryHighArousal:
                    ar_value += 2 * weight
                elif emotion == meo.HighArousal:
                    ar_value += 1.5 * weight
                elif emotion == meo.LowArousal:
                    ar_value -= 1.5 * weight
                elif emotion == meo.VeryLowArousal:
                    ar_value -= 2 * weight
                elif emotion == meo.VeryPositiveValence:
                    val_value += 2 * weight
                elif emotion == meo.MediumPositiveValence:
                    val_value += weight
                elif emotion == meo.LowNegativeValence:
                    val_value -= weight
                elif emotion == meo.VeryNegativeValence:
                    val_value -= 2 * weight
                elif emotion == meo.PositiveValence:
                    val_value += 1.5 * weight
                elif emotion == meo.NegativeValence:
                    val_value -= 1.5 * weight

        # finally calculate the arousal change of tempo
        ar_value += calculate_tempo(tempo_class)
        return ar_value, val_value

if __name__ == "__main__":

    # create instances for all ontology classes, this is important for reasoning
    instances = meo.create_instances()

    directory = Path("xmlFiles/")

    for xml_file in directory.rglob("*.xml"): 
        print("niaou")
        # parse a music XML file  
        #xml_file = 'xmlFiles/Frygian.xml'
        if not os.path.isfile(xml_file):
            print("Abort")
            break
        print(xml_file)
        score = converter.parse(xml_file)

        # create an instance of the meo.Track class for the Track
        base_name, extension = os.path.splitext(xml_file)
        title = os.path.basename(base_name)
        track = meo.Track(str(title))
        
        # find the mode of the score
        mode = get_mode(score)
        if mode:
            track.hasMode.append(mode)

        # find the tempo of the score and append it as a musical feature
        tempo_class, bpm = get_tempo(score)

        # manually append the tempo for the Modes piece
        if tempo_class is None:
            tempo_class = meo.Andante
            bpm=96

        if tempo_class:
            if bpm:
                tempo_class.hasBPM.append(bpm)
            track.hasTempo.append(instances[tempo_class])


        # this is to save the previous dynamic marking if there is not a new one in the current meter
        last_dynamic = None  
        last_note = None
        # used to check if the time signature changes
        last_time_signature = None  
        # save the average arousal for each meter
        avg_ar = {}  
        # saves the average valence for each meter
        avg_val = {}  

        meter_list = []
        # count measures
        num_of_measures, first_measure_num = count_measures(xml_file)
        print(first_measure_num,num_of_measures)
        for i in range(first_measure_num, num_of_measures +1):
            print("Meter", i)
            # create an instance for the meter:
            meter = meo.Meter(str(title) + "_Meter" + str(i))
            # append the meter to the meter list
            meter_list.append(meter)
            # connect the meter with its track
            meter.meterHasTrack.append(track)

            # append the mode and tempo to the meter
            if mode:
                meter.hasMode.append(instances[mode])
            if tempo_class:
                meter.hasTempo.append(instances[tempo_class])
                
            dynamic_shape, rhythm_change, time_signature = find_dynamic_shape_time_signature(xml_file, i)

            """if time_signature:
                meter.hasMusicalFeature.append(time_signature)
                last_time_signature = time_signature
            else:
                time_signature = last_time_signature
            """

            if dynamic_shape:
                meter.hasDynamicShape.append(dynamic_shape)
            if rhythm_change:
                meter.hasRhythmChange.append(rhythm_change)

            # find notes, chords, rests, dynamics and articulations of a meter
            notes, chords, rests, dyns, articulations = get_measure_notes(xml_file, score, i) 
            
            # append dynamics
            if dyns:  
                for dyn in dyns:
                    meter.hasDynamics.append(
                        instances[dyn])
                    
                # make last_dynamic the last dynamic in the music sheet  
                last_dynamic = dyns[-1]  
            elif last_dynamic:
                # append the last
                meter.hasDynamics.append(instances[last_dynamic])

            # append articulations
            if articulations:  
                for a in articulations: 
                    # every note has its own articulation, but we don't want to add it many times
                    if a not in meter.hasMusicalFeature:  
                        meter.hasArticulation.append(instances[a])

            # notes - intervals
            if notes:  
                # if notes exist then we can also find these 3:
                direction, avg_pitch, pitch_range = find_melody_direction_pitch_and_pitch_range(notes, last_note)
                # append direction
                if direction > 1: 
                    meter.hasMelodyDirection.append(instances[meo.AscendingMelody])
                elif direction < -1:  
                    meter.hasMelodyDirection.append(instances[meo.DescendingMelody])
                else:
                    meter.hasMelodyDirection.append(instances[meo.UndulatingMelody])
                
                # avg_pitch is a value corresponding to the average midi value of every note in the meter
                if avg_pitch:  
                    if avg_pitch > 71:
                        meter.hasAveragePitch.append(instances[meo.HighPitch])
                    elif avg_pitch > 55:
                        meter.hasAveragePitch.append(instances[meo.MediumPitch])
                    else:
                        meter.hasAveragePitch.append(instances[meo.LowPitch])

                # an integer corresponding to the difference between the highest and the lowest note
                if pitch_range: 
                    if pitch_range > 11:
                        meter.hasPitchRange.append(instances[meo.WidePitchRange])
                    elif pitch_range < 8:
                        meter.hasPitchRange.append(instances[meo.NarrowPitchRange])

                # if last note (coming from the previous measure) exists 
                # then we append to this meter the interval of the last note with the first note of this measure
                if last_note:
                    interval = find_intervals(last_note, notes[0])
                    if interval != 'Invalid interval':
                            meter.hasMusicalFeature.append(instances[interval]) 
                
                # for every note find interval  and append it 
                for j in range(len(notes) - 1):
                    interval = find_intervals(notes[j], notes[j + 1])
                    if interval != 'Invalid interval':
                        instances[interval].hasDuration = interval.hasDuration
                        # append the interval to the meter
                        meter.hasMusicalFeature.append(instances[interval]) 
                # update the last note
                last_note = notes[-1]
            # if there are no notes in the measure then make last note None
            else:
                last_note = None 

        # run the reasoner:      
        sync_reasoner_pellet(infer_property_values=True, debug=1)

        print(track.hasTempo)
        # calculate and append the valence and arousal values to the dataProperties
        for j,meter in enumerate(meter_list):
            avg_ar[j], avg_val[j] = calculate_valence_arousal(meter)
            meter.hasValenceValue.append(avg_val[j])
            meter.hasArousalValue.append(avg_ar[j])
        
        
        for meter in meter_list:
            print(meter)
            for mf in meter.hasMusicalFeature:
                print(mf)
            print(meter.hasValenceValue, meter.hasArousalValue)

        # plot the valence and arousal values as the meters progress
        plot_valence_arousal(list(avg_val.values()), list(avg_ar.values()), len(meter_list), title)



