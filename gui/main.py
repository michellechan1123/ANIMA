from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty
import time
import random
import pyaudio
import wave
from src.ANIMA import ANIMA
from src.manage_audio import AudioManager


class MainApp(MDApp):
    harvard_sentences = ['Oak is strong and also gives shade',
                        'Cats and dogs each hate the other',
                        'The pipe began to rust while new',
                        "Open the crate but don't break the glass",
                        'Add the sum to the product of these three',
                        'Thieves who rob friends deserve jail',
                        'The ripe taste of cheese improves with age',
                        'Act on these orders with great speed',
                        'The hog crawled under the high fence',
                        'Move the vat over the hot fire']
    to_read = StringProperty(random.choice(harvard_sentences))

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        self.anima = ANIMA()
        self.audio_manager = AudioManager()
        self.audio = pyaudio.PyAudio()
        self.audio_stream = None
        self.audio_frames = None
        return Builder.load_file("styles.kv")

    def next_sentence(self):
        self.to_read = random.choice(self.harvard_sentences)

    def process(self):
        text = self.root.ids.input.text
        filename = self.root.ids.input_filename.text
        print("Text: ", text)
        print("Filename: ", filename)
        self.anima.tts_default_voice(text, filename, 'en')

    def file_selected(self, filename, text, output_filename):
        try:
            print("selected file: ", filename[0])
            print("inputted text: ", text)
            self.anima.voice_clone(text, filename[0], output_filename, "en")
        except IndexError:
            print("please select a file")

    def play_selected(self, filename):
        try:
            self.audio_manager.play_audio('en', filename[0])
        except IndexError:
            print("please select a file")

    def recording(self):
        self.audio_stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        self.audio_frames = []

        t_end = time.time() + 5
        while time.time() < t_end:
            data = self.audio_stream.read(1024)
            self.audio_frames.append(data)

    def start_recording(self):
        print("Recording in progress...")
        self.recording()

    def exit_recording(self):
        try:
            print("Recording stopped.")
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            sound_file = wave.open(self.root.ids.input_filename_voice.text, "wb")
            sound_file.setnchannels(1)
            sound_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(self.audio_frames))
            sound_file.close()
        except AttributeError:
            print("please enter a filename")


if __name__ == '__main__':
    MainApp().run()