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
from kivy.clock import Clock


class ButtonDisplay(BoxLayout):
    pass


class ToolManager(GridLayout):
    """Controls the display containing the list of tools.
    Manages adding and removing tools.
    Provides FileBrowser access to tools for saving sessions."""
    tools = []
    path = None
    widget_display = ObjectProperty(None)
    remove_button = Button(text="Remove")
    cancel_button = Button(text="Cancel")
    confirm_button = Button(text="Confirm Remove")
    tool_height = 100

    def __init__(self, **kwargs):
        super(ToolManager, self).__init__(**kwargs)
        Clock.schedule_once(self.on_start)
        #self.button_display.add_widget(remove_button)
        #self.ids.button_display.add_widget(remove_button)
        #self.widget_display.bind(minimum_height=self.widget_display.setter('height'))

    def on_start(self, *args):
        self.remove_button.bind(on_release=self.open_remove_checkboxes)
        #self.confirm_button.bind(on_release=self.)
        self.cancel_button.bind(on_release=self.close_remove_checkboxes)
        self.ids.button_display.add_widget(self.remove_button)

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
        tool.height = self.tool_height
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
        """Enters mode to remove tools.
        Calls Tool method to add checkbox alongside it.
        Adds 'Cancel' and 'Confirm' buttons."""

        for tool in self.tools:
            tool.open_remove_checkbox()

        self.ids.button_display.remove_widget(self.remove_button)
        self.ids.button_display.add_widget(self.cancel_button)
        self.ids.button_display.add_widget(self.confirm_button)

    def close_remove_checkboxes(self, event):
        for tool in self.tools:
            tool.close_remove_checkbox()

        self.ids.button_display.remove_widget(self.confirm_button)
        self.ids.button_display.remove_widget(self.cancel_button)
        self.ids.button_display.add_widget(self.remove_button)

    def zoom_in(self):
        """Enlarges all tools."""
        self.tool_height += 20
        for tool in self.tools:
            tool.zoom(self.tool_height)

    def zoom_out(self):
        """Shrinks all tools"""
        self.tool_height -= 20
        for tool in self.tools:
            tool.zoom(self.tool_height)
