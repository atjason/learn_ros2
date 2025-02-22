import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
from threading import Thread
import time
import espeakng

class NovelSubNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)
        self.novels_queue = Queue()
        self.novel_subscriber = self.create_subscription(String, 'novel', self.novel_callback, 10)
        self.speech_thread = Thread(target=self.speak_callback)
        self.speech_thread.start()

    def novel_callback(self, msg):
        self.novels_queue.put(msg.data)
    
    def speak_callback(self):
        speaker = espeakng.Speaker()
        speaker.voice = 'zh'
        while rclpy.ok:
            if self.novels_queue.qsize() > 0:
                text = self.novels_queue.get()
                self.get_logger().info(f'Reading {text}')
                speaker.say(text)
                speaker.wait()
            else:
                time.sleep(1)
    
def main():
    rclpy.init()
    node = NovelSubNode('novel_read')
    rclpy.spin(node)
    rclpy.shutdown()