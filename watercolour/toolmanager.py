from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from watercolour.tool import Tool
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from watercolour.tools.averagecolour import AverageColour
from watercolour.tools.saturation import Saturation
from watercolour.tools.temperature import Temperature
from watercolour.tools.thresholdingvalues import ThresholdingValues

class ToolManager(GridLayout):
    tools = []
    path = None
    widget_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ToolManager, self).__init__(**kwargs)
        #self.widget_display.bind(minimum_height=self.widget_display.setter('height'))

    def add_tool(self):
        name = self.ids.btn.text
        tool = None

        if name == 'Temperature':
            tool = Temperature(self.path)
        elif name == 'Saturation':
            tool = Saturation(self.path)
        elif name == 'Values':
            tool = ThresholdingValues(self.path)
        elif name == 'Average Colour':
            tool = AverageColour(self.path)

        tool.set_label(name)
        self.tools.append(tool)
        self.ids.widget_display.add_widget(tool)

    def remove_tool(self):
        pass

    def add_widget_to_grid(self):
        img = Image(source='D:/Projects/watercolour-spikes/146081236_890288241737602_904200711451988803_n.png')
        img.size_hint = 1, None
        #img.width = self.ids.widget_display.width / self.ids.widget_display.cols
        #img.size = 167, (self.ids.widget_display.width / self.ids.widget_display.cols)
        print("gridview width / cols =", (self.ids.widget_display.width / self.ids.widget_display.cols))
        self.ids.widget_display.add_widget(img)

    def set_path(self, path):
        self.path = path

    def hide_others(self, current):
        for tool in self.tools:
            if tool is not current:
                tool.hide()

    def show_others(self, current):
        for tool in self.tools:
            if tool is not current:
                tool.show()