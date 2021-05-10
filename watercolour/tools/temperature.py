from scipy.interpolate import UnivariateSpline

from watercolour.tool import Tool
from kivy.uix.slider import Slider
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import ast
from color_temp import temperature_to_rgb

class Temperature(Tool):
    coolValue = 1
    coolControl = Slider(min=35, max=65, value=50)
    kelvin = {}
    lookup = []
    lookuptable = []

    def __init__(self, path):
        super().__init__(path)

    def spreadLookupTable(self, x, y):
        spline = UnivariateSpline(x, y)
        return spline(range(256))

    def add_settings(self):
        self.add_widget(self.coolControl)
        self.coolControl.bind(value=self.on_cool)

    def remove_settings(self):
        self.remove_widget(self.coolControl)

    def on_cool(self, instance, cool):
        self.coolValue = cool
        self.update_photo(self.coolValue)

    # slider should be a number from 0 - 100
    def adjustTemps(self, slider):
        default_temps = [0, 64, 128, 256]
        factor = slider / 50
        new_temps = [min(int(i * factor), 256) for i in default_temps]
        new_temps[len(new_temps) - 1] = 256
        print(slider, new_temps)
        return new_temps

    def update_photo(self, temperature):
        self.img_source = cv2.imread(self.path)
        other = self.img_source.copy()

        increaseLookupTable = self.spreadLookupTable([0, 64, 128, 256], self.adjustTemps(temperature))
        decreaseLookupTable = self.spreadLookupTable([0, 64, 128, 256], self.adjustTemps(100 - temperature))


        blue_channel, green_channel, red_channel = cv2.split(other)
        red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
        blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
        #temp = cv2.merge((red_channel, green_channel, blue_channel))
        temp = cv2.merge((blue_channel, green_channel, red_channel))

        w, h, c = temp.shape
        texture = Texture.create(size=(h,w))
        self.flip(texture)
        texture.blit_buffer(temp.flatten(), colorfmt='bgr', bufferfmt='ubyte')  # ????
        #w_img = Image(size=(w, h), texture=texture)
        self.ids.tool_image.texture = texture