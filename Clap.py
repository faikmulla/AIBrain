import sounddevice as sd
import numpy as np

# The threshold for clap detection (tune this based on testing)
THRESHOLD = 0.3
SAMPLE_RATE = 44100

def detect_clap():
    """
    Detects a clap based on sound volume levels.
    Returns True if a clap is detected, otherwise False.
    """
    try:
        # Record audio for a short period
        audio = sd.rec(int(SAMPLE_RATE * 0.5), samplerate=SAMPLE_RATE, channels=1)
        sd.wait()  # Wait for the recording to finish

        # Compute the audio's loudness level
        loudness = np.max(np.abs(audio))

        if loudness > THRESHOLD:
            return True  # A loud sound (like a clap) is detected
        else:
            return False

    except Exception as e:
        print(f"Error in clap detection: {e}")
        return False
