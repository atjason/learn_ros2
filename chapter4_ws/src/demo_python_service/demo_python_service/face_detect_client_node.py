import rclpy
from rclpy.node import Node
from chapter4_interfaces.srv import FaceDetector
from sensor_msgs.msg import Image
from ament_index_python.packages import get_package_share_directory
import cv2
from cv_bridge import CvBridge

class FaceDetectorClient(Node):
  def __init__(self):
    super().__init__('face_detect_client_node')
    self.client = self.create_client(FaceDetector, '/face_detect_client')
    self.bridge = CvBridge()
    self.test_image_path = get_package_share_directory('demo_python_service') + '/resouce/face2.png'
    self.image = cv2.imread(self.test_image_path)
  
  def send_request(self):
    while self.client.wait_for_service(timeout_sec=1.0) is False:
      self.get_logger().info('Wait for service')
    
    request = FaceDetector.Request()
    request.image = self.bridge.cv2_to_imgmsg(self.image)
    
    future = self.client.call_async(request)
    rclpy.spin_until_futuren_complete(self, future)
    
    response = future.result()
    self.get_logger().info(f'Get response. {response.number} faces, used {response.use_time}s.')
    self.show_face_locations(response)

  def show_face_locations(self, response):
    for i in range(response.number):
      top = response[i]
      right = response[i]
      bottom = response[i]
      left = response[i]
      cv2.rectangle(self.image, (left, top), (right, botto), (255, 0, 0), 2)
      cv2.imshow('Face Detection Result', self.image)
      cv2.waitKey(0)

def main():
  rclpy.init()
  node.get_logger().info('Face Detector Client started.')
  face_detect_client = FaceDetectorClient()
  face_detect_client.send_request()
  rclpy.shutdown()