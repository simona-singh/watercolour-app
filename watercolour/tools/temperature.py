from watercolour.tool import Tool
from kivy.uix.slider import Slider
from kivy.graphics.texture import Texture
import cv2
import numpy as np


class Temperature(Tool):
    coolValue = 1
    coolControl = Slider(min=0, max=255, value=0)
    warmValue = 1
    warmControl = Slider(min=0, max=255, value=0)

    def __init__(self, path):
        super().__init__(path)

    def add_settings(self):
        self.add_widget(self.coolControl)
        self.add_widget(self.warmControl)
        self.coolControl.bind(value=self.on_cool)
        self.warmControl.bind(value=self.on_warm)

    def remove_settings(self):
        self.remove_widget(self.coolControl)
        self.remove_widget(self.warmControl)

    def on_cool(self, instance, cool):
        self.coolValue = cool
        self.update_photo(self.coolValue, self.warmValue)

    def on_warm(self, instance, warm):
        self.warmValue = warm
        self.update_photo(self.coolValue, self.warmValue)

    def update_photo(self, cool, warm):
        self.img_source = cv2.imread(self.path)
        temp = self.img_source.copy()

        #for index, pixel in np.ndenumerate(temp):  # iterate 2D array with index and pixel (array of RGB)
        #    print(index, pixel)
        #    red = pixel[0]
        #    temp.itemset((index[0], index[1], 2), red * self.warmValue)

        """
        pixel_index = 0
        row_index = 0
        for row in temp:  # iterate 2D array with index and pixel (array of RGB)
            for pixel in row:
                red = pixel[0]
                print(pixel_index)
                print(temp.shape)
                #print("pixel", pixel)
                #print("red", red)
                #print("other", temp[pixel_index][0])
                print(temp[row_index, pixel_index])
                temp[row_index, pixel_index, 0] = red * self.warmValue
                #print("last", temp[pixel_index][0])
                #temp.itemset((index[0], index[1], 2), red * self.warmValue)

                pixel_index += 1
            row_index += 1
        """
        for x in range(0, temp.shape[0]):
            for y in range(0, temp.shape[1]):
                red = temp[x, y, 0]
                #print(temp[x,y])
                temp[x, y, 0] = red * self.warmValue

        b, g, r = cv2.split(temp)
        cool_lim = 255 - cool
        warm_lim = 255 - warm
        b[b<=cool_lim] += int(cool)
        r[r<=warm_lim] += int(warm)

        #b = int(cool_lim)
        #temp[np.all(temp == (0, 0, 255), axis=-1)] = (:,:,cool_lim)

        temp = cv2.merge([b,g,r])#[np.uint8(b), np.uint8(g), np.uint8(r)])
        #b[b>cool_lim] = 255
        #b[b <= cool_lim] += int(cool)


        #print("shape = ", temp.shape)
        w, h, c = temp.shape
        texture = Texture.create(size=(h,w))
        self.flip(texture)
        texture.blit_buffer(temp.flatten(), colorfmt='bgr', bufferfmt='ubyte')  # ????
        #w_img = Image(size=(w, h), texture=texture)
        self.ids.tool_image.texture = texture