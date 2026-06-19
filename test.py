import sys
sys.path.append('.')
from core.capture import Camera
from core.pose import PoseEstimator

print('start')
cam = Camera()
print('camera ok')
cam.release()