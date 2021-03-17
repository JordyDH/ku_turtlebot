import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Publisher(Node):

	def __init__(self):
		super().__init__('demo_publisher')
		self.publisher_ = self.create_publisher(String, 'tick', 10)
		timer_period = 1  # 1 second period
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.i = 0

	def timer_callback(self):
		msg = String()
		msg.data = '[DEMO] tick =  %d' % self.i
		self.publisher_.publish(msg)
		self.get_logger().info("Publishing: '%s'"%msg.data)
		self.i += 1

def main(args=None):
	rclpy.init(args=args)		#Init RCLPY met de argumenten
	demo_publisher = Publisher()	#Maak een publisher van bovenstaande classe
	rclpy.spin(demo_publisher)	#Spin : laat de node actief blijven

	minimal_publisher.destroy_node() #Als de node gestopt wordt (garbage collecting)
	rclpy.shutdown()		#Sluit de RCLPY service

if __name__ == '__main__':
    main()
