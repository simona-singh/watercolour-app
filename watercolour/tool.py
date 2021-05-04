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

class ButtonGrid(ButtonBehavior, GridLayout):
    pass

class Tool(BoxLayout):
    tool_image = ObjectProperty(None)
    path = None
    visible = False

    btn = None

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

    def add_settings(self):
        raise NotImplementedError

    def remove_settings(self):
        raise NotImplementedError

    def open_tool(self):
        print("opening")
        self.orientation = 'vertical'
        self.visible = True
        print(self.size_hint)
        print(self.parent.size_hint)
        self.size_hint = (1, 1)
        self.parent.size_hint = (1, 1)
        self.parent.parent.parent.hide_others(self)
        self.btn = Button(text='Back')
        self.btn.bind(on_press=self.close_button_callback)
        self.add_widget(self.btn)
        self.add_settings()
        #self.ids.tool_image.height = 100

    def close_button_callback(self, event):
        self.close_tool()

    def close_tool(self):
        print("closing")
        self.height = 100
        self.orientation = 'horizontal'
        self.visible = False
        self.parent.size_hint = (1, None)
        self.size_hint = (1, None)
        self.remove_widget(self.btn)
        self.remove_settings()
        self.parent.parent.parent.show_others(self)

    def toggle(self):
        if self.visible:
            self.close_tool()
        else:
            self.open_tool()

    def set_path(self, path):
        self.path = path
        self.ids.tool_image.source = path

    def set_label(self, name):
        self.ids.lbl.text = name

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y) and self.visible == False:
            self.open_tool()
        super(Tool, self).on_touch_down(touch)

    def hide(self):
        self.size = [0, 0]
        self.opacity = 0
        self.disabled = True

    def show(self):
        self.height = 100
        self.opacity = 1
        self.disabled = False
