# 🎧 Flashcard Audio Generator Guide

This project converts flashcard CSV files into natural‑sounding MP3
audio files.

It is used to aid in memorising One Piece trading cards. As a blind player this is incredibly helpful. It converts files I use for flash cards into audio fiels I can listen to as I go about other tasks.

You can now choose between two different text‑to‑speech engines:

-   **google-tts.py** → Uses Google's TTS engine\
-   **natural.py** → Uses Microsoft Windows natural AI voices

------------------------------------------------------------------------

## ✅ Prerequisites

### 1️⃣ Install Python

Download and install Python from:\
https://www.python.org/

Make sure you check **"Add Python to PATH"** during installation.

------------------------------------------------------------------------

### 2️⃣ Install FFmpeg

FFmpeg is required for exporting MP3 files.

The easiest method (Windows) is using PowerShell as Administrator:

``` powershell
choco install ffmpeg
```

(Requires Chocolatey: https://chocolatey.org/)

Alternatively, you may install FFmpeg manually and ensure it is added to
your system PATH.

------------------------------------------------------------------------

### 3️⃣ Install Python Dependencies

All required libraries are now included in `requirements.txt`.

Inside your project folder, run:

``` bash
pip install -r requirements.txt
```

This will install everything needed for both TTS engines.

------------------------------------------------------------------------

## 📁 Folder Structure

Create the following structure:

    project-folder/
    │
    ├── import/          # Place your CSV files here
    ├── output/          # Generated MP3 files will be saved here
    ├── google-tts.py
    ├── natural.py
    └── requirements.txt

### Setup Steps

1.  Create a **main project folder**
2.  Inside it, create:
    -   `import` → for CSV files\
    -   `output` → where MP3 files are saved\
3.  Place:
    -   `google-tts.py`
    -   `natural.py`
    -   `requirements.txt` inside the main project folder

------------------------------------------------------------------------

## 📄 CSV Specifications

-   **Format:** `.csv`
-   **Required Columns:**
    -   `Front`
    -   `Back`
-   **Naming:**
    -   The final MP3 file will be named exactly the same as the CSV
        file
-   **Location:**
    -   Place the CSV file inside the `import` folder

------------------------------------------------------------------------

## ⚙️ How the Scripts Work

Both scripts:

1.  Scan the `import` folder for the first CSV file found\
2.  Read the **Front** column text\
3.  Wait for the configured Front/Back pause\
4.  Read the **Back** column text\
5.  Wait for the configured next‑card pause\
6.  Export the combined audio to the `output` folder as an MP3

------------------------------------------------------------------------

## 🎙 Choosing Your TTS Engine

### ▶ Option 1: Google TTS

Run:

``` bash
python google-tts.py
```

Uses Google's text‑to‑speech engine.

Best for: - Simple setup - Cloud-based voice generation - Consistent
cross‑platform behavior

------------------------------------------------------------------------

### ▶ Option 2: Windows Natural Voices

Run:

``` bash
python natural.py
```

Uses Microsoft Windows built‑in natural AI voices.

Best for: - High-quality neural voices - Offline generation (after voice
installation) - Customizable voice selection

Note: Windows natural voices require Windows OS.

------------------------------------------------------------------------

## 🔧 Adjustable Variables (Inside the Scripts)

### 🎙 VOICE (natural.py only)

Example:

    en-GB-RyanNeural
    en-US-JennyNeural

Change this value to select a different Windows neural voice.

------------------------------------------------------------------------

### 🚀 SPEED

Adjust the speaking rate percentage (without changing pitch):

    +10%
    +20%
    -10%

------------------------------------------------------------------------

### ⏱ PAUSES

Silence is controlled in milliseconds:

-   `1000 = 1 second`

You can modify pause values to control silence between: - Front and
Back - Each flashcard

------------------------------------------------------------------------

## ▶️ Running the Project

1️⃣ Open Terminal or PowerShell inside your project folder

2️⃣ Run one of the following:

``` bash
python google-tts.py
```

or

``` bash
python natural.py
```

3️⃣ Wait until you see:

    Finished!

Your MP3 file will appear inside the `output` folder.

------------------------------------------------------------------------

## 🎉 Done!

Your flashcards will now be converted into natural‑sounding MP3 audio
files using your chosen TTS engine.
