import os
import tempfile
from io import BytesIO
from gtts import gTTS
from playsound import playsound


def run_tts(text):

    tts = gTTS(text)
    

    mp3_fp = BytesIO()
    

    tts.write_to_fp(mp3_fp)

    mp3_bytes = mp3_fp.getvalue()


    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(mp3_bytes)
        audio_file = f.name

    playsound(audio_file)


    os.unlink(audio_file)

if __name__ == '__main__':
    run_tts(text='this is a test')