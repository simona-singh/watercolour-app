from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.core.image import Image as Image
from kivy.properties import ObjectProperty
import cv2
from kivy.uix.relativelayout import RelativeLayout

class ColourViewer(GridLayout):
    pass

class ImageViewer(RelativeLayout):
    actual_image = ObjectProperty(None)
    colour_display = ObjectProperty(None)

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
            d = 30
            #Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            print("\nDefault =", touch.x, touch.y)  # prints mouse coords
            print("Local =", self.to_local(*touch.pos))

            half_width = self.ids.actual_image.size[0] / 2
            half_height = self.ids.actual_image.size[1] / 2
            height = self.ids.actual_image.size[1]
            print("HEIGHT =",height)
            print("HEIGHT 2 = ", self.img.size[1])
            x = self.to_local(*touch.pos)[0]
            y = self.to_local(*touch.pos)[1]
            print("test =", x, y)
            calc_x = x - half_width
            calc_y = y - half_height
            image_x = self.ids.actual_image.pos[0]
            image_y = self.ids.actual_image.pos[1]
            print("img pos =", self.ids.actual_image.pos)
            print("Calc =", calc_x, ",", calc_y)
            print("Calc2 =", half_width + calc_x, ",", half_height + calc_y)

            print("Colour =", self.img.read_pixel(x, y))
            print(self.img_source[int(x), int(y)])  # prints colour
            rgb = self.img_source[int(x), int(y)]
            colour = []
            for i in range(len(rgb)):
                colour.append(rgb[i] / 255)
            colour.append(1)
            print(colour)
            #self.update_colour_display(colour)#self.img.read_pixel(x, y))

            stretch_factor = self.ids.actual_image.size[1] /self.img.size[1]
            print("Stretch =", stretch_factor)

            self.update_colour_display(self.img.read_pixel(int(x / stretch_factor), int(self.img.size[1] - (y / stretch_factor))))
            #self.update_colour_display(self.img.read_pixel(int(x), int(height - (y))))

            #print("Calc =", touch.pos - self.ids.actual_image.size)

            #print(self.ids.actual_image.ac)
            #print(self.ids.actual_image.norm_image_size)
            #print(self.img_source[int(touch.x), int(touch.y)])  # prints colour
            #print(self.img.read_pixel(touch.x, touch.y))

    def update_colour_display(self, new_colour):
        self.parent.parent.parent.colour_display.background_color = new_colour
        #pass
