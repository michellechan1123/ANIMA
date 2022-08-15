import unittest
from src.manage_audio import AudioManager
import pathlib

class ManageAudioTest(unittest.TestCase):
    def setUp(self):
        self.audio_manager = AudioManager()

    def test_play_audio_invalid_lang(self):
        with self.assertRaises(Exception):
            self.audio_manager.play_audio("ch", "input_voice.wav", "Daisy")

    def test_play_audio_invalid_file_path(self):
        with self.assertRaises(Exception):
            self.audio_manager.play_audio("en", "any_file.wav", "Daisy")

    def test_play_audio_invalid_voice_name(self):
       with self.assertRaises(Exception):
            self.audio_manager.play_audio("en", "input_voice.wav", "Lily")

    def test_play_audio_invalid_default_lang(self):
       with self.assertRaises(Exception):
            self.audio_manager.play_audio("ch", "bathroom.wav")

    def test_play_audio_invalid_default_file_path(self):
       with self.assertRaises(Exception):
            self.audio_manager.play_audio("en", "kitchen.wav")


    def test_combine_wav_files_invalid(self):
        with self.assertRaises(Exception):
            self.audio_manager.combine_wav_files([])
        
    def test_combine_wav_files(self):
        wav_list = ["tests/test_files/sample1.wav", "tests/test_files/sample2.wav", "tests/test_files/sample3.wav"]
        self.audio_manager.combine_wav_files(wav_list)

        path = pathlib.Path("input_voice.wav")
        self.assertTrue(path.is_file())

        for wav in wav_list:
            wav_file = pathlib.Path(wav)
            self.assertFalse(wav_file.is_file())


    def test_edit_voice_name_invalid_voice_name(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.edit_voice_name("Jerry", "Lily")

    def test_edit_voice_name_invalid_new_voice_name(self):
        with self.assertRaises(self.audio_manager.InvalidDuplicatePath):
            self.audio_manager.edit_voice_name("Daisy", "Peter")

    def test_edit_voice_name(self):
        self.audio_manager.edit_voice_name("Daisy", "Jerry")

        path = pathlib.Path("audios/Jerry")
        self.assertTrue(path.is_dir())

        self.audio_manager.edit_voice_name("Jerry", "Daisy")


    def test_edit_audio_name_invalid_voice_name(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.edit_audio_name("en", "peter_self_intro.wav", "new_name.wav", "Jerry")

    def test_edit_audio_name_invalid_lang(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.edit_audio_name("fr", "peter_self_intro.wav", "new_name.wav", "Peter")

    def test_edit_audio_name_invalid_audio_name(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.edit_audio_name("en", "any_name.wav", "new_name.wav", "Peter")

    def test_edit_audio_name_invalid_new_audio_name(self):
        with self.assertRaises(self.audio_manager.InvalidDuplicatePath):
            self.audio_manager.edit_audio_name("en", "peter_self_intro.wav", "peter_self_intro2.wav", "Peter")

    def test_edit_audio_name(self):
        self.audio_manager.edit_audio_name("en", "peter_self_intro.wav", "new_name.wav", "Peter")

        self.audio_manager.edit_audio_name("en", "new_name.wav", "peter_self_intro.wav", "Peter")

    def test_edit_audio_name_default_speaker(self):
        self.audio_manager.edit_audio_name("en", "bathroom.wav", "new_name.wav")

        self.audio_manager.edit_audio_name("en", "new_name.wav", "bathroom.wav")


    def test_create_voice_invalid_voice_name_lang(self):
        with self.assertRaises(self.audio_manager.InvalidDuplicatePath):
            self.audio_manager.create_voice("Daisy", "en", "tests/test_files/sample4.wav")

    def test_create_voice_invalid_file_path(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.create_voice("Jerry", "en", "tests/test_files/sample10.wav")

    def test_create_voice(self):
        self.audio_manager.create_voice("Jerry", "en", "tests/test_files/sample5.wav")


    def test_delete_voice_invalid_default_speaker_voice_name(self):
        with self.assertRaises(self.audio_manager.InvalidVoiceName):
            self.audio_manager.delete_voice("default_speaker")

    def test_delete_voice_invalid_voice_name(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.delete_voice("Warren")

    def test_delete_voice_invalid_lang(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.delete_voice("Daisy", "fr")

    def test_delete_voice_invalid_file(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.delete_voice("Daisy", "en", "toilet.wav")

    def test_delete_voice_invalid_lang_file(self):
        with self.assertRaises(self.audio_manager.InvalidPath):
            self.audio_manager.delete_voice("Daisy", None, "self_intro.wav")

    def test_delete_voice_audio(self):
        self.audio_manager.delete_voice("Jerry", "en", "input_voice.wav")

    def test_delete_voice_lang(self):
        self.audio_manager.delete_voice("Jerry", "en")

    def test_delete_voice_voice_name(self):
        self.audio_manager.delete_voice("Jerry")


    



