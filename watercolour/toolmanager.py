from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from watercolour.tool import Tool

class ToolManager(GridLayout):
    tools = []
    path = None

    def add_tool(self):
        tool = Tool(self.path)
        self.ids.widget_display.add_widget(tool)

    def remove_tool(self):
        pass

    def add_widget_to_grid(self):
        img = Image(source='D:/Projects/watercolour-spikes/146081236_890288241737602_904200711451988803_n.png')
        img.size_hint = 1, None
        img.width = self.ids.widget_display.width / self.ids.widget_display.cols
        img.size = 167, (self.ids.widget_display.width / self.ids.widget_display.cols)
        print("gridview width / cols =", (self.ids.widget_display.width / self.ids.widget_display.cols))
        self.ids.widget_display.add_widget(img)

    def set_path(self, path):
        self.path = path