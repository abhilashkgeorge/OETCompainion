# import pyaudio
# import wave


# FORMAT = pyaudio.paInt16  # Audio format
# CHANNELS = 1  # Number of audio channels
# RATE = 16000  # Sampling rate
# CHUNK = 1024  # Number of audio frames per buffer
# RECORD_SECONDS = 5  # Duration of recording in seconds
# RECORDING_FILENAME = 'recording.wav'  # Name of output file


# def record(seconds=RECORD_SECONDS, filename=RECORDING_FILENAME):

#     audio = pyaudio.PyAudio()


#     stream = audio.open(
#         format=FORMAT, channels=CHANNELS,
#         rate=RATE, input=True,
#         frames_per_buffer=CHUNK)
        

#     frames = []
#     for i in range(0, int(RATE / CHUNK * seconds)):
#         data = stream.read(CHUNK)
#         frames.append(data)

#     stream.stop_stream()
#     stream.close()
#     audio.terminate()

#     # Write frames to a WAV file
#     wave_file = wave.open(filename, 'wb')
#     wave_file.setnchannels(CHANNELS)
#     wave_file.setsampwidth(audio.get_sample_size(FORMAT))
#     wave_file.setframerate(RATE)
#     wave_file.writeframes(b''.join(frames))
#     wave_file.close()

# if __name__ == '__main__':
#     record()

import pyaudio
import wave
import argparse
import audioop


FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 16000  
CHUNK = 1024  
INITIAL_SILENCE_THRESHOLD = 1500 
SILENCE_THRESHOLD_ADJUSTMENT = 50  
SILENCE_THRESHOLD_MAX = 500  

def record(filename):

    audio = pyaudio.PyAudio()


    stream = audio.open(
        format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        frames_per_buffer=CHUNK)

    print("Listening...")


    frames = []
    speech_started = False
    silence_frames = 0
    current_silence_threshold = INITIAL_SILENCE_THRESHOLD

    while True:
        data = stream.read(CHUNK)
        frames.append(data)


        rms = audioop.rms(data, 2)  

        if rms > current_silence_threshold:
            silence_frames = 0

            if not speech_started:
                print("Recording started.")
                speech_started = True
        else:
            silence_frames += 1

        if silence_frames > int(RATE / CHUNK):
            if speech_started:
                print("Recording finished.")
                break
            elif current_silence_threshold > SILENCE_THRESHOLD_MAX:
                current_silence_threshold -= SILENCE_THRESHOLD_ADJUSTMENT


    stream.stop_stream()
    stream.close()
    audio.terminate()


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
