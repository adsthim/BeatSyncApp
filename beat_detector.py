# beat_detector.py
import librosa
import numpy as np

AUDIO_FILE = "trimmed_audio.mp3"
BEATS_FILE = "beats.npy"  # file to save filtered beats

def detect_beats(audio_path, min_interval=1.0):
    """
    Detect major beats in a song, using onset strength and filtering.
    Only returns beats separated by at least min_interval seconds.
    """
    y, sr = librosa.load(audio_path, sr=None)  # load at native sample rate

    # Compute onset envelope
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Pick peaks above the 75th percentile of onset strength
    threshold = np.percentile(onset_env, 75)
    strong_frames = np.where(onset_env >= threshold)[0]
    beat_times = librosa.frames_to_time(strong_frames, sr=sr)

    # Filter out beats that are too close together
    filtered_beats = []
    last_beat = -min_interval
    for t in beat_times:
        if t - last_beat >= min_interval:
            filtered_beats.append(t)
            last_beat = t

    print(f"Detected {len(filtered_beats)} major beats")
    np.save(BEATS_FILE, np.array(filtered_beats))
    print(f"✅ Beats saved to {BEATS_FILE}")
    return filtered_beats

if __name__ == "__main__":
    detect_beats(AUDIO_FILE)
