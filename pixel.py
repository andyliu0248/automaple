import time
import struct

import Quartz.CoreGraphics as CG


class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """

    def capture(self, rect = None):
        """region should be a CGRect, something like:

        >>> import Quartz.CoreGraphics as CG
        >>> region = CG.CGRectMake(0, 0, 100, 100)
        >>> sp = ScreenPixel()
        >>> sp.capture(region=region)

        The default region is CG.CGRectInfinite (captures the full screen)
        """

        if rect is None:
            region = CG.CGRectInfinite
        else:
            region = CG.CGRectMake(rect.x0, rect.y0, rect.width, rect.height)
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

    def query_pixel(self, x, y, alpha=False):
        """Get pixel value at given (x,y) screen coordinates

        Must call capture first.
        """

        print(self.width, self.height)

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
    the_manager = None

    def pop_manager():
        the_manager = ScreenPixelManager.the_manager
        if the_manager is None:
            the_manager = ScreenPixelManager()
            the_manager.capture_list = list()
        return the_manager

    def set_default_rect(self, rect):
        self.rect = rect

    def pop_sp(self):
        if len(self.capture_list) == 0:
            raise ValueError("No screen capture yet.")
        return self.capture_list[-1]


    def new_capture(self, rect=None):
        new_sp = ScreenPixel()
        if rect is None:
            try:
                rect = self.rect
            except AttributeError:
                rect = Rect(0, 0, 1440, 900)
        new_sp.capture(rect)
        self.capture_list.append(new_sp)

    def get_pixel(self, x, y, new=False, alpha=False):
        if new or len(self.capture_list) == 0:
            self.new_capture()
        last_capture = self.pop_sp()
        return last_capture.query_pixel(x, y, alpha)

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

    with timer("Capture"):
        # Take screenshot (takes about 70ms for me)
        rect = Rect(0, 0, 800, 622)
        sp.capture(rect)

    with timer("Query"):
        # Get pixel value (takes about 0.01ms)
        print(sp.width, sp.height)
        print(sp.query_pixel(0, 0))

    with timer("New manager"):
        manager = ScreenPixelManager.pop_manager()

    with timer("Ask manager for a new capture"):
        manager.new_capture(rect)

    with timer("Ask manager for an old pixel"):
        manager.get_pixel(0, 22)

    with timer("Set default rect to something"):
        manager.set_default_rect(rect)

    with timer("Get pixel at (73, 116)"):
        print(manager.get_pixel(73, 116))
