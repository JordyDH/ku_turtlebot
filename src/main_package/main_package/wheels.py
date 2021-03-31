
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from std_msgs.msg import *

class Subscriber(Node):

    def __init__(self):
        super().__init__('Subscriber')
        self.publisher_twist = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription_lin = self.create_subscription(Float32,'wheels_lin',self.linear_callback,10)
        self.subscription_lin  # prevent unused variable warning
        self.subscription_ang = self.create_subscription(Float32,'wheels_ang',self.angular_callback,10)
        self.subscription_ang
        self.twist_msg = Twist() 

    # called when joy message is received
    def linear_callback(self, msg):
        self.get_logger().info('Linear value change:  "%d"' % msg.data)    
        #int is puur de speed
        self.twist_msg.linear.x = msg.data
        self.publisher_twist.publish(self.twist_msg)

    def angular_callback(self, msg):

        self.get_logger().info('Angular value change:  "%d"' % msg.data)  
        #int is puur de speed
        self.twist_msg.angular.z = msg.data
        self.publisher_twist.publish(self.twist_msg)



def main(args=None):
    print("test main wheels,...")
    rclpy.init(args=args)		#Init RCLPY met de argumenten
    subscriber = Subscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()
    rclpy.shutdown()		#Sluit de RCLPY service







if __name__ == '__main__':
    main()
