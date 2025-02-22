import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue

class NovelPubNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.novel_queue = Queue()
        self.novel_publisher = self.create_publisher(String, 'novel', 10)
        self.timer = self.create_timer(5, self.timer_callback)
    
    def download_novel(self, url: str):
        response = requests.get(url)
        response.encoding = 'utf-8'
        self.get_logger().info(f'Downloaded {url}')
        for line in response.text.splitlines():
            self.novel_queue.put(line)
    
    def timer_callback(self):
        if self.novel_queue.qsize() > 0:
            msg = String()
            msg.data = self.novel_queue.get()
            self.novel_publisher.publish(msg)
            self.get_logger().info(f'Publish a line: {msg.data}')

def main():
    rclpy.init()
    node = NovelPubNode('novel_pub_node')
    node.download_novel('https://sh.yigeyi.top/tmp/novel/novel1.txt')
    rclpy.spin(node)
    rclpy.shutdown()