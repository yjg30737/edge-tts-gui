import edge_tts
import pyaudio
from io import BytesIO
from pydub import AudioSegment

TEXT = 'Hello World! How are you guys doing? I hope great, cause I am having fun and honestly it has been a blast'
VOICE = "en-US-AndrewMultilingualNeural"
CHUNK_SIZE = 20

def main() -> None:
    communicator = edge_tts.Communicate(TEXT, VOICE)
    audio_chunks = []

    pyaudio_instance = pyaudio.PyAudio()
    audio_stream = pyaudio_instance.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    for chunk in communicator.stream_sync():
        if chunk["type"] == "audio" and chunk["data"]:
            audio_chunks.append(chunk["data"])
            if len(audio_chunks) >= CHUNK_SIZE:
                edge_tts_play_audio_chunk(audio_chunks, audio_stream)
                audio_chunks.clear()

    # Play the rest of the audio
    edge_tts_play_audio_chunk(audio_chunks, audio_stream)

    audio_stream.stop_stream()
    audio_stream.close()
    pyaudio_instance.terminate()

def edge_tts_play_audio_chunk(chunks: list[bytes], stream: pyaudio.Stream) -> None:
    stream.write(AudioSegment.from_mp3(BytesIO(b''.join(chunks))).raw_data)

if __name__ == "__main__":
    main()