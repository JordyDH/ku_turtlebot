import rclpy
from sensor_msgs.msg import LaserScan
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *

FREQ = 40
NUMREADINGS = 100

class Lidar(Node):
    def __init__(self):
        super().__init__('lidar_publisher')
        self.get_logger().info('Lidar service Starting')
        self.publisher_lidar = self.create_publisher(LaserScan, 'lidar', 10)
        self.subscrib_lidar = self.create_subscription(LaserScan, "/kobuki/laser/scan", self.laser_callback, 10)
        # self.timer = self.create_timer(1/FREQ, self.timer_callback)
    
    def laser_callback(self, msg):
        self.get_logger().info(msg)
        self.publisher_lidar.publish(msg)
        print(msg)
    
    def timer_callback(self):
        self.getReading()

    def getReading(self):
        current_time = self.get_clock().now().to_msg()

        scan = LaserScan()

        scan.header.stamp = current_time
        scan.header.frame_id = 'laser_frame'
        scan.angle_min = -1.57
        scan.angle_max = 1.57
        scan.angle_increment = 3.14 / NUMREADINGS
        scan.time_increment = (1.0 / FREQ) / (NUMREADINGS)
        scan.range_min = 0.0
        scan.range_max = 100.0

        scan.ranges = []
        scan.intensities = []

        self.publisher_lidar.publish(scan)

def main(args=None):
    rclpy.init(args=args)		#Init RCLPY met de argumenten
    lidar_publisher = Lidar()	#Maak een publisher van bovenstaande klasse
    rclpy.spin(lidar_publisher)	#Spin : laat de node actief blijve
    
    lidar_publisher.destroy_node() #Als de node gestopt wordt (garbage collecting)
    rclpy.shutdown()		#Sluit de RCLPY service

if __name__ == '__main__':
    main()
