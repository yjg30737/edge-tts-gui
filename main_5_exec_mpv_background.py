import os
import subprocess
import tempfile
import sys

async def speech(text, voice):
    media = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    media.close()
    mp3_fname = media.name

    subtitle = tempfile.NamedTemporaryFile(suffix=".vtt", delete=False)
    subtitle.close()
    vtt_fname = subtitle.name

    print(f"Media file: {mp3_fname}")
    print(f"Subtitle file: {vtt_fname}\n")
    with subprocess.Popen(
            [
                "edge-tts",
                f"--write-media={mp3_fname}",
                f"--write-subtitles={vtt_fname}",
                f"--voice={voice}",
                f"--text={text}",
            ]
    ) as process:
        process.communicate()

    with subprocess.Popen(
            [
                "mpv",
                f"--sub-file={vtt_fname}",
                mp3_fname,
            ],
            shell=True
    ) as process:
        process.communicate()
    if mp3_fname is not None and os.path.exists(mp3_fname):
        os.unlink(mp3_fname)
    if vtt_fname is not None and os.path.exists(vtt_fname):
        os.unlink(vtt_fname)