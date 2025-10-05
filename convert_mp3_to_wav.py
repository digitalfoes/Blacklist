"""
Convert MP3 to WAV for use in the blacklist application
"""
from pydub import AudioSegment
import os

def convert_mp3_to_wav():
    """Convert blacklistsong.mp3 to blacklist_theme.wav"""
    
    input_file = "blacklistsong.mp3"
    output_file = "blacklist_theme.wav"
    
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        return False
    
    try:
        print(f"🔄 Converting {input_file} to {output_file}...")
        
        # Load MP3 file
        audio = AudioSegment.from_mp3(input_file)
        
        # Convert to WAV with settings compatible with pygame
        audio = audio.set_frame_rate(22050)  # Standard sample rate
        audio = audio.set_channels(2)        # Stereo
        audio = audio.set_sample_width(2)    # 16-bit
        
        # Export as WAV
        audio.export(output_file, format="wav")
        
        print(f"✅ Successfully converted to {output_file}")
        print(f"   Duration: {len(audio) / 1000:.1f} seconds")
        print(f"   Sample Rate: 22050 Hz")
        print(f"   Channels: Stereo")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False

if __name__ == "__main__":
    convert_mp3_to_wav()
