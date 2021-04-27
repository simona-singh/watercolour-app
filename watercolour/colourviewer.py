from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.core.image import Image as Image
from kivy.properties import ObjectProperty
import cv2
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.texture import Texture
import numpy as np
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
#from kivy.garden.matplotlib.backend_kivy import FigureCanvas
from kivy_garden.graph import Graph
#from kivy.garden import Graph
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivyagg')

class ColourViewer(GridLayout):
    pass

class ImageViewer(RelativeLayout):
    actual_image = ObjectProperty(None)
    colour_display = ObjectProperty(None)
    path = None
    last_x, last_y = 0, 0
    panel = ObjectProperty(None)

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
            self.last_x, self.last_y = real_x, real_y
            if self.img.size[1] > real_x >= 0 and real_y < self.img.size[1] and real_y >= 0:
                self.update_colour_display(self.img.read_pixel(int(x / stretch_factor), int(self.img.size[1] - (y / stretch_factor))))

    def update_colour_display(self, new_colour):
        self.parent.parent.parent.colour_display.background_color = new_colour
        #pass

    def similar_colours(self):
        """Convert to cv2 to use numpy"""
        display = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        reference = cv2.imread(self.path, cv2.IMREAD_COLOR)

        #display[np.where((reference >= 200))] = [255]  # change pixels above highlight boundary to white
        #temp[np.where((temp <= [shadow]))] = [0]  # change pixels below shadow boundary to black
        #temp[np.where((temp < highlight) & (temp > shadow))] = [100]  # change remaining pixels to grey


        w, h = display.shape
        texture = Texture.create(size=(h,w))
        texture.blit_buffer(display.flatten(), colorfmt='luminance', bufferfmt='ubyte')  # ????
        #w_img = Image(size=(w, h), texture=texture)
        self.ids.actual_image.texture = texture


    def colour_chart(self):
        reference = cv2.imread(self.path, cv2.IMREAD_COLOR)#[:, :, :-1]
        pixels = np.float32(reference.reshape(-1, 3))

        n_colors = 6
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]

        indices = np.argsort(counts)[::-1]
        freqs = np.cumsum(np.hstack([[0], counts[indices] / float(counts.sum())]))
        rows = np.int_(reference.shape[0] * freqs)

        dom_patch = np.zeros(shape=reference.shape, dtype=np.uint8)
        for i in range(len(rows) - 1):
            dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(np.flip(palette[indices[i]]))

        print(type(dom_patch))
        print(dom_patch)

        fig, ax = plt.subplots()
        ax.imshow(dom_patch)
        ax.axis('off')

        chart = FigureCanvasKivyAgg(plt.gcf())

        self.parent.parent.parent.panel.add_widget(chart)

    def set_path(self, path):
        self.path = path
        self.img = Image(path)
        self.img_source = cv2.imread(path, cv2.IMREAD_COLOR)
        self.ids.actual_image.source = path
