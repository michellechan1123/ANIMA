# ANIMA
## Voice Integration and TTS of MotionInput

ANIMA is a TTS and voice cloning backend working on multiple languages. This repository is built upon Coqui TTS to provide a voice integration layer to UCL MotionInput, which contributes to my implementation of  my MSc Computer Science master's thesis.

## Features

- Voice cloning in English and Portuguese
- TTS in English, French and German
- Pdf to text (English only)
- docx to text (English only)
- image to text (English, Portuguese, French and German)


## Installation

ANIMA requires the dependencies below:
- Python <3.10
- ffmpeg (version-free)
- Tesseract-OCR exe (C:\Program Files)
- Visual studio C++ build 

## Play around with ANIMA (slow and not working atm)

### Voice cloning

```sh
 $ cli.py --text "example text" --voice_name "voice_name" --lang "lang_code" --out_file "out_filename.wav"
```

### TTS 
```sh
$ cli.py --text "example text" --lang "lang_code" --out_file "out_filename.wav"
```

## "audios" file structure
    | "default_speaker"
        | lang
            | out_audio_file
    | voice_name
        | lang
            | "input_voice.wav"
            | out_audio_file
