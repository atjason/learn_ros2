import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node = Node('python_node')
    node.get_logger().info('Hello Python')
    rclpy.spin(node)
    rclpy.shutdown()

# run via `python3 python_node.py`
if __name__ == "__main__":
    main()