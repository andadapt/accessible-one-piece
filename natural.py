import os
import glob
import asyncio
import pandas as pd
from edge_tts import Communicate
from pydub import AudioSegment

# --- Configuration ---
IMPORT_FOLDER = 'import'
OUTPUT_FOLDER = 'output'
FRONT_BACK_PAUSE = 5000  # 5 seconds
NEXT_CARD_PAUSE = 1000   # 1 second
VOICE = "en-GB-RyanNeural"  # Options: en-US-GuyNeural, en-US-JennyNeural, en-GB-SoniaNeural
SPEED = "+10%"              # Use +10%, -20%, etc. (Much more natural than the pitch-shift way!)

# Ensure folders exist
os.makedirs(IMPORT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

async def text_to_segment(text):
    """Converts text to an audio segment using Microsoft's Natural Voices."""
    temp_file = "temp_segment.mp3"
    communicate = Communicate(str(text), VOICE, rate=SPEED)
    await communicate.save(temp_file)
    segment = AudioSegment.from_mp3(temp_file)
    os.remove(temp_file)
    return segment

async def process_latest_csv():
    csv_files = glob.glob(os.path.join(IMPORT_FOLDER, "*.csv"))
    
    if not csv_files:
        print(f"Error: No CSV files found in '{IMPORT_FOLDER}'")
        return

    input_path = csv_files[0]
    file_name_no_ext = os.path.splitext(os.path.basename(input_path))[0]
    
    print(f"Reading: {os.path.basename(input_path)}")
    print(f"Using Voice: {VOICE} at {SPEED} speed")

    df = pd.read_csv(input_path, encoding='utf-8-sig')
    full_audio = AudioSegment.empty()
    mid_pause = AudioSegment.silent(duration=FRONT_BACK_PAUSE)
    end_pause = AudioSegment.silent(duration=NEXT_CARD_PAUSE)

    print(f"Processing {len(df)} cards...")

    for index, row in df.iterrows():
        print(f"  [{index + 1}/{len(df)}] Speaking: {str(row['Front'])[:30]}...")
        
        # We 'await' the audio generation here
        front_audio = await text_to_segment(row['Front'])
        back_audio = await text_to_segment(row['Back'])
        
        full_audio += front_audio + mid_pause + back_audio + end_pause

    output_path = os.path.join(OUTPUT_FOLDER, f"{file_name_no_ext}.mp3")
    print("Exporting final MP3...")
    full_audio.export(output_path, format="mp3")
    print(f"Finished! Saved to: {output_path}")

if __name__ == "__main__":
    asyncio.run(process_latest_csv())