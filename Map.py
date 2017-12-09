import time

import Pixel
from Pixel import ScreenPixelManager as spm


class Map(object):
    def __init__(self, name, mmap_rect=None, geography_list=None):
        self.name = name
        if mmap_rect is None:
            self.mmap_rect = Pixel.Rect(0,0,300,300)
        else:
            self.mmap_rect = mmap_rect
        spm.set_default_rect(self.mmap_rect)

        self.geography_list = geography_list
        self.previous_pos = None

    def is_player(self, i, j):
        player_rgp = (255, 255, 136)
        try:
            return spm.get_pixel(i, j) == player_rgp and \
                spm.get_pixel(i+1, j+1) == player_rgp
        except IndexError:
            return False

    def find_player_rect(self, rect):
        for i in range(rect.x0, rect.x1):
            for j in range(rect.y0, rect.y1):
                if self.is_player(i, j):
                    return (i,j)
        raise PlayerNotFound("Player not found.")

    def record_map(self, sec, sleep_sec=0.2, search_radius=15):
        attempts = int(sec / sleep_sec)
        x_min, x_max, y_min, y_max = 1e6, -1, 1e6, -1
        print("Search for player for %d times" % (attempts))
        for i in range(attempts):
            with timer("Attempt #%d:" % (i)):
                spm.new_capture()
                pos = self.find_player()
                print(pos)
            x_min, y_min = min(x_min, pos[0]), min(y_min, pos[1])
            x_max, y_max = max(x_max, pos[0]), max(y_max, pos[1])
            #print(pos, (x_min, y_min), (x_max, y_max))
            time.sleep(sleep_sec)
        self.mmap_rect = Pixel.Rect(x_min, y_min, x_max, y_max)
        print(self.mmap_rect)


    def find_player(self, search_radius=15):
        spm.new_capture()
        if self.previous_pos is not None:
            print("Search the vicinity of previous position.")
            search_rect = Pixel.Rect(max(self.mmap_rect.x0, self.previous_pos[0] - search_radius), \
                               max(self.mmap_rect.y0, self.previous_pos[1] - search_radius), \
                               min(self.mmap_rect.x1, self.previous_pos[0] + search_radius), \
                               min(self.mmap_rect.y1, self.previous_pos[1] + search_radius))
            try:
                pos =  self.find_player_rect(search_rect)
                self.previous_pos = pos
                return pos
            except PlayerNotFound as e:
                print("Player not found in vicinity.")
                pass
        try:
            print("Comprehensive search.")
            pos =  self.find_player_rect(self.mmap_rect)
            self.previous_pos = pos
            return pos
        except PlayerNotFound as e:
            print("Player not found in the current mmap.")
            raise PlayerNotFound("Player not found.")



class PlayerNotFound(Exception):
    def __init__(self, rect):
        self.rect = rect
    def __str__(self):
        return str(self.rect)



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
    m = Map(name="ueii",mmap_rect=Rect(10, 106, 132, 154))
    #spm.set_default_rect(Rect(5, 115, 136, 158))

    with timer("Get the current default rect"):
        #print(spm.rect)
        spm.rect

    with timer("Get the current default rect"):
        #print(spm.rect)
        m.find_player()

    m.record_map(60)
