import time
import struct

import Quartz.CoreGraphics as CG


DEFAULT_REGION = CG.CGRectMake(0, 0, 800, 622)

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

    def query_pixel(self, x, y, alpha=False):
        """Get pixel value at given (x,y) screen coordinates

        Must call capture first.
        """

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


class ScreenPixelStamped(object):
    def __init__(self, region=None):
        self.stamp = time.time()
        self.sp = ScreenPixel()
        self.sp.capture(region)

    def get_stamp(self):
        return self.stamp

    def get_sreen_pixel_object(self):
        return self.sp

    def get_pixel(self, x, y, alpha=False):
        return self.sp.query_pixel(x, y, alpha)



class ScreenPixelManager(object):

    def __init__(self, default_region=None):
        # A list storeing ScreenPixelStamped objects
        self.captured_list = list()
        self.default_region = default_region

    def new_capture(self, region=None):
        if region is None:
            region = self.default_region
        new_sp = ScreenPixelStamped(region)
        self.captured_list.append(new_sp)

    def get_pixel(self, x, y, new=False, alpha=False):
        if new or len(self.captured_list) == 0:
            self.new_capture()
        latest_capture = self.captured_list[-1]
        return latest_capture.get_pixel(x, y, alpha)


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
        region=CG.CGRectMake(0, 22, 800, 600)
        sp.capture(region=region)

    with timer("Query"):
        # Get pixel value (takes about 0.01ms)
        print(sp.width, sp.height)
        print(sp.query_pixel(0, 0))

    with timer("New time-stamped capture"):
        stamped = ScreenPixelStamped()

    with timer("New manager"):
        manager = ScreenPixelManager()

    with timer("Ask manager for a new capture"):
        manager.new_capture()

    with timer("Ask manager for an old pixel"):
        manager.get_pixel(0, 22)

    with timer("Ask manager for a new pixel"):
        manager.get_pixel(0, 22, new=True)
