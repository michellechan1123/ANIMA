# ANIMA
## Voice Integration and TTS of MotionInput

ANIMA is a TTS and voice cloning backend working on multiple languages. This repository is built upon Coqui TTS to provide a voice integration layer to UCL MotionInput and an alternative open source voice integration toolkit to Intel.

## Features

- Voice cloning in English and Portuguese
- TTS in English, French and German
- Pdf to text (English only)
- image to text (English, Portuguese, French and German)


## Installation

ANIMA requires the dependencies below and download all of these and place it in the location as indicated (if applicable):
- Python 3.7<= and <3.10
- Visual studio C++ build 
- ffmpeg (version-free)
- Tesseract-OCR exe (C:\Program Files)

Then run:
```sh
 $ pip install -r requirements.txt 
```

## Play around with ANIMA CLI

### Voice cloning

```sh
 $ py cli.py --voice_clone --text "example text" --voice_name "voice_name" --lang "lang_code" --out_file "out_filename.wav"
```

### TTS 
```sh
$ py cli.py --tts --text "example text" --lang "lang_code" --out_file "out_filename.wav"
```

## "audios" file structure
    | "audios"
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
