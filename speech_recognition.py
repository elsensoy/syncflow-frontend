import sounddevice as sd
import pyaudio
from google.cloud import speech
import numpy as np
import soundfile as sf
import time

def test_capture():
    try:
        with sd.InputStream(device=1, channels=2, samplerate=16000):
            print("Audio device is working")
    except Exception as e:
        print(f"Failed to capture audio: {e}")

test_capture()

def create_speech_client():
    """Configures and returns a Google Cloud Speech client and streaming configuration with speaker diarization."""
    client = speech.SpeechClient()

    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=2,
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        model='video',
        use_enhanced=True,
        diarization_config=diarization_config
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    return client, streaming_config

def audio_stream(device_index=None, channels=1, rate=16000, chunk=4096, duration=5):
    """Captures audio from the specified microphone using PyAudio and yields it in chunks for a specified duration."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk,
                    input_device_index=device_index)

    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            data = stream.read(chunk)
            yield data
        except Exception as e:
            print(f"Error capturing audio: {e}")
            break  # Exit loop on error

    stream.stop_stream()
    stream.close()
    p.terminate()
def recognize_speech(client, streaming_config, audio_generator):
    """Streams audio to Google Cloud Speech-to-Text API and processes the responses."""
    requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
    responses = client.streaming_recognize(config=streaming_config, requests=requests)

    for response in responses:
        for result in response.results:
            if result.is_final:
                print(f"Final result: {result.alternatives[0].transcript} (Speaker {result.alternatives[0].speaker_tag})")
            else:
                print(f"Interim result: {result.alternatives[0].transcript}")

def list_audio_devices():
    """Lists available audio devices."""
    print("Available audio devices:")
    print(sd.query_devices())

def main():
    client, streaming_config = create_speech_client()
    list_audio_devices()  # Optional: list devices for user reference

    # Specify device index and channels directly in audio_stream
    audio_generator = audio_stream(device_index=1)  # PyAudio automatically detects channels

    recognize_speech(client, streaming_config, audio_generator)  # Pass audio_generator

if __name__ == '__main__':
    main()