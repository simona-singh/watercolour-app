from kivy.app import App
from kivy.properties import ObjectProperty
from watercolour.tabmanager import TabManager
from watercolour.filebrowser import FileBrowser
from watercolour.colourviewer import ColourViewer
from watercolour.toolmanager import ToolManager

class WatercolourApp(App):
    tab_mgr = ObjectProperty
    # filebrowser = FileBrowser()
    # colourviewer = ColourViewer()
    # toolmanager = ToolManager()

    def build(self):
        self.tab_mgr = TabManager()
        return self.tab_mgr