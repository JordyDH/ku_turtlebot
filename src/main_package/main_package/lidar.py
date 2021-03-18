import rclpy
# import rospy
from sensor_msgs.msg import LaserScan
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *

class Lidar(Node):
    def __init__(self):

        super().__init__('lidar_publisher')
        self.get_logger().info('Lidar service Starting')
        self.publisher_lidar = self.create_publisher(String, 'lidar', 10)

def main(args=None):
    rclpy.init(args=args)		#Init RCLPY met de argumenten
    lidar_publisher = Lidar()	#Maak een publisher van bovenstaande klasse
    rclpy.spin(lidar_publisher)	#Spin : laat de node actief blijve
    
    lidar_publisher.destroy_node() #Als de node gestopt wordt (garbage collecting)
    rclpy.shutdown()		#Sluit de RCLPY service

if __name__ == '__main__':
    main()
