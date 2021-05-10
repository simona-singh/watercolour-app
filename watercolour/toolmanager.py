from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from watercolour.tool import Tool
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from watercolour.tools.averagecolour import AverageColour
from watercolour.tools.saturation import Saturation
from watercolour.tools.temperature import Temperature
from watercolour.tools.thresholdingvalues import ThresholdingValues
from kivy.factory import Factory
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
Factory.register('saturation', cls=Saturation)

class ToolManager(GridLayout):
    """Controls the display containing the list of tools.
    Manages adding and removing tools.
    Provides FileBrowser access to tools for saving sessions."""
    tools = []
    path = None
    widget_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ToolManager, self).__init__(**kwargs)
        #self.widget_display.bind(minimum_height=self.widget_display.setter('height'))

    def add_tool(self):
        """Selects corresponding tool from drop down selection.
        Adds tool to list of current tools and adds it to display."""
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
        """Not used?"""
        img = Image(source='D:/Projects/watercolour-spikes/146081236_890288241737602_904200711451988803_n.png')
        img.size_hint = 1, None
        #img.width = self.ids.widget_display.width / self.ids.widget_display.cols
        #img.size = 167, (self.ids.widget_display.width / self.ids.widget_display.cols)
        print("gridview width / cols =", (self.ids.widget_display.width / self.ids.widget_display.cols))
        self.ids.widget_display.add_widget(img)

    def set_path(self, path):
        """Updates local path variable."""
        self.path = path

    def hide_others(self, current):
        """Hides all tools except selected so the current tool can be expanded."""
        for tool in self.tools:
            if tool is not current:
                tool.hide()

    def show_others(self, current):
        """Shows all tools after current tool has been minimised."""
        for tool in self.tools:
            if tool is not current:
                tool.show()

    def get_tools(self):
        """Returns list of tool objects."""
        return self.tools

    def open_remove_checkboxes(self, event):
        print("inside")
        confirm = Button(text='Confirm')
        self.ids.buttons.add_widget(confirm)
        print(self.ids.remove_btn.text)
        for tool in self.tools:
            tool.open_remove_checkbox()
        self.ids.remove_btn.text = 'Cancel'
        self.ids.remove_btn.bind(on_press=self.close_remove_checkboxes)
        #self.ids.remove_btn.on_release = self.close_remove_checkboxes

    def close_remove_checkboxes(self, event):
        self.ids.remove_btn.text = 'Remove'
        self.ids.remove_btn.bind(on_press=self.open_remove_checkboxes)
        #self.ids.remove_btn.on_release = self.open_remove_checkboxes
        for tool in self.tools:
            tool.open_remove_checkbox()

    def zoom_in(self):
        for tool in self.tools:
            h = tool.ids.tool_image.height
            tool.ids.tool_image.height = h + 10

    def zoom_out(self):
        pass