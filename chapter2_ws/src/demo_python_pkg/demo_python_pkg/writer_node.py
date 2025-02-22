import rclpy
from demo_python_pkg.person_node import PersonNode

class WriterNode(PersonNode):
    def __init__(self, node_name: str, name: str, age: int, book: str) -> None:
        super().__init__(node_name, name, age)
        self.book = book

    def write(self, time: str):
        self.get_logger().info(f"I'm writing {self.book} at {time}.")

def main():
    rclpy.init()
    node = WriterNode('writer_node', 'Jim', 16, 'How to use ROS2.')
    node.write('11:30')
    rclpy.spin(node)
    rclpy.shutdown()