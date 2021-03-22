import rclpy
import numpy as np
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *

class SubsLidar(Node):

    def __init__(self):
        super().__init__('lidar_test')

        self.subscription = self.create_subscription(LaserScan, 'lidar', self.reaction, 10)
        self.subscription
    
    def reaction(self, msg):
        print("Lidar info received")
        print("\t" + str(msg))
    
def main(args=None):
    rclpy.init(args=args)

    subscriber = SubsLidar()

    rclpy.spin(subscriber)

    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
