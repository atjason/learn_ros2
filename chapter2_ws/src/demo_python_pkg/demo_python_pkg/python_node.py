import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node('python_node')
    node.get_logger().info('Hello Python')
    rclpy.spin(node)
    rclpy.shutdown()