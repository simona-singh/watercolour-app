import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.image import Image
from kivy.core.image import Image as Image

import os
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.app import App
import json as json


class LoadDialog(FloatLayout):
    """The pop up dialog for the 'load' button"""
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class FileBrowser(BoxLayout):
    """FileBrowser handles selecting and updating image paths, and save/load sessions.
    A session includes instances of tools and corresponding image path and slider values set."""
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    confirm_image = ObjectProperty(None)
    path = None

    def __init__(self, **kwargs):
        """Initialises FileBrowser instance."""
        super(FileBrowser, self).__init__(**kwargs)
        self.app = App.get_running_app()
        #Clock.schedule_once(self.on_start)

    #def on_start(self, *args):
        #self.ids.confirm_image(text=self.confirm_image)


    def dismiss_popup(self):
        """Closes load dialog popup window."""
        self._popup.dismiss()

    def show_load(self):
        """Opens load dialog popup window."""
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        """Handles the path selected from load dialog.
        Updates ColourViewer and ToolManager path setters.
        Calls methods to handle updating colour chart."""
        path = os.path.join(path, filename[0])
        self.ids.confirm_image.source = path
        self.parent.parent.tool_manager.set_path(path)
        self.parent.parent.colour_viewer.image_viewer.set_path(path)
        self.parent.parent.colour_viewer.image_viewer.remove_chart()
        self.parent.parent.colour_viewer.image_viewer.colour_chart()
        #self.app.root.ids.tool_image.source = path
        #Factory.Tool.set_path(path)
        #self.ids.actual_image.source = path
        #root.ids.tool.ids.tool_image.source = path
        self.set_path(path)
        #self.PATH = os.path.join(path, filename[0])

        #with open(os.path.join(path, filename[0]), encoding="utf8") as stream:
         #   self.text_input.text = stream.read()

        self.dismiss_popup()

    def get_path(self):
        """Gets current path."""
        return self.path

    def set_path(self, path):
        """Updates path."""
        self.path = path

    def load_session(self):
        pass

    def save_session(self):
        """Generates JSON file from dictionary containing tools."""
        tools = self.parent.parent.tool_manager.get_tools()
        settings = {}
        for tool in tools:
            if type(tool).__name__ in settings:
                settings[type(tool).__name__].append(tool.get_settings())
            else:
                settings[type(tool).__name__] = []
                settings[type(tool).__name__].append(tool.get_settings())

        contents = json.dumps(settings)
        print(settings)
        print(tools)
        f = open("./sessions/settings.txt", "w")
        f.write(contents)
        f.close()
