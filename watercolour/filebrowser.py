import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.image import Image
from kivy.core.image import Image as Image

import os
from kivy.clock import Clock

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class FileBrowser(BoxLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    confirm_image = ObjectProperty(None)
    #global PATH

    def __init__(self, **kwargs):
        super(FileBrowser, self).__init__(**kwargs)
        #Clock.schedule_once(self.on_start)

    #def on_start(self, *args):
        #self.ids.confirm_image(text=self.confirm_image)


    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        path = os.path.join(path, filename[0])
        self.ids.confirm_image.source = path
        #self.PATH = os.path.join(path, filename[0])

        #with open(os.path.join(path, filename[0]), encoding="utf8") as stream:
         #   self.text_input.text = stream.read()

        self.dismiss_popup()