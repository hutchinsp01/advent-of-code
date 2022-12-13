import cv2


class VideoEncoder:
    def __init__(self, filename, fps, resolution):
        self.filename = filename
        self.fps = fps
        self.resolution = resolution

    def encode_frame(self, size_x, size_y, frame):
        dsize = (size_x, size_y)
        frame = cv2.resize(frame, dsize=dsize, interpolation=cv2.INTER_NEAREST)

        # make image black and white
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
