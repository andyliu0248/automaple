import time
import struct

from scipy.misc import toimage, imsave

import numpy
import Quartz.CoreGraphics as CG


class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """

    def capture(self, region = None):
        """region should be a CGRect, something like:

        >>> import Quartz.CoreGraphics as CG
        >>> region = CG.CGRectMake(0, 0, 100, 100)
        >>> sp = ScreenPixel()
        >>> sp.capture(region=region)

        The default region is CG.CGRectInfinite (captures the full screen)
        """

        if region is None:
            region = CG.CGRectInfinite
        else:
            #region = CG.CGRectMake(rect.x0, rect.y0, rect.width, rect.height)
            # TODO: Odd widths cause the image to warp. This is likely
            # caused by offset calculation in ScreenPixel.query_pixel, and
            # could could modified to allow odd-widths
            if region.size.width % 2 > 0:
                emsg = "Capture region width should be even (was %s)" % (
                    region.size.width)
                raise ValueError(emsg)

        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)

        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(prov)

        # Get width/height of image
        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)

        # Get the time stamp of image
        self.stamp = time.time()

    def get_array(self):
        arr = [[self.query_pixel(i,j) for i in range(self.width)] for j in range(self.height)]
        self.array = numpy.array(arr)

    def to_image(self):
        im = Image.fromarray(self.array.astype('uint8'), 'RGB')
        current_time = time.strftime("%Y-%m%d-%H%M%S")
        im.save(current_time + ".png")
        #im.show()

    def capture_and_save(self, region=None):
        self.capture(region)
        self.get_array()
        self.to_image()

    def query_pixel(self, x, y, alpha=False):
        """Get pixel value at given (x,y) screen coordinates

        Must call capture first.
        """

        #print(self.width, self.height)

        # Pixel data is unsigned char (8bit unsigned integer),
        # and there are for (blue,green,red,alpha)
        data_format = "BBBB"

        # Calculate offset, based on
        # http://www.markj.net/iphone-uiimage-pixel-color/
        offset = 4 * ((self.width*int(round(y))) + int(round(x)))

        # Unpack data from string into Python'y integers
        b, g, r, a = struct.unpack_from(data_format, self._data, offset=offset)

        # Return BGRA as RGBA
        if alpha:
            return (r, g, b, a)
        else:
            return (r, g, b)

class ScreenPixelManager(object):
    capture_list = list()
    rect = None

    def set_default_rect(rect):
        ScreenPixelManager.rect = rect

    def pop_sp():
        if len(ScreenPixelManager.capture_list) == 0:
            raise ValueError("No screen capture yet.")
        return ScreenPixelManager.capture_list[-1]


    def new_capture(rect=None):
        new_sp = ScreenPixel()
        if rect is None:
            try:
                rect = ScreenPixelManager.rect
            except AttributeError:
                rect = Rect(0, 0, 1440, 900)
        new_sp.capture(rect)
        ScreenPixelManager.capture_list.append(new_sp)

    def get_pixel(x, y, new=False, alpha=False):
        if new or len(ScreenPixelManager.capture_list) == 0:
            ScreenPixelManager.new_capture()
        last_capture = ScreenPixelManager.pop_sp()
        return last_capture.query_pixel(x, y, alpha)

    def find_pixel(r, g, b, new=False):
        if new: ScreenPixelManager.new_capture()
        last_sp = ScreenPixelManager.pop_sp()
        for i in range(last_sp.width):
            for j in range(last_sp.height):
                if ScreenPixelManager.get_pixel(i,j) == (r,g,b):
                    return (i,j)
        raise ValueError("Pixel not found.")

class Rect(object):
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.width = x1 - x0
        self.height = y1 - y0

    def __str__(self):
        return str((self.x0, self.y0, self.x1, self.y1))

    def top_right(self):
        return self.x0, self.y0

    def bot_left(self):
        return self.x1, self.y1


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
    sp = ScreenPixel()
    sp.capture()
    sp.get_array()
    sp.to_image()

    with timer("Capture"):
        # Take screenshot (takes about 70ms for me)
        rect = Rect(0, 0, 800, 622)
        sp.capture(rect)

    with timer("Query"):
        # Get pixel value (takes about 0.01ms)
        print(sp.width, sp.height)
        print(sp.query_pixel(0, 0))

    with timer("Ask manager for a new capture"):
        ScreenPixelManager.new_capture(rect)

    with timer("Ask manager for an old pixel"):
        ScreenPixelManager.get_pixel(0, 22)

    with timer("Set default rect to something"):
        ScreenPixelManager.set_default_rect(rect)

    with timer("Get pixel at (45, 145)"):
        print(ScreenPixelManager.get_pixel(45, 145))

    with timer("Get new pixel at (45, 145)"):
        print(ScreenPixelManager.get_pixel(45, 145, new=True))


    with timer("Search for a pixel"):
        ScreenPixelManager.set_default_rect(Rect(0, 0, 138, 178))
        print(ScreenPixelManager.get_pixel(45, 145, new=True))

    rect_2 = Rect(0, 0, 1000, 1000)

    with timer("Search for a pixel"):
        ScreenPixelManager.set_default_rect(rect_2)
        print(ScreenPixelManager.get_pixel(45, 145, new=True))
