import rclpy
from rclpy.node import Node

def PersonNode(Node):
    def __init__(self, node_name: str, name: str, age: int) -> None:
        super.__init__(node_name)
        self.name = name
        self.age = age
    
    def eat(self, food_name: str):
        self.get_logger().info(f"I'm {self.name}, {self.age} years old. Now I'm eating {food_name}.")

def main():
    rclpy.init()
    node = PersonNode('person_node', 'Tom', 18)
    rclpy.eat('fish')
    rclpy.spin(node)
    rclpy.shutdown()