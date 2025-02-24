import rclpy
from rclpy.node import Node
from chapter4_interfaces.srv import FaceDetector
from sensor_msgs.msg import Image
from ament_index_python.packages import get_package_share_directory
import cv2
from cv_bridge import CvBridge
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

class FaceDetectorClient(Node):
  def __init__(self):
    super().__init__('face_detect_client_node')
    self.client = self.create_client(FaceDetector, '/face_detect') # Service Type, Service Name.
    self.bridge = CvBridge()
    self.test_image_path = get_package_share_directory('demo_python_service') + '/resource/face3.png'
    self.image = cv2.imread(self.test_image_path)
  
  def send_request(self):
    while self.client.wait_for_service(timeout_sec=1.0) is False:
      self.get_logger().info('Wait for service')
    
    request = FaceDetector.Request()
    request.image = self.bridge.cv2_to_imgmsg(self.image)
    
    future = self.client.call_async(request)
    rclpy.spin_until_future_complete(self, future)
    
    response = future.result()
    self.get_logger().info(f'Get response. {response.number} faces, used {response.use_time}s.')
    # self.show_face_locations(response)

  def show_face_locations(self, response):
    for i in range(response.number):
      top = response.top[i]
      right = response.right[i]
      bottom = response.bottom[i]
      left = response.left[i]
      cv2.rectangle(self.image, (left, top), (right, bottom), (255, 0, 0), 2)
    
    cv2.imshow('Face Detection Result', self.image)
    cv2.waitKey(0)
  
  def call_set_parameters(self, parameters):
    update_param_client = self.create_client(SetParameters, '/face_detect_node/set_parameters')
    while not update_param_client.wait_for_service(timeout_sec=1.0):
      self.get_logger().info('Wait for set_parameters service.')
    
    request = SetParameters.Request()
    request.parameters = parameters
    
    future = update_param_client.call_async(request)
    rclpy.spin_until_future_complete(self, future)
    response = future.result()
    return response
  
  def update_detect_model(self, model):
    param = Parameter()
    param.name = 'face_locations_model'
    
    new_model_value = ParameterValue()
    new_model_value.type = ParameterType.PARAMETER_STRING
    new_model_value.string_value = model
    
    response = self.call_set_parameters([param])
    for result in response.results:
      if result.successful:
        self.get_logger().info(f'Set {param.name} to {model}')
      else:
        self.get_logger().info(f'Failed to set param. Reason: {result.reason}')

def main():
  rclpy.init()
  face_detect_client = FaceDetectorClient()
  face_detect_client.get_logger().info('Face Detector Client started.')
  face_detect_client.update_detect_model('hog')
  face_detect_client.send_request()
  face_detect_client.update_detect_model('cnn')
  face_detect_client.send_request()
  rclpy.shutdown()