import pyaudio
import wave

# Set audio parameters
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of audio channels
RATE = 16000  # Sampling rate
CHUNK = 1024  # Number of audio frames per buffer
RECORD_SECONDS = 5  # Duration of recording in seconds
RECORDING_FILENAME = 'recording.wav'  # Name of output file


def record(seconds=RECORD_SECONDS, filename=RECORDING_FILENAME):
    # Initialize PyAudio object
    audio = pyaudio.PyAudio()

    # Open audio stream
    stream = audio.open(
        format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        frames_per_buffer=CHUNK)
        
    # Record audio
    frames = []
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop audio stream and PyAudio object
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Write frames to a WAV file
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

if __name__ == '__main__':
    # Run the record function with default parameters
    record()

'''import pyaudio
import wave
import argparse

# Set audio parameters
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Number of audio channels
RATE = 16000  # Sampling rate
CHUNK = 1024  # Number of audio frames per buffer
SILENCE_THRESHOLD = 0.01  # Adjust this value as needed (lower for more sensitivity)

def record(filename):
    """
    Record audio until the user stops speaking and save it to a WAV file.

    Parameters:
        filename (str): Name of the output WAV file.
    """
    # Initialize PyAudio object
    audio = pyaudio.PyAudio()

    # Open audio stream
    stream = audio.open(
        format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        frames_per_buffer=CHUNK)

    print("Listening...")

    # Variables for VAD
    frames = []
    speech_started = False
    silence_frames = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Calculate RMS energy of the audio frame
        rms = audioop.rms(data, 2)  # 2 is the width of each sample in bytes

        if rms > SILENCE_THRESHOLD:
            silence_frames = 0

            if not speech_started:
                print("Recording started.")
                speech_started = True
        else:
            silence_frames += 1

        # Adjust the silence duration threshold as needed
        if speech_started and silence_frames > int(RATE / CHUNK):
            print("Recording finished.")
            break

    # Stop audio stream and PyAudio object
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Write frames to a WAV file
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Record audio until the user stops speaking and save it to a WAV file.")
    parser.add_argument("--output", type=str, default="recording.wav", help="Name of the output WAV file.")
    args = parser.parse_args()

    record(filename=args.output)
'''