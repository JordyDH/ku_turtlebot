# DEV  : <PLACE HERE YOUR NAME>
# DATE : <DATE OF CREATION>
# DESCRIPTION : 

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Subscriber(Node):
    def __init__(self):
        super().__init__('Subscriber')
        self.subscription = self.create_subscription(String,'test_string',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('STRING: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    subscriber = Subscriber()

    rclpy.spin(subscriber)

    subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
