import rclpy
import cv2 as cv
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *

class Subscriber(Node):

	def __init__(self):
		super().__init__('webcam_test')
		self.bridge = CvBridge()
		self.subscription = self.create_subscription(Image,'webcam',self.listener_callback,10)
		self.subscription  # prevent unused variable warning

	def listener_callback(self, msg):
		print("FRAME received")
		frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
		cv.imshow("video",frame)
		key = cv.waitKey(1)


def main(args=None):
	rclpy.init(args=args)
	subscriber = Subscriber()
	rclpy.spin(subscriber)
	subscriber.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
