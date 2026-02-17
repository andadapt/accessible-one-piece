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
VOICE = "en-GB-RyanNeural"
SPEED = "+10%"

# Ensure folders exist
os.makedirs(IMPORT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

async def text_to_segment(text, identifier):
    """Converts text to an audio segment. Uses an identifier to prevent file collisions."""
    temp_file = f"temp_{identifier}.mp3"
    try:
        communicate = Communicate(str(text), VOICE, rate=SPEED)
        await communicate.save(temp_file)
        segment = AudioSegment.from_mp3(temp_file)
        return segment
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

async def process_single_csv(input_path):
    """Processes a single CSV file and exports its specific MP3."""
    file_name_no_ext = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(OUTPUT_FOLDER, f"{file_name_no_ext}.mp3")
    
    print(f"\n--- Processing: {os.path.basename(input_path)} ---")
    
    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"Failed to read {input_path}: {e}")
        return

    full_audio = AudioSegment.empty()
    mid_pause = AudioSegment.silent(duration=FRONT_BACK_PAUSE)
    end_pause = AudioSegment.silent(duration=NEXT_CARD_PAUSE)

    for index, row in df.iterrows():
        print(f"  [{file_name_no_ext}] Card {index + 1}/{len(df)}: {str(row['Front'])[:20]}...")
        
        # We pass the index to text_to_segment to keep temp files unique
        front_audio = await text_to_segment(row['Front'], f"{index}_f")
        back_audio = await text_to_segment(row['Back'], f"{index}_b")
        
        full_audio += front_audio + mid_pause + back_audio + end_pause

    print(f"Exporting: {output_path}")
    full_audio.export(output_path, format="mp3")

async def main():
    csv_files = glob.glob(os.path.join(IMPORT_FOLDER, "*.csv"))
    
    if not csv_files:
        print(f"Error: No CSV files found in '{IMPORT_FOLDER}'")
        return

    print(f"Found {len(csv_files)} files. Starting batch process...")

    for csv_file in csv_files:
        await process_single_csv(csv_file)
    
    print("\nAll files have been processed successfully!")

if __name__ == "__main__":
    asyncio.run(main())