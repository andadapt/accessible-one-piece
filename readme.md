# 🎧 Flashcard Audio Generator Guide

## ✅ Prerequisites

1.  Install Python from https://www.python.org/\

2.  Install FFmpeg. The easiest way is via PowerShell (as Admin) using:

    ``` powershell
    choco install ffmpeg
    ```

    (Requires `<organization>`{=html}Chocolatey`</organization>`{=html})

3.  Install the required Python libraries:

    ``` bash
    pip install edge-tts pandas pydub
    ```

------------------------------------------------------------------------

## 📁 Folder Structure

Create the following structure:

    project-folder/
    │
    ├── import/      # Place your CSV files here
    ├── output/      # Generated MP3 files will be saved here
    └── your_script.py

-   Create a **main project folder**
-   Inside it, create:
    -   `import` → for CSV files\
    -   `output` → where MP3 files are saved\
-   Place your Python script (`.py` file) in the main project folder

------------------------------------------------------------------------

## 📄 CSV Specifications

-   **Format:** Must be a `.csv` file\
-   **Required Columns:**
    -   `Front`\
    -   `Back`\
-   **Naming:**
    -   The final MP3 file will be named exactly the same as the CSV
        file\
-   **Location:**
    -   Place the CSV file inside the `import` folder

------------------------------------------------------------------------

## ⚙️ How the Script Works

1.  Scans the `import` folder for the first CSV file it finds\
2.  Uses `<organization>`{=html}Microsoft`</organization>`{=html}'s
    Natural AI voices to read the **"Front"** text\
3.  Waits for the duration set in `FRONT_BACK_PAUSE` (default: 5
    seconds)\
4.  Reads the **"Back"** text\
5.  Waits for the duration set in `NEXT_CARD_PAUSE` (default: 1 second)\
6.  Exports the combined audio to the `output` folder as an MP3

------------------------------------------------------------------------

## 🔧 Adjustable Variables (Inside the Script)

### 🎙 VOICE

Change the voice string, for example:

    en-GB-RyanNeural
    en-US-JennyNeural

This changes the speaker voice.

### 🚀 SPEED

Change the percentage value to adjust speaking rate (without changing
pitch):

    +10%
    +20%

### ⏱ PAUSES

Adjust silence timing using milliseconds: - `1000 = 1 second` - Modify
pause values to control silence between: - Front and Back - Each
flashcard

------------------------------------------------------------------------

## ▶️ Running the Script

1.  Open Terminal or PowerShell inside your project folder\

2.  Run:

    ``` bash
    python your_script_name.py
    ```

3.  Wait until you see:

```{=html}
<!-- -->
```
    Finished!

------------------------------------------------------------------------

**You're all set! 🎉 Your flashcards will now be converted into
natural‑sounding MP3 audio files.**
