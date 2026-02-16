import os
import glob
import pandas as pd
from gtts import gTTS
from pydub import AudioSegment

# --- Configuration ---
IMPORT_FOLDER = 'import'
OUTPUT_FOLDER = 'output'
FRONT_BACK_PAUSE = 5000  # 5 seconds
NEXT_CARD_PAUSE = 1000   # 1 second
SPEECH_SPEED = 1.0       # <--- ADJUST THIS (1.0 is normal, 1.5 is fast)

# Ensure folders exist
os.makedirs(IMPORT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def speed_change(sound, speed=1.0):
    """Adjusts the playback speed of an AudioSegment without changing pitch."""
    # Manually override the frame rate to change speed
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    # Convert back to standard frame rate so it plays correctly
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def text_to_segment(text):
    """Converts text to an audio segment with speed adjustment."""
    temp_file = "temp_segment.mp3"
    tts = gTTS(text=str(text), lang='en')
    tts.save(temp_file)
    segment = AudioSegment.from_mp3(temp_file)
    os.remove(temp_file)
    
    # Apply speed adjustment if not 1.0
    if SPEECH_SPEED != 1.0:
        segment = speed_change(segment, SPEECH_SPEED)
        
    return segment

def process_latest_csv():
    csv_files = glob.glob(os.path.join(IMPORT_FOLDER, "*.csv"))
    
    if not csv_files:
        print(f"Error: No CSV files found in the '{IMPORT_FOLDER}' folder.")
        return

    input_path = csv_files[0]
    file_name_no_ext = os.path.splitext(os.path.basename(input_path))[0]
    
    print(f"Reading file: {os.path.basename(input_path)}")
    print(f"Current Speed Setting: {SPEECH_SPEED}x")

    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"Failed to read CSV: {e}")
        return

    full_audio = AudioSegment.empty()
    mid_pause = AudioSegment.silent(duration=FRONT_BACK_PAUSE)
    end_pause = AudioSegment.silent(duration=NEXT_CARD_PAUSE)

    print(f"Processing {len(df)} cards...")

    for index, row in df.iterrows():
        print(f"  [{index + 1}/{len(df)}] Processing: {str(row['Front'])[:30]}...")
        
        front_audio = text_to_segment(row['Front'])
        back_audio = text_to_segment(row['Back'])
        
        full_audio += front_audio + mid_pause + back_audio + end_pause

    output_filename = f"{file_name_no_ext}.mp3"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    
    print("Exporting final MP3... (this may take a moment)")
    full_audio.export(output_path, format="mp3")
    print(f"Success! File saved as: {output_path}")

if __name__ == "__main__":
    process_latest_csv()