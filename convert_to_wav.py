"""
Convert MIDI to WAV using synthesizer
"""
import numpy as np
from scipy.io import wavfile
from midiutil import MIDIFile

def generate_tone(frequency, duration, sample_rate=22050, volume=0.3):
    """Generate a more musical tone with harmonics and envelope."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create a richer sound with harmonics
    fundamental = np.sin(2 * np.pi * frequency * t)
    harmonic2 = 0.3 * np.sin(2 * np.pi * frequency * 2 * t)  # Octave
    harmonic3 = 0.2 * np.sin(2 * np.pi * frequency * 3 * t)  # Fifth
    
    wave = fundamental + harmonic2 + harmonic3
    
    # Apply ADSR envelope (Attack, Decay, Sustain, Release)
    attack = int(0.1 * len(t))
    release = int(0.2 * len(t))
    
    envelope = np.ones(len(t))
    # Attack
    envelope[:attack] = np.linspace(0, 1, attack)
    # Release
    envelope[-release:] = np.linspace(1, 0, release)
    
    wave = wave * envelope * volume
    return wave

def midi_note_to_frequency(note):
    """Convert MIDI note number to frequency."""
    return 440.0 * (2.0 ** ((note - 69) / 12.0))

def create_haunting_wav():
    """Create a dramatic, menacing theme."""
    sample_rate = 22050
    
    # Define a dramatic, powerful melody (note, start_time, duration)
    # Original composition with a dark, menacing vibe
    melody = [
        # Phrase 1 - Powerful opening
        (48, 0, 1.5),    # C3
        (48, 1.5, 1.5),  # C3
        (48, 3, 1.5),    # C3
        (51, 4.5, 0.5),  # Eb3
        (53, 5, 1),      # F3
        
        # Phrase 2 - Rising intensity
        (48, 6, 1.5),    # C3
        (48, 7.5, 1.5),  # C3
        (48, 9, 1.5),    # C3
        (55, 10.5, 0.5), # G3
        (56, 11, 1),     # Ab3
        
        # Phrase 3 - Climax
        (60, 12, 2),     # C4
        (58, 14, 1),     # Bb3
        (56, 15, 1),     # Ab3
        (55, 16, 2),     # G3
        
        # Phrase 4 - Dark resolution
        (53, 18, 1.5),   # F3
        (51, 19.5, 1.5), # Eb3
        (48, 21, 3),     # C3 (hold)
    ]
    
    # Powerful bass notes
    bass_notes = [
        (36, 0, 3),      # C2
        (36, 3, 3),      # C2
        (36, 6, 3),      # C2
        (36, 9, 3),      # C2
        (36, 12, 4),     # C2
        (39, 16, 2),     # Eb2
        (36, 18, 6),     # C2 (long)
    ]
    
    # Calculate total duration
    total_duration = 32  # seconds
    total_samples = int(sample_rate * total_duration)
    audio = np.zeros(total_samples)
    
    # Add melody notes
    for note, start, duration in melody:
        freq = midi_note_to_frequency(note)
        wave = generate_tone(freq, duration, sample_rate, volume=0.25)
        start_sample = int(start * sample_rate)
        end_sample = start_sample + len(wave)
        if end_sample <= total_samples:
            audio[start_sample:end_sample] += wave
    
    # Add bass notes
    for note, start, duration in bass_notes:
        freq = midi_note_to_frequency(note)
        wave = generate_tone(freq, duration, sample_rate, volume=0.15)
        start_sample = int(start * sample_rate)
        end_sample = start_sample + len(wave)
        if end_sample <= total_samples:
            audio[start_sample:end_sample] += wave
    
    # Normalize and convert to 16-bit
    audio = audio / np.max(np.abs(audio))
    audio = (audio * 32767).astype(np.int16)
    
    # Save as WAV
    wavfile.write('blacklist_theme.wav', sample_rate, audio)
    print("✅ Created blacklist_theme.wav")

if __name__ == "__main__":
    create_haunting_wav()
