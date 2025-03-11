import math
import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler

class StaticTFBoradcaster(Node):
  def __init__(self):
    super().__init__('static_tf2_broadcaster')
    self.static_broadcaster = StaticTransformBroadcaster(self)
    self.publish_static_tf()
  
  def publish_static_tf(self):
    transform = TransformStamped()
    transform.header.stamp = self.get_clock().now().to_msg()
    transform.header.frame_id = "base_link"
    transform.child_frame_id = "camera_link"
    
    transform.transform.translation.x = 0.5
    transform.transform.translation.y = 0.3
    transform.transform.translation.z = 0.6
    
    rotation_quat = quaternion_from_euler(math.radians(180), 0, 0)
    transform.transform.rotation.x = rotation_quat[0]
    transform.transform.rotation.y = rotation_quat[1]
    transform.transform.rotation.z = rotation_quat[2]
    transform.transform.rotation.w = rotation_quat[3]
    
    self.static_broadcaster.sendTransform(transform)
    self.get_logger().info(f'Publish TF: {transform}')

def main():
  rclpy.init()
  node = StaticTFBoradcaster()
  rclpy.spin(node)
  rclpy.shutdown()