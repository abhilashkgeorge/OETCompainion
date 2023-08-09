import os
import tempfile
from io import BytesIO
from gtts import gTTS
from playsound import playsound


def run_tts(text):
    # Create a gTTS object with the specified text
    tts = gTTS(text)
    
    # Create a BytesIO object to hold the audio data
    mp3_fp = BytesIO()
    
    # Write the audio data to the BytesIO object
    tts.write_to_fp(mp3_fp)

    # Extract the byte string from the BytesIO object
    mp3_bytes = mp3_fp.getvalue()

    # Save the audio data to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(mp3_bytes)
        audio_file = f.name

    # Play the audio data using the playsound module
    playsound(audio_file)

    # Delete the temporary audio file
    os.unlink(audio_file)

if __name__ == '__main__':
    # Run the run_tts function with the specified text
    run_tts(text='this is a test')