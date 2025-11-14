import numpy as np
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips

# --- USER SETTINGS ---
VIDEO_FILE = "your_clip.mp4"        # replace with your video filename
AUDIO_FILE = "trimmed_audio.mp3"    # replace with your song filename
BEATS_FILE = "beats.npy"            # saved from beat_detector.py
OUTPUT_FILE = "synced_edit.mp4"

# --- OFFSET SETTINGS ---
clip_duration = 0.7   # seconds per highlight clip
OFFSET = 0.05         # seconds to shift clip start for better sync

def create_synced_edit(video_path, audio_path, beats_path, output_path):
    print("Loading video...")
    clip = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Load beats
    beat_times = np.load(beats_path)

    # Remove beats that exceed video duration
    beat_times = beat_times[beat_times < clip.duration]
    print(f"{len(beat_times)} beats after trimming to video length")

    # Create short clips around each beat with OFFSET
    subclips = []
    for i, t in enumerate(beat_times):
        start = max(0, t - clip_duration / 2 - OFFSET)  # apply offset
        end = min(clip.duration, start + clip_duration)
        subclips.append(clip.subclipped(start, end))
        print(f"Processed beat {i+1}/{len(beat_times)} at {t:.2f}s (start={start:.2f}s)")

    # Concatenate subclips and attach audio
    final = concatenate_videoclips(subclips, method="compose")
    final = final.with_audio(audio.with_duration(final.duration))

    print("Exporting final video...")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print("✅ Video exported successfully!")

if __name__ == "__main__":
    create_synced_edit(VIDEO_FILE, AUDIO_FILE, BEATS_FILE, OUTPUT_FILE)
