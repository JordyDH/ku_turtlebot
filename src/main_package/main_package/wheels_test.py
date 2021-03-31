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
        super().__init__('Publisher')
        self.publisher_lin = self.create_publisher(Float32, 'wheels_lin', 10)
        self.publisher_ang = self.create_publisher(Float32, 'wheels_ang', 10)
        self.timer = self.create_timer(1/update_rate, self.timer_callback)

    def timer_callback(self):
        intlin=Float32()
        intlin.data=0.1
        intang=Float32()
        intang.data=1.0
        self.publisher_lin.publish(intlin)
        self.publisher_ang.publish(intang)

def main(args=None):
    rclpy.init(args=args)		#Init RCLPY met de argumenten
    demo_publisher = Publisher()	#Maak een publisher van bovenstaande classe
    rclpy.spin(demo_publisher)	#Spin : laat de node actief blijven
    minimal_publisher.destroy_node() #Als de node gestopt wordt (garbage collecting)
    rclpy.shutdown()		#Sluit de RCLPY service

if __name__ == '__main__':
    main()
