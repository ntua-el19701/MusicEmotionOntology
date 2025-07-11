from owlready2 import *

onto = get_ontology("http://www.semanticweb.org/musicEmotionOntology#")


with onto:

    class Track(Thing):
        comment = "Class representing a musical track"


    class Meter(Track):
        comment = "Class representing a meter in a track"


    class MusicalFeature(Thing):
        comment = "Class representing a musical feature"


    class EmotionalEffect(Thing):
        comment = "Class that represents an emotional effect"


    class Arousal(EmotionalEffect):
        comment = "Class representing arousal effect"
        label = "Arousal"


    class Valence(EmotionalEffect):
        comment = "Class that represents valence effect"


    class LowArousal(Arousal):
        comment = "Subclass representing Low Arousal"


    class VeryLowArousal(Arousal):
        comment = "Subclass representing Very Low Arousal"


    class MediumArousal(Arousal):
        comment = "Subclass representing Medium Arousal"


    class HighArousal(Arousal):
        comment = "Subclass representing High Arousal"


    class VeryHighArousal(Arousal):
        comment = "Subclass representing Very High Arousal"


    # VALENCE
    class PositiveValence(Valence):
        comment = "Class representing emotions with positive Valence, e.g happiness"


    class MediumPositiveValence(PositiveValence):
        comment = "Subclass representing emotions with Medium positive Valence"


    class VeryPositiveValence(PositiveValence):
        comment = "Subclass representing Emotions with very positive valence"


    class NegativeValence(Valence):
        comment = "Class representing emotions with negative Valence"


    class LowNegativeValence(NegativeValence):
        comment = "Class representing emotions with Low negative valence ()"


    class VeryNegativeValence(NegativeValence):
        comment = "Class representing emotions with Very negative valence ()"


    # Object Properties
    class hasMusicalFeature(Track >> MusicalFeature):
        comment = "Class connecting a track to their musical features"


    class triggers(MusicalFeature >> EmotionalEffect):
        comment = "Class that defines the relationship between a musical feature and the emotions it triggers"

    
    class meterHasTrack(Meter >> Track):
        comment = "Class that defines the relationship between meter and Track"


    class trackHasMeter(Track >> Meter):
        inverse_property = meterHasTrack


    class hasNext(Meter >> Meter):
        comment = "Class that defines which meter is the next one of this meter"


    class isFollowedByMeter(ObjectProperty, TransitiveProperty):
        domain = [Meter]
        range = [Meter]
        pass

    class hasNextMeter(ObjectProperty, FunctionalProperty,
                       isFollowedByMeter):
        domain = [Meter]
        range = [Meter]
        pass

    class followsMeter(Meter >> Meter):
        comment = "Class that defines which meter is the previous of this meter"

    # Data Properties
    class trackHasAverageValence(DataProperty):
        comment = "Class that defines the overall valence of the track"
        domain = [Track]
        range = [float]


    class trackHasAverageArousal(DataProperty):
        comment = "Class that defines the overall arousal of the track"
        domain = [Track]
        range = [float]

    class meterHasPosition(DataProperty):
        domain = [Meter]
        range = [str]


    class hasValenceValue(DataProperty):
        comment = "Class that defines a decimal number representing the valence value of the meter"
        domain = [Meter]
        range = [float]
        pass


    class hasArousalValue(DataProperty):
        comment = "Class that defines a decimal number representing the arousal value of the meter"
        domain = [Meter]
        range = [float]
        pass


    # Meters with valence/ arousal values
    class VeryPositiveValenceMeter(Meter):
        comment = "Class representing meters with very positive valence"
        equivalent_to = [Meter & (hasValenceValue >= 3.9)]


    class LowPositiveValenceMeter(Meter):
        comment = "Class representing meters with low positive valence"
        equivalent_to = [Meter & (hasValenceValue >= 0.25) & (hasValenceValue < 3.9)]


    class LowNegativeValenceMeter(Meter):
        comment = "Class representing meters with low positive valence"
        equivalent_to = [Meter & (hasValenceValue >= -3.9) & (hasValenceValue < 0.24)]


    class VeryNegativeValenceMeter(Meter):
        comment = "Class representing meters with low positive valence"
        equivalent_to = [Meter & (hasValenceValue < -3.9)]


    class VeryHighArousalMeter(Meter):
        comment = "Class representing meters with very high arousal"
        equivalent_to = [Meter & (hasArousalValue >= 7)]


    class MediumHighArousalMeter(Meter):
        comment = "Class representing meters with medium to high arousal"
        equivalent_to = [Meter & (hasArousalValue >= 0.4) & (hasArousalValue < 7)]


    class MediumLowArousalMeter(Meter):
        comment = "Class representing meters with medium to low arousal"
        equivalent_to = [Meter & (hasArousalValue >= -4.5) & (hasArousalValue < 0.4)]


    class VeryLowArousalMeter(Meter):
        comment = "Class representing meters with very low arousal"
        equivalent_to = [Meter & (hasArousalValue < -4.5)]



    #MUSICAL FEATURES
    # TEMPO

    class Rhythm(MusicalFeature):
        comment = "Class representing rhythm in music."


    class Tempo(Rhythm):
        comment = "Class representing the tempo in music."

    # Object property for tempo
    class hasTempo(Track >> Tempo):
        comment = "Class the defined the tempo of a track"
        is_a = [hasMusicalFeature]


    class hasBPM(DataProperty):
        domain = [Tempo]
        range = [int]


    class SlowTempo(Tempo):
        comment = "Subclass representing slow tempos in music."


    class MediumTempo(Tempo):
        comment = "Subclass representing medium tempos in music."


    class FastTempo(Tempo):
        comment = "Subclass representing fast tempos in music."


    # Subclasses for SlowTempo
    class Grave(SlowTempo):
        comment = "Subclass representing Grave tempo (20-40)."
        triggers = [VeryLowArousal]


    class LargoTempo(SlowTempo):
        comment = "Subclass representing Largo tempo (40-66)."
        triggers = [VeryLowArousal]


    class Adagio(SlowTempo):
        comment = "Subclass representing Adagio tempo (44-68)."
        triggers = [LowArousal]


    class Andante(SlowTempo):
        comment = "Subclass representing Andante tempo (56-108)."
        triggers = [LowArousal]


    # Subclasses for MediumTempo
    class Moderato(MediumTempo):
        comment = "Subclass representing Moderato tempo (108-120)."
        triggers = [LowArousal]


    class Allegretto(MediumTempo):
        comment = "Subclass representing Allegretto tempo (112-120)."
        triggers = [MediumArousal]


    class AllegroModerato(MediumTempo):
        comment = "Subclass representing Allegro Moderato tempo (116-120)."
        triggers = [MediumArousal]


    # Subclasses for FastTempo
    class AllegroTempo(FastTempo):
        comment = "Subclass representing Allegro tempo (120-156)."
        triggers = [HighArousal]


    class Vivace(FastTempo):
        comment = "Subclass representing Vivace tempo (156-176)."
        triggers = [HighArousal]


    class PrestoTempo(FastTempo):
        comment = "Subclass representing Presto tempo (168-200)."
        triggers = [VeryHighArousal]


    class Prestissimo(FastTempo):
        comment = "Subclass representing Prestissimo tempo (>200)."
        triggers = [VeryHighArousal]


    # Class for RhythmChange
    class RhythmChange(Rhythm):
        comment = "Class representing Rhythmic Changes."

     # object property for RhythmChange
    class hasRhythmChange(Track >> RhythmChange):
        comment = "Class that represents the rhythm change of a Track/meter"
        is_a = [hasMusicalFeature]

    class Accelerando(RhythmChange):
        comment = "Subclass representing Accelerando, which means gradually increase tempo"
       
        triggers = [VeryHighArousal, MediumPositiveValence]


    class Ritenuto(RhythmChange):
        comment = "Subclass representing Ritenuto, which means immediately and temporarily slow down the tempo"
        triggers = [VeryLowArousal, NegativeValence]


    class Ritardando(RhythmChange):
        comment = "Subclass representing Ritardando, which means gradually decrease tempo"
        triggers = [LowArousal, NegativeValence]


    # MELODY
    class Melody(MusicalFeature):
        comment = "Class representing Melody"


    # NOTES
    class Notes(Melody):
        comment = "Class representing the notes in a melody"

    # object property for notes
    class hasNotes(Track >> Notes):
        comment = "Class representing the notes of a track/meter"
        is_a = [hasMusicalFeature]

    # MELODY RANGE
    class MelodyRange(Melody):
        comment = "Class representing Melody Range"

    # object property for melody range
    class hasMelodyRange(Track >> MelodyRange):
        comment = "Class tha represents the melody range of a Track/meter"
        is_a = [hasMusicalFeature]

    class WideMelodyRange(MelodyRange):
        comment = "Subclass representing Wide Melody Range"
        triggers = [HighArousal]


    class NarrowMelodyRange(MelodyRange):
        comment = "Subclass representing Narrow Melody Range"
        triggers = [LowArousal]


    # MELODY DIRECTION
    class MelodyDirection(Melody):
        comment = "Class representing Melody Direction"

    # object property for melody direction
    class hasMelodyDirection(Track >> MelodyDirection):
        comment = "Class tha represents the melody direction of a Track/meter"
        is_a = [hasMusicalFeature]
    
    class AscendingMelody(MelodyDirection):
        comment = "Subclass representing Ascending Melody"
        triggers = [VeryHighArousal]


    class DescendingMelody(MelodyDirection):
        comment = "Subclass representing Descending Melody"
        triggers = [LowArousal]


    class UndulatingMelody(MelodyDirection):
        comment = "Subclass representing Undulating Melody"


    # INTERVALS
    class Intervals(Melody):
        comment = "Class representing the intervals in a Melody"


    class IntervalCount(Intervals):
        comment = "Class representing the number of times an interval is found in a meter"


    class hasIntervalCount(DataProperty):
        comment = "Class to count intervals"
        domain = [IntervalCount]
        range = [int]

    class hasInterval(ObjectProperty):
        comment = "Class to link the interval count to the specific interval"
        domain = [IntervalCount]
        range = [Intervals]
        is_a = [hasMusicalFeature]

    class hasIntervalsRatio(Intervals >> str, FunctionalProperty):
        comment = "Data Property for the ratio of intervals"


    class hasDuration(Intervals >> str, DataProperty):
        comment = "An integer represeting the duration of the interval - the note with the biggest duration"


    class ConsonantIntervals(Intervals):
        comment = "Class representing Consonant Intervals"


    class UnisonInterval(ConsonantIntervals):
        comment = "Subclass representing the Unison Interval"
        hasIntervalsRatio = ["1:1"]
        triggers = [LowArousal, PositiveValence]


    class OctaveInterval(ConsonantIntervals):
        comment = "Subclass representing the Octave Interval"
        hasIntervalsRatio = ["2:1"]
        triggers = [PositiveValence]


    class PerfectFifthInterval(ConsonantIntervals):
        comment = "Subclass representing the Perfect 5th Interval"
        hasIntervalsRatio = ["3:2"]
        triggers = [VeryPositiveValence]


    class PerfectFourthInterval(ConsonantIntervals):
        comment = "Subclass representing the Perfect 4th Interval"
        hasIntervalsRatio = ["4:3"]
        triggers = [MediumPositiveValence]


    class IntermediateIntervals(Intervals):
        comment = "Class representing Intermediate (Less consonant) Intervals"


    class MajorThirdInterval(IntermediateIntervals):
        comment = "Subclass representing the Major 3rd Interval"
        hasIntervalsRatio = ["5:4"]
        triggers = [MediumPositiveValence, MediumArousal]


    class MajorSixthInterval(IntermediateIntervals):
        comment = "Subclass representing the Major 6th Interval"
        hasIntervalsRatio = ["5:3"]
        triggers = [MediumPositiveValence, HighArousal]  # as a passing note emotionally neutral


    class MinorThirdInterval(IntermediateIntervals):
        comment = "Subclass representing the Minor 3rd Interval"
        hasIntervalsRatio = ["6:5"]
        triggers = [LowNegativeValence, MediumArousal]


    class MinorSixthInterval(IntermediateIntervals):
        comment = "Subclass representing the Minor 6th Interval"
        hasIntervalsRatio = ["8:5"]
        triggers = [LowNegativeValence, HighArousal]


    class DissonantIntervals(Intervals):
        comment = "Class representing Dissonant Intervals"

    class AugmentedFourthInterval(IntermediateIntervals):
        comment = "Subclass representing the Augmented Fourth Interval"
        hasIntervalsRatio = [""]
        triggers = [MediumArousal, LowNegativeValence]

    class MinorSeventhInterval(DissonantIntervals):
        comment = "Subclass representing the Minor 7th Interval"
        hasIntervalsRatio = ["7:4"]
        triggers = [VeryNegativeValence, HighArousal]  # if in major context neutral


    class MajorSecondInterval(DissonantIntervals):
        comment = "Subclass representing the Major 2nd Interval"
        hasIntervalsRatio = ["9:8"]
        triggers = [VeryNegativeValence]  # if whole note, not a passing note: if it is in majorMode: neutral


    class MajorSeventhInterval(DissonantIntervals):
        comment = "Subclass representing the Major 7th Interval"
        hasIntervalsRatio = ["15:8"]
        triggers = [VeryNegativeValence, MediumArousal]  # as a passing note emotionally neutral


    class MinorSecondInterval(DissonantIntervals):
        comment = "Subclass representing the Minor 2nd Interval"
        hasIntervalsRatio = ["16:15"]
        triggers = [VeryNegativeValence, HighArousal]


    class MelodyRepetition(Melody):
        comment = "Class representing repetition in a melody"


    class MelodyMotion(Melody):
        comment = "Class representing Melody motion"


    class ConjunctMelody(MelodyMotion):
        comment = "Subclass representing conjunct melody motion"
        triggers = [VeryLowArousal, LowArousal, MediumPositiveValence]


    class DisjunctMelody(MelodyMotion):
        comment = "Subclass representing disjunct melody motion"
        triggers = [HighArousal, VeryHighArousal]


    class Phrasing(Melody):
        comment = "Class representing phrasing in music"


    class PhrasingLength(Phrasing):
        comment = "Class representing phrasing length"


    class ShortPhrasingLength(PhrasingLength):
        comment = "Subclass representing short phrasing length"


    class LongPhrasingLength(PhrasingLength):
        comment = "Subclass representing long phrasing length"


    class MelodyConsistency(Phrasing):
        comment = "Class representing Melody Consistency"


    class ConsistentMelody(MelodyConsistency):
        comment = "Subclass representing Consistent Melody Phrasing"


    class InconsistentMelody(MelodyConsistency):
        comment = "Subclass representing Inconsistent Melody Phrasing"


    class MelodyCadence(Phrasing):
        comment = "Class representing Melody Cadence"

    # object property for melody cadence
    class hasMelodyCadence(Track >> MelodyCadence):
        comment = "Class tha represents the melody cadence of a Track/meter"
        is_a = [hasMusicalFeature]

    class PerfectCadence(MelodyCadence):
        comment = "Subclass representing Perfect Cadence"
        triggers = [VeryPositiveValence]


    class ImperfectCadence(MelodyCadence):
        comment = "Subclass representing Imperfect Cadence"
        triggers = [MediumPositiveValence, MediumArousal, HighArousal]


    class PlagalCadence(MelodyCadence):
        comment = "Subclass representing Plagal Cadence"
        triggers = [PositiveValence, MediumArousal]


    class InterruptedCadence(MelodyCadence):
        comment = "Subclass representing Interrupted Cadence"
        triggers = [LowNegativeValence, MediumArousal]


    # ARTICULATION
    class Articulation(Phrasing):
        comment = "Class representing Articulation"

    # object property for artilucations
    class hasArticulation(Track >> Articulation):
        comment = "Class tha represents the articulation of a Track/meter"
        is_a = [hasMusicalFeature]

    class Legato(Articulation):
        comment = "Subclass representing Legato: Notes are played smoothly"
        triggers = [VeryLowArousal, LowArousal, MediumPositiveValence]


    class Staccato(Articulation):
        comment = "Subclass representing Staccato: Notes are short and detached – tense"
        triggers = [HighArousal]


    class Tenuto(Articulation):
        comment = "Subclass representing Tenuto: Emphasizes on the length of the note, played with a sense of weight, stress"
        triggers = [MediumArousal]


    class Accent(Articulation):
        comment = "Subclass representing Accent: Play with additional force, intensity"
        triggers = [HighArousal]


    # Dynamic Shape
    class DynamicShape(Phrasing):
        comment = "Class representing Dynamic Shape: How the volume of the melody moves"

    # object Property for Dynamic Shape
    class hasDynamicShape(Track >> DynamicShape):
        comment = "Class representing the dynamic shape of a track/meter"
        is_a = [hasMusicalFeature]

    class Crescendo(DynamicShape):
        comment = "Subclass representing Crescendo: Volume gradually increases, building intensity"
        triggers = [HighArousal]


    class Diminuendo(DynamicShape):
        comment = "Subclass representing Diminuendo: Volume gradually decreases, a sense of release"
        triggers = [LowArousal]


    # Dynamics
    class Dynamics(Phrasing):
        comment = "Class representing Dynamics"

    # object property for dynamics
    class hasDynamics(Track >> Dynamics):
        comment = "Class representing the dynamics of a track/meter"
        is_a = [hasMusicalFeature]

    class SoftDynamics(Dynamics):
        comment = "Subclass representing soft dynamics"


    class ModerateDynamics(Dynamics):
        comment = "Subclass representing moderate dynamics"


    class LoudDynamics(Dynamics):
        comment = "Subclass representing loud dynamics"


    class Pianissimo(SoftDynamics):
        comment = "Subclass representing Pianissimo: Very softly"
        triggers = [VeryLowArousal, LowArousal, LowNegativeValence, MediumPositiveValence]


    class Piano(SoftDynamics):
        comment = "Subclass representing Piano: Softly"
        triggers = [LowArousal, MediumPositiveValence]


    class MezzoPiano(ModerateDynamics):
        comment = "Subclass representing Mezzo Piano: Moderately soft"
        triggers = [MediumArousal, HighArousal]


    class MezzoForte(ModerateDynamics):
        comment = "Subclass representing Mezzo Forte: Moderately loud"
        triggers = [MediumArousal]


    class Forte(LoudDynamics):
        comment = "Subclass representing Forte: Loud"
        triggers = [HighArousal]


    class Fortissimo(LoudDynamics):
        comment = "Subclass representing Fortissimo: Very loud"
        triggers = [VeryHighArousal]


    # Direct Instructions
    class DirectInstructions(Phrasing):
        comment = "Class representing Direct Instructions"

    # object property for direct instructions
    class hasDirectInstructions(Track >> DirectInstructions):
        comment = "Class representing the direct instruction of a track"
        is_a = [hasMusicalFeature]

    # Subclasses for specific direct instructions
    class Scherzando(DirectInstructions):
        comment = "Subclass representing Scherzando: Playful, with a sense of humor"
        triggers = [PositiveValence, MediumArousal]


    class Sforzando(DirectInstructions):
        comment = "Class representing Sforzando: play with sudden, strong emphasis"
        triggers = [VeryHighArousal, NegativeValence]


    class Vivo(DirectInstructions):
        comment = "Subclass representing Vivo: Lively"
        triggers = [PositiveValence, HighArousal]


    class Largo(DirectInstructions):
        triggers = [LowArousal, VeryLowArousal, LowNegativeValence, MediumPositiveValence]


    class AllegroInstruction(DirectInstructions):
        comment = "Subclass representing Allegro: Fast"
        triggers = [HighArousal]


    class PrestoInstruction(DirectInstructions):
        comment = "Subclass representing Presto: Very Fast"
        triggers = [HighArousal]


    class Tone(MusicalFeature):
        comment = "Class representing Tone"

    # Subclasses for specific tone characteristics
    class Pitch(Tone):
        comment = "Subclass representing Pitch: How high or low a tone is"
    
    # object property for pitch
    class hasAveragePitch(Track >> Pitch):
        comment = "Class tha represents the overall pitch of a Track/meter"
        is_a = [hasMusicalFeature]

    class HighPitch(Pitch):
        comment = "Subclass representing High Pitch: Associated with happiness, anger, fear"
        triggers = [HighArousal, MediumPositiveValence]


    class MediumPitch(Pitch):
        comment = "Class representing Medium Pitch: Octaves: 4- 4.5"
        triggers = [MediumArousal]


    class LowPitch(Pitch):
        comment = "Subclass representing Low Pitch: Associated with sadness, tenderness, fear"
        triggers = [LowArousal, LowNegativeValence]


    class PitchRange(Tone):
        comment = "Subclass representing Pitch Range: Narrow, Wide"

     # object property for pitch
    class hasPitchRange(Track >> PitchRange):
        comment = "Class tha represents the overall pitch Range of a Track/meter"
        is_a = [hasMusicalFeature]

    class NarrowPitchRange(PitchRange):
        comment = "Subclass representing Narrow Pitch Range"
        triggers = [LowArousal]


    class WidePitchRange(PitchRange):
        comment = "Subclass representing Wide Pitch Range"
        triggers = [VeryHighArousal]


    class Timbre(Tone):
        comment = "Subclass representing Timbre: Color/quality of the tone"

     # object property for pitch
    class hasTimbre(Track >> Timbre):
        comment = "Class tha represents the overall timbre of a Track/meter"
        is_a = [hasMusicalFeature]

    class BrightTimbre(Timbre):
        comment = "Subclass representing Bright Timbre: How bright and vibrant the timbre is"
        triggers = [PositiveValence]


    class MellowTimbre(Timbre):
        comment = "Subclass representing Mellow Timbre: Warm and smooth"
        triggers = [MediumArousal, LowArousal, NegativeValence]


    class HarshTimbre(Timbre):
        comment = "Subclass representing Harsh Timbre: How rough the timbre is"
        triggers = [HighArousal]


    class Mode(MusicalFeature):
        comment = "Class representing Mode"

    # Object property for Mode
    class hasMode(Track >> Mode):
        comment = "Class that defines the mode of a track"
        is_a = [hasMusicalFeature]

    class MajorMode(Mode):
        comment = "Subclass representing Major Mode"
        triggers = [VeryPositiveValence]


    class MinorMode(Mode):
        comment = "Subclass representing Minor Mode"
        triggers = [VeryNegativeValence]


    # HARMONY
    class Harmony(MusicalFeature):
        comment = "Class representing Harmony"


    # CHORD TYPES
    class ChordType(Harmony):
        comment = "Class representing Chord Types"


    class MajorChord(ChordType):
        comment = "Subclass representing Major Chord: Happiness, Cheerfulness, satisfaction"
        triggers = [PositiveValence, HighArousal, MediumArousal]


    class MinorChord(ChordType):
        comment = "Subclass representing Minor Chord: Sadness, darkness, depression"
        triggers = [NegativeValence, MediumArousal, LowArousal]


    class MajorSeventhChord(ChordType):
        comment = "Subclass representing Major Seventh Chord: Romance, softness, jazziness"
        triggers = [PositiveValence, MediumArousal]


    class MinorSeventhChord(ChordType):
        comment = "Subclass representing Minor Seventh Chord: Mellowness, moodiness, jazziness"
        triggers = [LowNegativeValence, MediumArousal]


    class NinthChord(ChordType):
        comment = "Subclass representing Ninth Chord: Optimism, Openness"
        triggers = [MediumPositiveValence, MediumArousal, HighArousal]


    class DiminishedChord(ChordType):
        comment = "Subclass representing Diminished Chord: Fear, shock, suspense"
        triggers = [HighArousal]


    class SuspendedFourthChord(ChordType):
        comment = "Subclass representing Suspended Fourth Chord: Delightful Tension"
        triggers = [PositiveValence, MediumArousal, HighArousal]


    class SeventhMinorNinthChord(ChordType):
        comment = "Subclass representing Seventh Minor Ninth Chord: Creepiness, fear"
        triggers = [HighArousal, NegativeValence]


    class AddedNinthChord(ChordType):
        comment = "Subclass representing Added Ninth Chord: Steeliness, austerity"
        triggers = [LowNegativeValence]


    # Chord Change Rate
    class ChordChangeRate(Harmony):
        comment = "Class representing Chord Change Rate: How fast chords are changed"


    class SlowChordChangeRate(ChordChangeRate):
        comment = "Subclass representing Chord Change Rate Feeling of stability, relaxation. (Chords change slowly)"
        triggers = [LowArousal, VeryLowArousal]


    class MediumChordChangeRate(ChordChangeRate):
        comment = "Subclass representing Chord Change Rate: Chords change at a regular pace (e.g., 1 per meter)"
        triggers = [MediumArousal]


    class FastChordChangeRate(ChordChangeRate):
        comment = "Subclass representing Chord Change Rate: Feeling of energy, movement, liveliness. (Fast, maybe 1 per beat)"
        triggers = [HighArousal, VeryHighArousal]


    # TONAL MODULATION
    class TonalModulation(Harmony):
        comment = "Subclass representing Tonal Modulation: Change in tonal center or key"


    # Modulation Expectancy hereeee
    class ModulationExpectancy(TonalModulation):
        comment = "Class representing Modulation Expectancy. The number next to each modulation means movement in the circle of fifths"


    class ExpectedTonalModulation(ModulationExpectancy):
        comment = "Class representing Expected Tonal Modulations"


    class UnexpectedTonalModulation(ModulationExpectancy):
        comment = "Class representing Unexpected Tonal Modulations"
        triggers = [HighArousal]


    class AmbiguousTonalModulation(ModulationExpectancy):
        comment = "Class representing Ambiguous Tonal Modulations"


    class ExpectedMajorToMajor(ExpectedTonalModulation):
        comment = "Subclass representing Expected Major to Major Tonal Modulations"
        triggers = [VeryPositiveValence]


    class ExpectedMajorToMinor(ExpectedTonalModulation):
        comment = "Subclass representing Expected Major to Minor Tonal Modulations"
        triggers = [MediumPositiveValence]


    class ExpectedMinorToMajor(ExpectedTonalModulation):
        comment = "Subclass representing Expected Minor to Major Tonal Modulations"
        triggers = [MediumPositiveValence]


    class ExpectedMinorToMinor(ExpectedTonalModulation):
        comment = "Subclass representing Expected Minor to Minor Tonal Modulations"
        triggers = [LowNegativeValence]


    class UnexpectedMajorToMajor(UnexpectedTonalModulation):
        comment = "Subclass representing Unexpected Major to Major Tonal Modulations"
        triggers = [MediumPositiveValence]


    class UnexpectedMajorToMinor(UnexpectedTonalModulation):
        comment = "Subclass representing Unexpected Major to Minor Tonal Modulations"
        triggers = [LowNegativeValence]


    class UnexpectedMinorToMajor(UnexpectedTonalModulation):
        comment = "Subclass representing Unexpected Minor to Major Tonal Modulations"
        triggers = [MediumPositiveValence]


    class UnexpectedMinorToMinor(UnexpectedTonalModulation):
        comment = "Subclass representing Unexpected Minor to Minor Tonal Modulations"
        triggers = [VeryNegativeValence]


    class AmbiguousMajorToMajor(AmbiguousTonalModulation):
        comment = "Subclass representing Ambiguous Major to Major Tonal Modulations"
        triggers = [MediumPositiveValence]


    class AmbiguousMajorToMinor(AmbiguousTonalModulation):
        comment = "Subclass representing Ambiguous Major to Minor Tonal Modulations"
        triggers = [LowNegativeValence]


    class AmbiguousMinorToMajor(AmbiguousTonalModulation):
        comment = "Subclass representing Ambiguous Minor to Major Tonal Modulations"
        triggers = [MediumPositiveValence]


    class AmbiguousMinorToMinor(AmbiguousTonalModulation):
        comment = "Subclass representing Ambiguous Minor to Minor Tonal Modulations"
        triggers = [LowNegativeValence]


    #onto.save(file="MusicEmotionsOntology.owl", format="rdfxml")
    
    def create_instances():
        """
        function that creates a dicitonary of class -> instance_of_the_class
        """
        instances_by_class = {}  # a dictionary like: { MajorMode -> majormode_instance , ... }
        for cls in onto.classes():
            if cls.namespace != owl.Thing.namespace:  # Exclude owl.Thing and its subclasses
                # Generate instance names dynamically (e.g., using class name + "_instance")
                instance_name = f"{cls.name.lower()}_instance"
                # Create an instance of the current class within the ontology context
                instance = cls(instance_name)
                if issubclass(cls, onto.MusicalFeature) and hasattr(cls, 'triggers'):
                    instance.triggers = cls.triggers  # add the triggers
                instances_by_class[cls] = instance 
    
        return instances_by_class
    
    onto.save("MusicEmotionsOntology.owl", 'rdfxml')
    create_instances()



