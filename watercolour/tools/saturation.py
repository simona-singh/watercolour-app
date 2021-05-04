from watercolour.tool import Tool
from kivy.uix.slider import Slider

class Saturation(Tool):
    saturationValue = 0
    saturationControl = Slider()

    def __init__(self, path):
        super().__init__(path)

    def add_settings(self):
        self.add_widget(self.saturationControl)
        self.saturationControl.bind(value=self.on_saturation)

    def remove_settings(self):
        pass

    def on_saturation(self, instance, saturation):
        self.saturationValue = saturation
        self.update_photo(self.saturationValue)

    def update_photo(self, saturation):
        pass