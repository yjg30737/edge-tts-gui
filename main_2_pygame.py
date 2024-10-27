#!/usr/bin/env python3

"""
Basic audio streaming example.

This example shows how to stream the audio data from the TTS engine,
and how to get the WordBoundary events from the engine (which could
be ignored if not needed).

The example streaming_with_subtitles.py shows how to use the
WordBoundary events to create subtitles using SubMaker.
"""

import asyncio
from pygame import mixer  # Load the popular external library

import edge_tts
import time
import os, tempfile

TEXT = "Hello World!"
VOICE = "en-GB-SoniaNeural"
OUTPUT_FILE = "test.mp3"


async def speech(text, voice, output_file) -> None:
    keep = os.environ.get("EDGE_PLAYBACK_KEEP_TEMP") is not None
    mp3_fname = os.environ.get("EDGE_PLAYBACK_MP3_FILE")
    vtt_fname = os.environ.get("EDGE_PLAYBACK_VTT_FILE")
    media, subtitle = None, None
    try:
        if not mp3_fname:
            media = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            media.close()
            mp3_fname = media.name

        if not vtt_fname:
            subtitle = tempfile.NamedTemporaryFile(suffix=".vtt", delete=False)
            subtitle.close()
            vtt_fname = subtitle.name
        mixer.init()
        mixer.music.load(mp3_fname)
        mixer.music.play()
        while mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
    finally:
        if keep:
            print(f"\nKeeping temporary files: {mp3_fname} and {vtt_fname}")
        else:
            if mp3_fname is not None and os.path.exists(mp3_fname):
                os.unlink(mp3_fname)
            if vtt_fname is not None and os.path.exists(vtt_fname):
                os.unlink(vtt_fname)


if __name__ == "__main__":
    asyncio.run(speech(TEXT, VOICE, OUTPUT_FILE))