from watercolour.tool import Tool
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.graphics.texture import Texture

import cv2

import numpy as np

class ThresholdingValues(Tool):
    """This tool displays a greyscale image separated into three values to represent shadows, mid-tones and highlights.
    Contains 3 sliders:
    highlight - the threshold for pixels to convert to white
    shadow - the threshold for pixels to convert to black
    blur - the amount of blur applied before thresholding to simplify shapes/detail."""
    highlightValue = 200
    shadowValue = 50
    blurValue = 1
    blurControl = Slider(min=1, max=100, value=1)
    highlightControl = Slider(min=1, max=255, value=200)
    shadowControl = Slider(min=1, max=255, value=50)
    blurLabel = Label(text='blur')
    shadowLabel = Label(text='shadow')
    highlightLabel = Label(text='highlight')

    settings = {"highlightValue": highlightValue,
                "shadowValue": shadowValue,
                "blurValue": blurValue}

    def __init__(self, path):
        super().__init__(path)

    def add_settings(self):
        """Overrides base class to add widgets to self."""
        self.ids.lbl.text = 'Values'
        # self.add_widget(self.img)
        self.add_widget(self.highlightLabel)
        self.add_widget(self.highlightControl)
        self.add_widget(self.shadowLabel)
        self.add_widget(self.shadowControl)
        self.add_widget(self.blurLabel)
        self.add_widget(self.blurControl)

        # one label for slider value
        #self.add_widget(Label(text='Slider Value'))
        #self.brightnessValue = Label(text='0')
        #self.add_widget(self.brightnessValue)

        #self.label = Label()
        #self.add_widget(self.label)
        #Window.bind(mouse_pos=self.mouse_pos)

        # On the slider object Attach a callback
        # for the attribute named value
        self.blurControl.bind(value=self.on_blur)
        self.highlightControl.bind(value=self.on_highlight)
        self.shadowControl.bind(value=self.on_shadow) # change to all one function

        self.shadowControl.value = self.settings.get("shadowValue")
        self.blurControl.value = self.settings.get("blurValue")
        self.highlightControl.value = self.settings.get("highlightValue")

    def remove_settings(self):
        """"Overrides base class to remove widgets from self."""
        self.remove_widget(self.highlightControl)
        self.remove_widget(self.shadowControl)
        self.remove_widget(self.blurControl)
        #self.remove_widget(self.brightnessValue)
        self.remove_widget(self.blurLabel)
        self.remove_widget(self.highlightLabel)
        self.remove_widget(self.shadowLabel)

    def update_photo(self, blur, highlight, shadow):
        """Creates copy of image in cv2.
        Replaces pixels with white/grey/black depending on boundary.
        Converts to texture and replaces image texture."""
        self.img_source = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        temp = self.img_source.copy()
        blur = int(blur)
        temp = cv2.blur(temp, (blur, blur))

        temp[np.where((temp >= [highlight]))] = [255]  # change pixels above highlight boundary to white
        temp[np.where((temp <= [shadow]))] = [0]  # change pixels below shadow boundary to black
        temp[np.where((temp < highlight) & (temp > shadow))] = [100]  # change remaining pixels to grey

        #print(temp.shape)
        w, h = temp.shape
        texture = Texture.create(size=(h,w))
        self.flip(texture)
        texture.blit_buffer(temp.flatten(), colorfmt='luminance', bufferfmt='ubyte')  # ????
        #w_img = Image(size=(w, h), texture=texture)
        self.ids.tool_image.texture = texture

    # i.e when pressed increase the value
    def on_blur(self, instance, blur):
        """Handles blurControl slider."""
        #print("blurb")
        #self.brightnessValue.text = "% d" % blur
        self.blurValue = blur
        self.update_photo(self.blurValue, self.highlightValue, self.shadowValue)

    def on_highlight(self, instance, highlight):
        """Handles highlightControl slider."""
        self.highlightValue = highlight
        self.update_photo(self.blurValue, self.highlightValue, self.shadowValue)

    def on_shadow(self, instance, shadow):
        """Handles shadowControl slider."""
        self.shadowValue = shadow
        self.update_photo(self.blurValue, self.highlightValue, self.shadowValue)
    # The app class

    def mouse_pos(self, window, pos):
        self.label.text = "Mouse coords = " + str(pos)

    def get_settings(self):
        """Updates settings array and returns it for FileBrowser to save session."""
        self.settings["highlightValue"] = self.highlightValue
        self.settings["shadowValue"] = self.shadowValue
        self.settings["blurValue"] = self.blurValue
        return self.settings
