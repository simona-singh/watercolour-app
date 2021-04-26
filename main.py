import kivy

from watercolour.watercolourapp import WatercolourApp

from kivy.factory import Factory
from watercolour.filebrowser import FileBrowser
from watercolour.tool import Tool

Factory.register('FileBrowser', cls=FileBrowser) # sets filebrowser global so path can be accessed
Factory.register('Tool', cls=Tool) # sets filebrowser global so path can be accessed


if __name__ == '__main__':
    WatercolourApp().run()