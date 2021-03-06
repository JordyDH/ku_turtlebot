import RPi.GPIO as GPIO
import time
import rclpy
import cv2 as cv
import numpy as np
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *

BREAKFLAG = 1
BREAKDISTANCE = 5
update = 10
class Sonar(Node):

    def __init__(self):
        super().__init__('sonar_publisher')
        self.get_logger().info('sonar service Starting')
        self.publisher_sonar = self.create_publisher(Int32, 'sonar', 10)
        self.publisher_break = self.create_publisher(Int32, 'break', 10)
        

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._gpio_trigger  = 27
        self._gpio_echo     = 17
        self._range_min     = 10
        self._range_max     = 400
        self._is_reading    = False
        
        self._speed_sound   = 17150.0 #- divided by 2 in cm/s
        
        self._last_time_reading = 0
        self._timeout       = self._range_max/self._speed_sound*2

        

        GPIO.setup(self._gpio_trigger, GPIO.OUT)
        GPIO.setup(self._gpio_echo, GPIO.IN)

        #- Waiting for sensor to settle
        
        GPIO.output(self._gpio_trigger, False)
        
        self.timer = self.create_timer(1/update, self.timer_callback)
        
    def timer_callback(self):
        self.get_logger().info('Timer called ')
        i_32 = Int32()
        i_32.data = self.distance()
        print (i_32.data)
    
        if i_32.data<BREAKDISTANCE: 
            ii_32 = Int32()
            ii_32.data = BREAKFLAG
            self.publisher_break.publish(ii_32)
            self.get_logger().info('Break')
        self.publisher_sonar.publish(i_32)
   
    def distance(self):
        GPIO.output(self._gpio_trigger, True)
        time.sleep(0.00001)
        GPIO.output(self._gpio_trigger, False)
        # save StartTime
        while GPIO.input(self._gpio_echo) == 0:
            StartTime = time.time()
          
    
        # save time of arrival
        while GPIO.input(self._gpio_echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = int ((TimeElapsed * 34300) / 2)
        print (distance)
        return distance

    @property
    def is_reading(self):
        return(self._is_reading)

def main(args=None):
    rclpy.init(args=args)
    PIN_TRIGGER = 5
    PIN_ECHO = 6
    sonar_publisher = Sonar()
    rclpy.spin(sonar_publisher)	#Spin : laat de node actief blijven
    
    sonar_publisher.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()

    
