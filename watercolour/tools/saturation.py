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
        self.add_widget(self.saturationControl)
        self.saturationControl.bind(value=self.on_saturation)

    def remove_settings(self):
        self.remove_widget(self.saturationControl)

    def on_saturation(self, instance, saturation):
        self.saturationValue = saturation
        self.update_photo(self.saturationValue)

    def update_photo(self, saturation):
        self.img_source = cv2.imread(self.path, cv2.IMREAD_COLOR)#.astype(np.float32) / 255.0
        #temp = self.img_source.copy()
        hsv = cv2.cvtColor(self.img_source, cv2.COLOR_BGR2HSV)

        #hsv[:, :, 2] = (1.0 + saturation / float(self.saturationControl.max)) * hsv[:, :, 2]
        #hsv[:, :, 2][hsv[:, :, 2] > 1] = 1

        #H, S, V = cv2.split(hsv)
        #temp = cv2.merge([np.uint8(H), np.uint8(S*saturation), np.uint8(V)])

        #temp = hsv*saturation

        #for row in hsv:
        #    for pixel in hsv:
        #        #print(pixel)
        #        hsv[row,pixel,1] = saturation * hsv[row,pixel,1]

        #print(temp.shape)


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
        texture.blit_buffer(x.flatten(), colorfmt='bgr', bufferfmt='ubyte')  # ????
        #w_img = Image(size=(w, h), texture=texture)
        self.ids.tool_image.texture = texture