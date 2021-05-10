#from kivy.core.image import Image as Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.factory import Factory
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.checkbox import CheckBox
class ButtonGrid(ButtonBehavior, GridLayout):
    pass

class Tool(BoxLayout):
    """The base class Tool which all tools must inherit from.
    Provides essential methods for children to override.
    Provides methods for the ToolManager to call for handling opening/closing of settings.

    Variables:
    Must have variable for slider values."""
    tool_image = ObjectProperty(None)
    path = None
    visible = False
    btn = None
    settings = {}
    checkbox = None

    def __init__(self, path):
        """Initialises tool object."""
        super().__init__()
        #Clock.schedule_once(self._finish_init)
        #self.img = Image(self.parent.parent.parent.get_path())
        self.set_path(path)
        #self.add_widget(self.img)

    def _finish_init(self, path):
        #self.img = Image(source=self.ids.filebrowser.get_path())
        #self.img.size_hint = 1, None
        self.set_path(path)

    def add_settings(self):
        """Add all widgets to self here."""
        raise NotImplementedError

    def remove_settings(self):
        """Remove all widgets from self here."""
        raise NotImplementedError

    def open_tool(self):
        """Handless resizing and hiding of UI widgets to expand tool."""
        print("opening")
        self.orientation = 'vertical'
        self.visible = True
        print(self.size_hint)
        print(self.parent.size_hint)
        self.size_hint = (1, 1)
        self.parent.size_hint = (1, 1)
        self.parent.parent.parent.hide_others(self)
        self.add_settings()
        self.ids.tool_image.size_hint_y = 10
        self.btn = Button(text='Back')
        self.btn.bind(on_press=self.close_button_callback)
        self.add_widget(self.btn)

    def close_button_callback(self, event):
        """Event callback function for "close" button click."""
        self.close_tool()

    def close_tool(self):
        """Handles UI widgets for returning back to list view."""
        print("closing")
        self.ids.tool_image.size_hint_y = 1
        self.height = self.parent.parent.parent.tool_height
        self.orientation = 'horizontal'
        self.visible = False
        self.parent.size_hint = (1, None)
        self.size_hint = (1, None)
        self.remove_widget(self.btn)
        self.remove_settings()
        self.parent.parent.parent.show_others(self)

    def toggle(self):
        """Opens or closes tool depending on current state."""
        if self.visible:
            self.close_tool()
        else:
            self.open_tool()

    def set_path(self, path):
        """Updates the UI Image widget to display image from new path."""
        self.path = path
        self.ids.tool_image.source = path

    def set_label(self, name):
        self.ids.lbl.text = name

    def on_touch_down(self, touch):
        """While in list view, when clicked on then open tool."""
        if self.collide_point(touch.x, touch.y) and self.visible == False:
            self.open_tool()
        super(Tool, self).on_touch_down(touch)

    def hide(self):
        """Disables and hides tool."""
        self.size = [0, 0]
        self.opacity = 0
        self.disabled = True

    def show(self):
        """Enables and shows tool."""
        self.height = self.parent.parent.parent.tool_height
        self.opacity = 1
        self.disabled = False

    def flip(self, texture):
        """Flips image y-axis after converting cv2 image to Kivy texture."""
        texture.uvpos = (0, 1)
        texture.uvsize = (1, -1)
        return texture

    def open_remove_checkbox(self):
        self.checkbox = CheckBox(color=[1,0,1,1])
        self.add_widget(self.checkbox)

    def close_remove_checkbox(self):
        self.remove_widget(self.checkbox)

    def zoom(self, height):
        #self.ids.tool_image.height += 20
        self.height = height
