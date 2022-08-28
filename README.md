# ANIMA
## Voice Integration and TTS of MotionInput

ANIMA is a TTS and voice cloning backend working on multiple languages. This repository is built upon Coqui TTS to provide a voice integration layer to UCL MotionInput, which contributes to the implementation of my MSc Computer Science master's thesis.

## Features

- Voice cloning in English and Portuguese
- TTS in English, French and German
- Pdf to text (English only)
- image to text (English, Portuguese, French and German)


## Installation

ANIMA requires the dependencies below:
- Python <3.10
- Visual studio C++ build 
- ffmpeg (version-free)
- Tesseract-OCR exe (C:\Program Files)

## Play around with ANIMA CLI

### Voice cloning

```sh
 $ cli.py --voice_clone --text "example text" --voice_name "voice_name" --lang "lang_code" --out_file "out_filename.wav"
```

### TTS 
```sh
$ cli.py --tts --text "example text" --lang "lang_code" --out_file "out_filename.wav"
```

## "audios" file structure
    | "default_speaker"
        | lang
            | out_audio_file
    | voice_name
        | lang
            | "input_voice.wav"
            | out_audio_file
            
 ## "models.json" data structure
    {
        "TTS_models": {
            "lang": {
                "tts_model": "tts_models/lang/dataset/model_name"
            }
        },
        "voice_cloning_models": {
            "lang": {
                "tts_model": "tts_models/lang/dataset/model_name"
            }
        }
    }
