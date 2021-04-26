from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.core.image import Image as Image
from kivy.properties import ObjectProperty
import cv2
from kivy.uix.relativelayout import RelativeLayout

import matplotlib.pyplot as plt
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
#from kivy.garden.matplotlib.backend_kivy import FigureCanvas

class ColourViewer(GridLayout):
    pass

class ImageViewer(RelativeLayout):
    actual_image = ObjectProperty(None)
    colour_display = ObjectProperty(None)
    path = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #super(ImageViewer, self).__init__(**kwargs)
        self.img = Image('images/color_wheel.png')
        self.img.keep_data = True

        self.img_source = cv2.imread(
            'images/color_wheel.png', cv2.IMREAD_COLOR)

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 1, 0)

            x = self.to_local(*touch.pos)[0]
            y = self.to_local(*touch.pos)[1]

            stretch_factor = self.ids.actual_image.size[1] /self.img.size[1]
            print("Stretch =", stretch_factor)

            real_x = int(x / stretch_factor)
            real_y = int(self.img.size[1] - (y / stretch_factor))
            if self.img.size[1] > real_x >= 0 and real_y < self.img.size[1] and real_y >= 0:
                self.update_colour_display(self.img.read_pixel(int(x / stretch_factor), int(self.img.size[1] - (y / stretch_factor))))

    def update_colour_display(self, new_colour):
        self.parent.parent.parent.colour_display.background_color = new_colour
        #pass

    def similar_colours(self):
        pass

    def colour_chart(self):
        pass

    def set_path(self, path):
        self.path = path
        self.img = Image(path)
        self.img_source = cv2.imread(path, cv2.IMREAD_COLOR)
        self.ids.actual_image.source = path
