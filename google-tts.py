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
SPEECH_SPEED = 1.0       # 1.0 is normal, 1.5 is fast

# Ensure folders exist
os.makedirs(IMPORT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def speed_change(sound, speed=1.0):
    """Adjusts the playback speed of an AudioSegment without changing pitch."""
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def text_to_segment(text, identifier):
    """Converts text to an audio segment with speed adjustment."""
    # Using identifier to prevent permission errors with overlapping files
    temp_file = f"temp_{identifier}.mp3"
    
    tts = gTTS(text=str(text), lang='en')
    tts.save(temp_file)
    segment = AudioSegment.from_mp3(temp_file)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    if SPEECH_SPEED != 1.0:
        segment = speed_change(segment, SPEECH_SPEED)
        
    return segment

def process_single_csv(input_path):
    """Processes one CSV file and exports an MP3 named after it."""
    file_name_no_ext = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(OUTPUT_FOLDER, f"{file_name_no_ext}.mp3")
    
    print(f"\n--- Starting: {os.path.basename(input_path)} ---")

    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"Error reading {input_path}: {e}")
        return

    full_audio = AudioSegment.empty()
    mid_pause = AudioSegment.silent(duration=FRONT_BACK_PAUSE)
    end_pause = AudioSegment.silent(duration=NEXT_CARD_PAUSE)

    total_rows = len(df)
    for index, row in df.iterrows():
        print(f"  [{file_name_no_ext}] {index + 1}/{total_rows}: {str(row['Front'])[:20]}...")
        
        # Pass unique identifiers for temp files
        front_audio = text_to_segment(row['Front'], f"{index}_f")
        back_audio = text_to_segment(row['Back'], f"{index}_b")
        
        full_audio += front_audio + mid_pause + back_audio + end_pause

    print(f"Exporting final MP3 to: {output_path}")
    full_audio.export(output_path, format="mp3")

def main():
    """Scans for all CSVs and processes them one by one."""
    csv_files = glob.glob(os.path.join(IMPORT_FOLDER, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in '{IMPORT_FOLDER}'.")
        return

    print(f"Found {len(csv_files)} files to process.")

    for csv_file in csv_files:
        process_single_csv(csv_file)
    
    print("\nAll tasks complete!")

if __name__ == "__main__":
    main()