"""
Create a haunting MIDI theme song for the Blacklist application
"""
from midiutil import MIDIFile

def create_haunting_theme():
    """Create a dark, haunting MIDI theme."""
    # Create MIDI file with 1 track
    midi = MIDIFile(1)
    
    track = 0
    channel = 0
    time = 0
    tempo = 60  # Slow, haunting tempo (60 BPM)
    volume = 100
    
    midi.addTempo(track, time, tempo)
    
    # Haunting melody in minor key (D minor)
    # Notes: D, E, F, G, A, Bb, C
    # Creating an eerie, descending pattern
    
    melody = [
        # Phrase 1 - Descending ominous pattern
        (62, 0, 2),   # D4
        (60, 2, 2),   # C4
        (58, 4, 2),   # Bb3
        (57, 6, 2),   # A3
        
        # Phrase 2 - Rising tension
        (57, 8, 1),   # A3
        (60, 9, 1),   # C4
        (62, 10, 1),  # D4
        (65, 11, 3),  # F4 (hold)
        
        # Phrase 3 - Dark resolution
        (62, 14, 2),  # D4
        (58, 16, 2),  # Bb3
        (55, 18, 2),  # G3
        (53, 20, 4),  # F3 (long hold)
        
        # Phrase 4 - Eerie echo
        (62, 24, 1),  # D4
        (60, 25, 1),  # C4
        (58, 26, 1),  # Bb3
        (57, 27, 5),  # A3 (fade out)
    ]
    
    # Add melody notes
    for pitch, start_time, duration in melody:
        midi.addNote(track, channel, pitch, start_time, duration, volume)
    
    # Add bass notes for depth (one octave lower)
    bass_notes = [
        (50, 0, 4),   # D3
        (48, 4, 4),   # C3
        (46, 8, 4),   # Bb2
        (45, 12, 4),  # A2
        (50, 16, 4),  # D3
        (48, 20, 4),  # C3
        (45, 24, 8),  # A2 (long)
    ]
    
    for pitch, start_time, duration in bass_notes:
        midi.addNote(track, channel, pitch, start_time, duration, volume - 20)
    
    # Write to file
    with open("blacklist_theme.mid", "wb") as output_file:
        midi.writeFile(output_file)
    
    print("✅ Created blacklist_theme.mid")

if __name__ == "__main__":
    create_haunting_theme()
