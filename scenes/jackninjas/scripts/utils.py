import os
import pygame

BASE_IMAGE_PATH = "scenes/jackninjas/data/images/"


# load a single image
def load_image(path):
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


# load all images in a directory
def load_images(path):
    images = []

    for img_name in sorted(
        os.listdir(BASE_IMAGE_PATH + path)
    ):  # sorted is used for OS interoperability
        images.append(load_image(path + "/" + img_name))

    return images


# animation class
class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
