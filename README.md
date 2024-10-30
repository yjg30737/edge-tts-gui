# edge-tts-gui
This shows how to use edge-tts on Python without showing mpv window asynchronously. Also, you can stop playing edge-tts in the middle.
MP3 and VTT(for subtitle) files are generated for mpv to play, and after mpv is terminated, both will be deleted.

## Requirements
* PySide6
* [edge-tts](https://github.com/rany2/edge-tts)
* psutil
* mpv (Install separately)

## How to Install
1. Install mpv
   * Windows - choco install mpv
   * Mac - brew install mpv
   * Linux - sudo apt-get install mpv
2. git clone ~
3. python -m venv venv or python3 -m venv venv
4. venv/Script/activate or . venv/bin/activate
5. pip install -r requirements.txt
6. python main.py

## Preview
https://youtu.be/Vp3F1Gx7g0g
