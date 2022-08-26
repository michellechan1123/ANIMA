from pathlib import Path
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import json
import os
import shutil

#ModelManager and Synthesizer are taken from TTS utils library.

class ANIMA(): 
    """
    Synthesises TTS with default speaker or voice cloning in a variety of languages.

    Models must be downloaded under AppData/Local/tts before usage with internet connection. 
    All models can be found in https://github.com/coqui-ai/TTS release. 

    Alternative is to run $ tts --text "Text for TTS" --model_name "<model_type>/<language>/<dataset>/<model_name>" --out_path output/path/speech.wav with internet connection.
    Additional language models can be added.

    The following models are downloaded and provided with corresponding languages in 'models.json':
        Voice cloning:
            English: tts_models/multilingual/multi-dataset/your_tts --"en"
            Portuguese: tts_models/multilingual/multi-dataset/your_tts --"pt"
        
        TTS:
            English: tts_models/en/ljspeech/tacotron2-DDC
            German: tts_models/de/thorsten/vits
            French: tts_models/fr/mai/tacotron2-DDC
    """

    def __init__(self) -> None:
        self.path = Path(__file__).parent / ".models.json"
        self.manager = ModelManager(self.path)
        self.model_path = None
        self.config_path = None
        self.model_item = None
        self.speakers_path = None
        self.language_ids_path = None
        self.vocoder_path = None
        self.vocoder_config_path = None
        self.encoder_path = None
        self.encoder_config_path = None
        self.use_cuda = False
        self.__download_init_models()


    def tts_default_voice(self, text: str, filename: str, lang: str):
        """
        Converts text to synthesize speech as a .wav file and speaks the speech with a default voice. 

        Output wav must be declared with desirable path and filename as a string. 

        English ("en"), french ("fr") and german ("de") are available for TTS. English are set as default.

        Args: 
            text (str): desired text to undergo TTS
            filename (str): output filename in path/output_speech.wav format
            lang (str): language code
        """

        self.__check_filename(filename)
        self.__check_lang_len(lang)

        model_path = self.__select_lang("TTS_models", lang)
        self.model_path, self.config_path, self.model_item = self.manager.download_model(model_path)
        synthesizer = Synthesizer(
            self.model_path,
            self.config_path,
            self.speakers_path,
            self.language_ids_path,
            self.vocoder_path,
            self.vocoder_config_path,
            self.encoder_path,
            self.encoder_config_path,
            self.use_cuda
        )

        wavs = synthesizer.tts(text, language_name=lang)
        synthesizer.save_wav(wavs, filename)
        print(f"The file {filename} has been saved!")


    def voice_clone(self, text: str, speaker_wav: str, filename: str, lang: str):
        """
        Real time voice cloning of an input voice .wav to oupt a digital voice .wav.

        Both English ("en") and Portugese ("pt") are available using YourTTS model in Coqui and the desired language can be specified in lang.
        
        Args:
            text (str): desired text to undergo TTS
            speaker_wav (str): input filename in path/input_speech.wav format
            filename (str): output filename in path/output_speech.wav format
            lang (str): language code 
        """

        self.__check_filename(speaker_wav)
        self.__check_filename(filename)
        self.__check_lang_len(lang)

        model_path = self.__select_lang("voice_cloning_models", lang)
        self.model_path, self.config_path, self.model_item = self.manager.download_model(model_path)
        synthesizer = Synthesizer(
            self.model_path,
            self.config_path,
            self.speakers_path,
            self.language_ids_path,
            self.vocoder_path,
            self.vocoder_config_path,
            self.encoder_path,
            self.encoder_config_path,
            self.use_cuda
        )

        wavs = synthesizer.tts(text, language_name=lang, speaker_wav=speaker_wav)
        synthesizer.save_wav(wavs, filename)
        print(f"The file {filename} has been saved!")


    def add_language_model(self, model_type: str, lang: str, model_name: str):
        """
        Add language model in 'models.json'. Download added models.

        Args: 
            model_type (str): TTS_models or voice_cloning_models
            lang (str): language code
            model_name (str): file path in model_type/language/dataset/model_name format
        """
        self.__check_lang_len(lang)
        self.__check_model_type(model_type)

        with open("models.json", 'r+') as file:
            file_str = file.read()
            file_data = json.loads(file_str)

            if lang in file_data[model_type]:
                raise self.InvalidDuplicateLanguage()

            self.manager.download_model(model_name)

            file_data[model_type][lang] = {}
            file_data[model_type][lang]["tts_model"] = model_name

            file.seek(0)
            json.dump(file_data, file, indent=4)


    #bug: Duplicating character sometimes occur at the end of models.json when deleting language model
    def remove_language_model(self, lang: str, model_type: str):
        """
        Remove language model in "models.json". Delete model folder. 

        Args: 
            lang (str): language code 
            model_type (str): TTS_models or voice_cloning_models
        """

        self.__check_lang_len(lang)
        self.__check_model_type(model_type)

        with open("models.json", 'r+') as file:
            file_str = file.read()
            file_data = json.loads(file_str)

            model_path = file_data[model_type][lang]["tts_model"]
            model_name = model_path.replace("/", "--")

            parent_path = Path.home()
            base_path = os.path.join(parent_path, "AppData", "Local", "tts")

            new_model_path = os.path.join(base_path, model_name)

            try:
                shutil.rmtree(new_model_path)

                file_data[model_type].pop(lang)

            except:
                raise self.InvalidLanguage()
            
            file.seek(0)
            json.dump(file_data, file, indent=15)


    def list_language_models(self):
        """
        List all downloaded models. 
        """
        with open("models.json", 'r') as file:
            file_str = file.read()
            file_data = json.loads(file_str)

            for model_type in file_data:
                print(f"{model_type}:")
                for lang_model in file_data[model_type]:
                    print(f"    {lang_model}:")
                    for model in file_data[model_type][lang_model]:
                        print(f"        {model}: {file_data[model_type][lang_model][model]}")
                print("")


    def __select_lang(self, model_type:str, lang:str):
        """
        Selects the requested language file path.

        Args: 
            model_type (str): TTS_models or voice_cloning_models
            lang (str): language code
        """

        with open("models.json", 'r') as file:
            file_str = file.read()
            file_data = json.loads(file_str)
            model_list = []

            
            for lang_model in file_data[model_type]:
                if lang == lang_model:
                    for model in file_data[model_type][lang_model]:
                        tts_model = file_data[model_type][lang_model][model]
                    return tts_model
                
            raise self.InvalidLanguage()

        
    def __check_filename(self, filename):
        """
        Check if filename ends with ".wav"

        Args: 
            filename (str): filename in path/speech.wav format
        """
        filename_len = len(filename) 

        if filename_len < 4 or filename[(filename_len - 4): filename_len] != ".wav":
            raise self.InvalidFilename()


    def __check_lang_len(self, lang):
        """
        Check if language code length is 2

        Args: 
            lang (str): language code 
        """
        if len(lang) != 2:
            raise self.InvalidLanguageCodeLength()
    

    def __check_model_type(self, model_type:str):
        """
        Check if model_type is either TTS_models or voice_cloning_models

        Args: 
            model_type (str): TTS_models or voice_cloning_models
        """
        if model_type == "TTS_models":
            return
        else:
            raise self.InvalidModelType()

    def __download_init_models(self):
        """
        Download initial language models. 
        """
        init_models = {
            "multi": "tts_models/multilingual/multi-dataset/your_tts",
            "en": "tts_models/en/ljspeech/tacotron2-DDC",
            "de": "tts_models/de/thorsten/vits",
            "fr": "tts_models/fr/mai/tacotron2-DDC"
        }

        for lang, model_path in init_models.items():
            self.manager.download_model(model_path)

        print("\n")
            

    class InvalidLanguage(Exception):
        def __init__(self) -> None:
            super().__init__(f"Invalid language: the language model does not exist")


    class InvalidDuplicateLanguage(Exception):
        def __init__(self) -> None:
            super().__init__(f"Invalid language: the language model already exists")


    class InvalidFilename(Exception):
        def __init__(self) -> None:
            super().__init__(f"Invlid filename: the filename must end with \".wav\"")


    class InvalidLanguageCodeLength(Exception):
        def __init__(self) -> None:
            super().__init__(f"Invalid language code: the language code must only consist of two alphabets")


    class InvalidModelType(Exception):
        def __init__(self) -> None:
            super().__init__(f"Invalid model type: the model can only be TTS_models or voice_cloning models")