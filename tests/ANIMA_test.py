import unittest
import pathlib
import os
from pathlib import Path
from src.ANIMA import ANIMA

class ANIMATest(unittest.TestCase):
    def setUp(self):
        self.anima = ANIMA()

    def test_tts_default_voice_invalid_filename(self):
        with self.assertRaises(self.anima.InvalidFilename):
            self.anima.tts_default_voice("This is a test one", "test1.mp3", "en")

    def test_tts_default_voice_invalid_txt(self):
        with self.assertRaises(TypeError):
            self.anima.tts_default_voice(123, "test2.wav", "en")

    def test_tts_default_voice_invalid_lang_code_len(self):
        with self.assertRaises(self.anima.InvalidLanguageCodeLength):
            self.anima.tts_default_voice("This is a test three", "test3.wav", "eng")

    def test_tts_default_voice_invalid_lang(self):
        with self.assertRaises(self.anima.InvalidLanguage):
            self.anima.tts_default_voice("This is a test four", "test4.wav", "ch")

    def test_tts_default_voice_valid_out_file(self):
        self.anima.tts_default_voice("This is a test five", "test5.wav", "en")
        path = pathlib.Path("test5.wav")
        self.assertTrue(path.is_file())
        self.assertTrue(path.parent.is_dir())


    def test_voice_clone_invalid_in_filename(self):
        with self.assertRaises(self.anima.InvalidFilename):
            self.anima.voice_clone("This is a test six", "in_voice.mp3", "test6.wav", "en")

    def test_voice_clone_invalid_out_filename(self):
        with self.assertRaises(self.anima.InvalidFilename):
            self.anima.voice_clone("This is a test seven", "audios/Daisy/en/input_voice.wav", "test7.mp3", "en")

    def test_voice_clone_invalid_txt(self):
        with self.assertRaises(TypeError):
            self.anima.voice_clone(123, "audios/Daisy/en/input_voice.wav", "test8.wav", "en")

    def test_voice_clone_invalid_lang_code_len(self):
        with self.assertRaises(self.anima.InvalidLanguageCodeLength):
            self.anima.voice_clone("This is a test nine", "audios/Daisy/en/input_voice.wav", "test9.wav", "eng")

    def test_voice_clone_invalid_lang(self):
        with self.assertRaises(self.anima.InvalidLanguage):
            self.anima.voice_clone("This is a test ten", "audios/Daisy/en/input_voice.wav", "test10.wav", "ch")

    def test_voice_clone_valid_out_file(self):
        self.anima.voice_clone("This is a test eleven", "audios/Daisy/en/input_voice.wav", "test11.wav", "en")
        path = pathlib.Path("test11.wav")
        self.assertTrue(path.is_file())
        self.assertTrue(path.parent.is_dir())

    def test_voice_clone_valid_in_file(self):
        self.anima.voice_clone("This is a test twelve", "audios/Daisy/en/input_voice.wav", "test12.wav", "en")
        path = pathlib.Path("audios/Daisy/en/input_voice.wav")
        self.assertTrue(path.is_file())
        self.assertTrue(path.parent.is_dir())


    def test_add_language_model_invalid_model_type(self):
        with self.assertRaises(self.anima.InvalidModelType):
            self.anima.add_language_model("any_model", "ja", "tts_models/ja/kokoro/tacotron2-DDC")

    def test_add_language_model_invalid_lang_code_len(self):
        with self.assertRaises(self.anima.InvalidLanguageCodeLength):
            self.anima.add_language_model("TTS_models", "jap", "tts_models/ja/kokoro/tacotron2-DDC")

    def test_add_language_model_invalid_duplicate_lang(self):
        with self.assertRaises(self.anima.InvalidDuplicateLanguage):
            self.anima.add_language_model("TTS_models", "en", "tts_models/ja/kokoro/tacotron2-DDC")

    def test_add_language_model_invalid_model_name(self):
        with self.assertRaises(Exception):
            self.anima.add_language_model("TTS_models", "ja", "any_model")

    def test_add_language_model_valid(self):
        model_path = "tts_models/ja/kokoro/tacotron2-DDC"
        self.anima.add_language_model("TTS_models", "ja", model_path)
        
        parent_path = Path.home()
        model_name = model_path.replace("/", "--")
        path = os.path.join(parent_path, "AppData", "Local", "tts", model_name)
        tts_model_path = pathlib.Path(path)
        self.assertTrue(tts_model_path.is_dir())

    def test_remove_language_model_invalid_model_type(self):
        with self.assertRaises(self.anima.InvalidModelType):
            self.anima.remove_language_model("ja", "any_model")

    def test_delete_language_model_invalid_lang_code_len(self):
        with self.assertRaises(self.anima.InvalidLanguageCodeLength):
            self.anima.remove_language_model("jap", "TTS_models")

    def test_delete_language_model_invalid_lang(self):
        with self.assertRaises(self.anima.InvalidLanguage):
            self.anima.remove_language_model("ch", "TTS_models")

    def test_delete_language_model_valid(self):
        model_path = "tts_models/ja/kokoro/tacotron2-DDC"
        self.anima.remove_language_model("ja", "TTS_models")

        parent_path = Path.home()
        model_name = model_path.replace("/", "--")
        path = os.path.join(parent_path, "AppData", "Local", "tts", model_name)
        tts_model_path = pathlib.Path(path)
        self.assertFalse(tts_model_path.is_dir())

        

        
