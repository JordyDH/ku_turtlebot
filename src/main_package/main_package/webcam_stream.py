# DEV : JORDY DE HOON & KARIM HAKO

import rclpy
import cv2 as cv
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *


FPS = 10
# VIDEO_FILE = "data/test.mkv"
VIDEO_FILE = "data/stop _sign.mp4"
class Publisher(Node):

	def __init__(self):
		super().__init__('webcam_fake_publisher')
		self.get_logger().info('Webcam fake service')
		self.publisher_webcam = self.create_publisher(Image, 'webcam', 10)
		self.cam = cv.VideoCapture(VIDEO_FILE)

		self.bridge = CvBridge()
		self.timer = self.create_timer(1/FPS, self.timer_callback)

	def timer_callback(self):
		
		ret ,frame = self.cam.read()
		if (ret):
			print("Frame sended")
			msg = self.bridge.cv2_to_imgmsg(frame, encoding="passthrough")
			self.publisher_webcam.publish(msg)
		else:
			print("nothing to be sended")
			self.cam.set(cv.CAP_PROP_POS_FRAMES, 0)

def main(args=None):
	rclpy.init(args=args)		#Init RCLPY met de argumenten
	webcam_publisher = Publisher()	#Maak een publisher van bovenstaande classe
	rclpy.spin(webcam_publisher)	#Spin : laat de node actief blijven

	webcam_publisher.destroy_node() #Als de node gestopt wordt (garbage collecting)
	rclpy.shutdown()		#Sluit de RCLPY service

if __name__ == '__main__':
    main()
