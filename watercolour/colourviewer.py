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
    chart = None
    colour = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #super(ImageViewer, self).__init__(**kwargs)
        self.img = Image('images/color_wheel.png')
        self.img.keep_data = True

        self.img_source = cv2.imread(
            'images/color_wheel.png', cv2.IMREAD_COLOR)

    #def set_image(self):

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
            if self.collide_point(touch.x, touch.y):
                self.update_colour_display(self.img.read_pixel(int(x / stretch_factor), int(self.img.size[1] - (y / stretch_factor))))

    def update_colour_display(self, new_colour):
        print("new colour =", new_colour)
        self.parent.parent.parent.colour_display.background_color = new_colour
        self.colour = new_colour.copy()
        #pass

    def similar_colours(self):
        """Convert to cv2 to use numpy"""
        grey = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
        grey = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)
        reference = cv2.imread(self.path, cv2.IMREAD_COLOR)
        hsv = cv2.cvtColor(reference, cv2.COLOR_BGR2HSV)

        #https://stackoverflow.com/questions/63498826/opencv-python-how-to-keep-one-color-as-is-converting-an-image-to-grayscale
        #ret, mask = cv2.threshold(reference[:, :, 0], 100, 255, cv2.THRESH_BINARY)

        bgr_colour = self.colour.copy() #self.parent.parent.parent.colour_display.background_color
        #print(colour) # convert to BGR
        for c in range(0,3):
            bgr_colour[c] *= 255
            bgr_colour[c] = int(bgr_colour[c])
        print(bgr_colour)
        #del bgr_colour[-1]
        print(bgr_colour)

        hsv_colour = np.uint8([[bgr_colour]])
        print(hsv_colour)
        hsv_colour = cv2.cvtColor(hsv_colour, cv2.COLOR_RGB2HSV)

        print("hsv)colour =", hsv_colour)

        lower_bound = np.array(hsv_colour[0, 0, 0]) - 10 # get hue from hsv
        upper_bound = np.array(hsv_colour[0, 0, 0]) + 10

        print(lower_bound)
        print(upper_bound)
        #hsv_upper = cv2.cvtColor(hsv_upper, cv2.COL)
        print(grey.shape)

        hue = hsv[:,:,0]
        print(hue)
        area = np.where((hue < lower_bound) | (hue > upper_bound))
        print(area[0])
        reference[area[0], area[1], :] = [0,0,0] #bgr_colour
        out = cv2.cvtColor(grey, cv2.COLOR_HSV2BGR)
        out[area] = reference[area]

        out = reference
        out[area] = grey[area]

        w, h, c = out.shape
        texture = Texture.create(size=(h,w))
        texture.uvpos = (0, 1)
        texture.uvsize = (1, -1)
        texture.blit_buffer(out.flatten(), colorfmt='bgr', bufferfmt='ubyte')  # ????
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

        self.chart = FigureCanvasKivyAgg(plt.gcf())

        self.parent.parent.parent.panel.add_widget(self.chart)

    def remove_chart(self):
        if self.chart is not None:
            self.parent.parent.parent.panel.remove_widget(self.chart)

    def set_path(self, path):
        self.path = path
        self.img = Image(path)
        self.img_source = cv2.imread(path, cv2.IMREAD_COLOR)
        self.ids.actual_image.source = path
