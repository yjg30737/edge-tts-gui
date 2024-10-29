import os
import subprocess
import sys
import tempfile

# Get the input text from command-line arguments
text = sys.argv[1] if len(sys.argv) > 1 else "Hello, world!"

output_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
output_file_name = output_file.name

print(f"Media file: {output_file_name}")

try:
    # Generate TTS audio using edge-tts
    with subprocess.Popen(
        ["edge-tts", "--voice", "en-US-JennyNeural", "--text", text, "--write-media", output_file_name]
    ) as process:
        process.communicate()

    # Play the generated audio using mpv in a non-blocking way and wait for it to complete
    mpv_process = subprocess.Popen( ["mpv", "--no-terminal", "--force-window=no", output_file_name])

    mpv_process.wait()  # mpv가 완료될 때까지 기다림

finally:
    # After playback, delete the file
    if output_file_name is not None and os.path.exists(output_file_name):
        try:
            os.unlink(output_file_name)
            print("Temporary file deleted successfully.")
        except PermissionError as e:
            print(f"Failed to delete file: {e}")
