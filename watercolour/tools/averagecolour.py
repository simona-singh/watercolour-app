from watercolour.tool import Tool
from kivy.uix.slider import Slider
from kivy.graphics.texture import Texture
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans

class AverageColour(Tool):
    clusterValue = 1
    clusterControl = Slider(min=1, max=10, value=1)

    def __init__(self, path):
        super().__init__(path)

    def add_settings(self):
        self.add_widget(self.clusterControl)
        self.clusterControl.bind(value=self.on_cluster)

    def remove_settings(self):
        self.remove_widget(self.clusterControl)

    def on_cluster(self, instance, cluster):
        self.clusterValue = cluster
        self.update_photo(self.clusterValue)

    def update_photo(self, cluster):
        self.img_source = cv2.imread(self.path)
        temp = self.img_source.copy()
        (h, w) = temp.shape[:2]
        image = cv2.cvtColor(temp, cv2.COLOR_BGR2LAB)
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        clt = MiniBatchKMeans(n_clusters=int(cluster))
        labels = clt.fit_predict(image)
        quant = clt.cluster_centers_.astype("uint8")[labels]
        quant = quant.reshape((h, w, 3))
        quant = cv2.cvtColor(quant, cv2.COLOR_LAB2RGB)

        w, h, c = quant.shape
        texture = Texture.create(size=(h,w))
        self.flip(texture)
        texture.blit_buffer(quant.flatten(), colorfmt='rgb', bufferfmt='ubyte')  # ????
        #w_img = Image(size=(w, h), texture=texture)
        self.ids.tool_image.texture = texture