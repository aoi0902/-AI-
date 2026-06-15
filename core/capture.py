import cv2

class Camera:
    def __init__(self, camera_index=0, width=640, height=480, fps=30, mirror=True):
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.mirror = mirror

        if not self.cap.isOpened():
            raise RuntimeError("カメラが開けません")

    def is_opened(self):
        return self.cap.isOpened()

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False, None
        if self.mirror:
            frame = cv2.flip(frame, 1)
        return True, frame

    def release(self):
        self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.release()

        