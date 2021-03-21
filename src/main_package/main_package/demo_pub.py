# DEV  : <PLACE HERE YOUR NAMES>
# DATE : <DATE OF CREATION>
# DESCRIPTION :  

import rclpy
from rclpy.node import Node
from std_msgs.msg import *

#NODE GLOBAL SETTINGS
update_rate	= 1
node_name 	= "DEMO_NODE"

# MAKE SURE THE CLASS INHERITS FROM NODE CLASS
class Publisher(Node):
	def __init__(self):
		super().__init__('demo_publisher')
		self.publisher_string = self.create_publisher(String, 'test_string', 10)
		self.publisher_int32 = self.create_publisher(Int32, 'test_int32', 10)
		self.timer = self.create_timer(1/update_rate, self.timer_callback)
		self.i = 0

	def timer_callback(self):
		msg = String()
		msg.data = 'You alive? %d' % self.i
		i_32 = Int32()
		i_32.data = self.i
		self.publisher_string.publish(msg)
		self.publisher_int32.publish(i_32)
		self.i += 1

def main(args=None):
	rclpy.init(args=args)		#Init RCLPY met de argumenten
	demo_publisher = Publisher()	#Maak een publisher van bovenstaande classe
	rclpy.spin(demo_publisher)	#Spin : laat de node actief blijven

	minimal_publisher.destroy_node() #Als de node gestopt wordt (garbage collecting)
	rclpy.shutdown()		#Sluit de RCLPY service

if __name__ == '__main__':
    main()

