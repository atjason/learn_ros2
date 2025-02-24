import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer
from tf_transformations import euler_from_quaternion

class TF2Listener(Node):
  def __init__(self):
    super().__init__('tf2_listener')
    self.buffer = Buffer()
    self.listener = TransformListener(self.buffer, self)
    self.timer = self.create_timer(1, self.get_transform)
    
  def get_transform(self):
    try:
      result = self.buffer.lookup_transform('base_link', 'bottle_link',
                                            rclpy.time.Time(seconds=0),
                                            rclpy.time.Duration(seconds=1))
      transform = result.transform
      rotation_euler = euler_from_quaternion([
        transform.rotation.x,
        transform.rotation.y,
        transform.rotation.z,
        transform.rotation.w,
      ])
      self.get_logger().info(f'A: {transform.translation}, B: {transform.rotation}, C: {rotation_euler}')
    except Exception as e:
      self.get_logger().warn(f'Cannot get transform: {str(e)}')

def main():
  rclpy.init()
  node = TF2Listener()
  rclpy.spin(node)
  rclpy.shutdown()