import rclpy
from rclpy.node import Node
from chapter4_interfaces.srv import FaceDetector
from ament_index_python.packages import get_package_share_directory
from cv_bridge import CvBridge
import cv2
import face_recognition
import time

class FaceDetectNode(Node):
  def __init__(self):
    super().__init__('face_detect_node')
    self.bridge = CvBridge()
    self.service = self.create_service(FaceDetector, '/face_detect', self.detect_face_callback)
    self.default_image_path = get_package_share_directory('demo_python_service') + '/resource/face2.png'
    self.upsample_times = 1
    self.model = 'hog'
  
  def detect_face_callback(self, request, response):
    if request.image.data:
      cv_image = self.bridge.imgmsg_to_cv2(request.image)
    else:
      cv_image = cv2.imread(self.default_image_path)
    
    start_time = time.time()
    self.get_logger().info('Image loaded. Start to detect.')
    face_locations = face_recognition.face_locations(cv_image, number_of_times_to_upsample=self.upsample_times, model=self.model)
    end_time = time.time()
    self.get_logger().info(f'Detect done. Time used: {end_time - start_time}')
    response.number = len(face_locations)
    response.use_time = end_time - start_time
    for top, right, bottom, left in face_locations:
      response.top.append(top)
      response.right.append(right)
      response.bottom.append(bottom)
      response.left.append(left)
    return response

def main():
  rclpy.init()
  node = FaceDetectNode()
  node.get_logger().info('Face detect service started.')
  rclpy.spin(node)
  rclpy.shutdown()
