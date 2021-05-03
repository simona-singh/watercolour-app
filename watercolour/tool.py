#from kivy.core.image import Image as Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.factory import Factory
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty

class Tool(BoxLayout):
    tool_image = ObjectProperty(None)
    path = None

    def __init__(self, path):
        super().__init__()
        #Clock.schedule_once(self._finish_init)
        #self.img = Image(self.parent.parent.parent.get_path())
        self.set_path(path)
        #self.add_widget(self.img)

    def _finish_init(self, path):
        #self.img = Image(source=self.ids.filebrowser.get_path())
        #self.img.size_hint = 1, None
        self.set_path(path)

    def open_tool(self):
        pass

    def close_tool(self):
        pass

    def set_path(self, path):
        self.path = path
        self.ids.tool_image.source = path

    def set_label(self, name):
        self.ids.lbl.text = name