import sys
import argparse
from src.ANIMA import ANIMA
from src.manage_audio import AudioManager
from src.pdf_to_txt import PdfToStrings
from src.docx_to_txt import DocxToStrings

def main():
    # Create the parser
    description = """
    This is a CLI to run ANIMA and demonstrates current features for TTS and voice-cloning. 

    Example commands are shown below:

    #list downloaded models for TTS and voice cloning
        $cli.py --list_models
    
    #list all saved audios 
        $cli.py --list_audios

    #voice cloning
        $cli.py --text "example text" --voice_name "voice_name" --lang "lang_code" --out_file "out_filename.wav"

    #tts
        $cli.py --text "example text" --lang "lang_code" --out_file "out_filename.wav"

    # (!!!) voice_cloning with pdf/docx
        $cli.py --txt_file "filename" ----voice_name "voice_name" --lang "lang_code" --out_file "out_filename.wav"

    # (!!!) tts with pdf/docx
        $cli.py --txt_file "filename" --lang "lang_code" --out_file "out_filename.wav"

    # (!!!) add language model in "models.json"
        $cli.py --model_type "model_type" --lang  "lang_code" --model_path "model_path"

    #create voice
        $cli.py --create --voice_name "voice_name" --lang "lang_code" --in_file "in_filename"

    # create voice with multiple files
        $cli.py --create --voice_name "voice_name" --lang "lang_code" --in_file_list "in_file1" "in_file2"

    #edit existing voice name
        $cli.py --in_file "in_filename.wav" --out_file "out_filename.wav"
    
    #edit existing audio name
        $cli.py --voice_name "voice_name" --lang "lang_code" --in_file "in_filename.wav" --out_file "out_filename.wav"

    #play audio 
        $cli.py --voice_name "voice_name" --lang "lang_code" --out_file "out_filename"

    #delete voice
        $cli.py --delete --voice_name "voice_name"

    #delete language
        $cli.py --delete --voice_name "voice_name" --lang "lang_code"

    #delete audio
        $cli.py --delete --voice_name "voice_name" --lang "lang_code" --in_file "in_filename"
    """
    parser = argparse.ArgumentParser(prog="anima", description=description, allow_abbrev=False, epilog="Enjoy ANIMA ;)")

    # Add arguments
    parser.add_argument("--list_models",
                        action="store_true",
                        help="List all downloaded TTS models and voice cloning models.")

    parser.add_argument("--list_audios",
                        action="store_true",
                        help="List all saved audios (.wav).")

    parser.add_argument("--lang",
                        type=str,
                        default=None,
                        help="Language for voice conversion or voice cloning.")

    parser.add_argument("--text_file",
                        type=str,
                        default=None,
                        help="Input text file.")

    parser.add_argument("--text",
                        type=str,
                        default=None,
                        help="Text for voice conversion or voice cloning.")

    parser.add_argument("--voice_name",
                        type=str,
                        default=None,
                        help="Voice input for speech generation.")

    parser.add_argument("--out_file",
                        type=str,
                        default=None,
                        help="Output .wav filename.")

    parser.add_argument("--in_file",
                        type=str,
                        default=None,
                        help="Input .wav filename.")

    parser.add_argument("--in_file_list",
                        nargs="+",
                        type=str,
                        default=[],
                        help="Input .wav files.")

    parser.add_argument("--model_type",
                        type=str,
                        default=None,
                        help="TTS model or voice cloning model.")

    parser.add_argument("--model_path",
                        type=str,
                        default=None,
                        help="Deep learning models path for speech generation.")

    parser.add_argument("--create",
                        nargs='?',
                        const=True,
                        help="Create voice for voice cloning")

    parser.add_argument("--delete",
                        nargs='?',
                        const=True,
                        help="Delete voice, voice in a language, audio")

    # Execute the parse_args() method
    args = parser.parse_args()

    anima = ANIMA()
    audio_manager = AudioManager()
    pdf_to_str = PdfToStrings()
    docx_to_str = DocxToStrings()

    #list models for TTS and voice cloning
    if args.list_models:
        anima.list_language_models()
        sys.exit()

    #list all saved audios 
    if args.list_audios:
        audio_manager.list_audio()
        sys.exit()

    lang = args.lang
    text = args.text 
    txt_file = args.text_file
    voice_name = args.voice_name
    in_file_list = args.in_file_list
    in_file = args.in_file
    out_file = args.out_file
    model_type = args.model_type
    model_path = args.model_path

    #voice cloning
    voice_cloning_args = [lang, text, voice_name, out_file]
    valid_voice_cloning_args = all(arg is not None for arg in voice_cloning_args)

    if valid_voice_cloning_args:
        in_dir, out_dir = audio_manager.dir_audio_to_folder(lang, out_file, voice_name)
        anima.voice_clone(text, in_dir, out_dir, lang)
        sys.exit()
        
  
    #tts
    tts_args = [lang, text, out_file]
    valid_tts_args = all(arg is not None for arg in tts_args)

    if valid_tts_args:
        in_dir, out_dir = audio_manager.dir_audio_to_folder(lang, out_file)
        anima.tts_default_voice(text, out_dir, lang)
        sys.exit()

    # (!!!) voice_cloning with pdf/docx
    # $cli.py --txt_file "filename" ----voice_name "voice_name" --lang "lang_code" --out_file "out_filename.wav"
    voice_cloning_txt_args = [lang, txt_file, voice_name, out_file]
    valid_voice_cloning_txt_args = all(arg is not None for arg in voice_cloning_txt_args)

    if valid_voice_cloning_txt_args:
        if ".pdf" in txt_file:
            pdf_to_str.pdf_to_str(txt_file, )
            in_dir, out_dir = audio_manager.dir_audio_to_folder(lang, out_file, voice_name)
            anima.voice_clone(text, in_dir, out_dir, lang)
            sys.exit()


    # (!!!) tts with pdf/docx
    #$cli.py --txt_file "filename" --lang "lang_code" --out_file "out_filename.wav"


    #add language model in "models.json"
    add_model_args = [lang, model_type, model_path]
    valid_add_model_args = all(arg is not None for arg in add_model_args)

    if valid_add_model_args:
        anima.add_language_model(model_type, lang, model_path)
        sys.exit()


    #edit existing audio name 
    edit_audio_name_args = [voice_name, lang, in_file, out_file]
    valid_audio_name_args = all(arg is not None for arg in edit_audio_name_args)

    if valid_audio_name_args:
        audio_manager.edit_audio_name(lang, in_file, out_file, voice_name)
        sys.exit()

    #play audio 
    play_audio_args = [voice_name, lang, out_file]
    valid_play_audio_args = all(arg is not None for arg in play_audio_args)

    if valid_play_audio_args:
        audio_manager.play_audio(lang, out_file, voice_name)
        sys.exit()

    #create voice
    create_voice_args = [args.create, voice_name, lang, in_file]
    valid_create_voice_args = all(arg is not None for arg in create_voice_args)

    if valid_create_voice_args:
        audio_manager.create_voice(voice_name, lang, in_file)
        sys.exit()

    #create voice with multiple voices 
    create_voice_multi_args = [args.create, voice_name, lang, in_file_list]
    valid_create_voice_multi_args = all(arg is not None for arg in create_voice_multi_args)

    if valid_create_voice_multi_args:
        file_path = audio_manager.combine_wav_files(in_file_list)
        audio_manager.create_voice(voice_name, lang, file_path)
        sys.exit()


    #delete audio
    delete_voice_args = [args.delete, voice_name, lang, in_file]
    valid_delete_voice_args = all(arg is not None for arg in delete_voice_args)

    if valid_delete_voice_args:
        audio_manager.delete_voice(voice_name, lang, in_file)
        sys.exit()

    #delete language
    delete_voice_args = [args.delete, voice_name, lang]
    valid_delete_voice_args = all(arg is not None for arg in delete_voice_args)

    if valid_delete_voice_args:
        audio_manager.delete_voice(voice_name, lang)
        sys.exit()

    #delete voice
    delete_voice_args = [args.delete, voice_name]
    valid_delete_voice_args = all(arg is not None for arg in delete_voice_args)

    if valid_delete_voice_args:
        audio_manager.delete_voice(voice_name)
        sys.exit()

    #edit existing voice name
    edit_voice_name_args = [in_file, out_file]
    valid_voice_name_args = all(arg is not None for arg in edit_voice_name_args)

    if valid_voice_name_args:
        audio_manager.edit_voice_name(in_file, out_file)
        sys.exit()


if __name__ == "__main__":
    main()


