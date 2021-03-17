import rclpy
import cv2 as cv
from rclpy.node import Node
from std_msgs.msg import *

print(cv.__version__)
FPS = 30

class Publisher(Node):

	def __init__(self):
		super().__init__('webcam_publisher')
		self.get_logger().info('Webcam service Starting')
		self.publisher_webcam = self.create_publisher(Int32, 'webcam', 10)
		self.timer = self.create_timer(1/FPS, self.timer_callback)

	def timer_callback(self):
		frame = Int32()
		frame.data = 0
		self.publisher_webcam.publish(frame)
		self.get_logger().info('Webcam service running')

def main(args=None):
	rclpy.init(args=args)		#Init RCLPY met de argumenten
	webcam_publisher = Publisher()	#Maak een publisher van bovenstaande classe
	rclpy.spin(webcam_publisher)	#Spin : laat de node actief blijven

	webcam_publisher.destroy_node() #Als de node gestopt wordt (garbage collecting)
	rclpy.shutdown()		#Sluit de RCLPY service

if __name__ == '__main__':
    main()
