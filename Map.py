import time

import Pixel
from Pixel import ScreenPixelManager as spm


class Map(object):
    def __init__(self, name, mmap_rect, geography_list):
        self.name = name
        self.mmap_rect = mmap_rect
        self.geography_list = geography_list
        spm.set_default_rect(mmap_rect)

    def is_player(self, x, y):
        player_pixel_rgb = (225, 225, 136)
        return spm.get_pixel(x, y) == player_pixel_rgb \
                and spm.get_pixel(x+1, y+1) == player_pixel_rgb

    def find_player(self, ref_x=None, ref_y=None):
        if ref_x is None:
            ref_x = self.mmap_rect.x0
        if ref_y is None:
            ref_y = self.mmap_rect.y0
        spm.new_capture()
        for i in range(self.mmap_rect.x0, self.mmap_rect.x1):
            for j in range(self.mmap_rect.y0, self.mmap_rect.y1):
                if self.is_player(i, j):
                    return (i,j)


if __name__ == '__main__':
    # Timer helper-function
    import contextlib

    @contextlib.contextmanager
    def timer(msg):
        start = time.time()
        yield
        end = time.time()
        print("%s: %.02fms" % (msg, (end-start)*1000))

    # Example usage
    m = Map(name="ueii", mmap_rect=Pixel.Rect(0, 0, 138, 175), geography_list=None)

    with timer("Get the current default rect"):
        #print(spm.rect)
        spm.rect

    with timer("Get pixel at (45, 145)"):
        print(spm.get_pixel(45, 145))

    with timer("is player at pixel (45, 145)"):
        print(m.is_player(45, 145))

    #with timer("Find player"):
        #print(m.find_player())
