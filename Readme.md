# Cursor Controlled with Eyes

Eye tracking application that lets you control your mouse cursor with your eyes and click by blinking.

## Features

- **Eye Tracking**: Uses MediaPipe face mesh to detect eye position in real-time
- **Mouse Control**: Cursor follows your gaze with adjustable sensitivity
- **Blink Detection**: Click by blinking (with cooldown to prevent accidental clicks)
- **Real-time Visualization**: See eye landmarks on the video feed
- **Failsafe**: Move cursor to screen corner to emergency stop


## Installation

```bash
python -m venv .venv
source .venv/Scripts/activate  
pip install -r requirements.txt