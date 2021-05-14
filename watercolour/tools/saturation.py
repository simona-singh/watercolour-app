from watercolour.tool import Tool
from kivy.uix.slider import Slider
from kivy.graphics.texture import Texture
import cv2
import numpy as np


class Saturation(Tool):
    """The Saturation Tool allows users to increase/decrease saturation."""
    saturationValue = 0
    saturationControl = Slider(min=0, max=255, value=0)

    def __init__(self, path):
        super().__init__(path)

    def add_settings(self):
        """Overrides base class to add widgets to self and bind to functions."""
        self.add_widget(self.saturationControl)
        self.saturationControl.bind(value=self.on_saturation)

    def remove_settings(self):
        """"Overrides base class to remove widgets from self."""
        self.remove_widget(self.saturationControl)

    def on_saturation(self, instance, saturation):
        """Handles saturationControl slider."""
        self.saturationValue = saturation
        self.update_photo(self.saturationValue)

    def update_photo(self, saturation):
        """Creates copy of image in cv2.
        Replaces pixels with white/grey/black depending on boundary.
        Converts to texture and replaces image texture."""
        self.img_source = cv2.imread(self.path, cv2.IMREAD_COLOR)
        hsv = cv2.cvtColor(self.img_source, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(hsv)
        print(type(s))
        lim = 255 - saturation
        s[s>lim] = 255
        s[s <= lim] += int(saturation)
        temp = cv2.merge([np.uint8(h), np.uint8(s), np.uint8(v)])

        x = cv2.cvtColor(temp, cv2.COLOR_HSV2BGR)
        w, h, c = x.shape
        texture = Texture.create(size=(h,w))
        texture.uvpos = (0, 1)
        texture.uvsize = (1, -1)
        texture.blit_buffer(x.flatten(), colorfmt='bgr', bufferfmt='ubyte')
        self.ids.tool_image.texture = texture
