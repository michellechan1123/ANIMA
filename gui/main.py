from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty
import random
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

    def process_toggle_recording(self):
        print("toggle state: " + self.root.ids.toggle_recording.state)
        if self.root.ids.toggle_recording.state == "normal":
            self.root.ids.toggle_recording.text = "Start Recording"
            self.root.ids.toggle_recording.color = (1, 1, 1, 1)
        else:
            self.root.ids.toggle_recording.text = "Recording..."
            self.root.ids.toggle_recording.color = (0, 0, 0, 1)


if __name__ == '__main__':
    MainApp().run()