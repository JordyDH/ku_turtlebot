import RPi.GPIO as GPIO
import time
import rclpy
import cv2 as cv
import numpy as np
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *

BREAKFLAG = 1
BREAKDISTANCE = 20
update = 10
class Sonar(Node):

    def __init__(self):
        super().__init__('sonar_publisher')
        self.get_logger().info('sonar service Starting')
        self.publisher_sonar = self.create_publisher(Int32, 'sonar', 10)
        self.publisher_break = self.create_publisher(Int32, 'break', 10)
        

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self._gpio_trigger  = 5
        self._gpio_echo     = 6
        self._range_min     = 10
        self._range_max     = 400
        self._is_reading    = False
        
        self._speed_sound   = 17150.0 #- divided by 2 in cm/s
        
        self._last_time_reading = 0
        self._timeout       = self._range_max/self._speed_sound*2

        

        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.IN)

        #- Waiting for sensor to settle
        GPIO.output(5, GPIO.LOW)
        
        self.timer = self.create_timer(1/update, self.timer_callback)
        
    def timer_callback(self):
		
        afstandgelezen = self.get_range()
        self.get_logger().info(afstandgelezen)

        if afstandgelezen<BREAKDISTANCE: 
            self.publisher_break.publish(BREAKFLAG)
        else:
            self.publisher_sonar.publish(afstandgelezen)
   
        
        

    def get_range(self):
        self._is_reading = True
        #--- Call for a reading
        GPIO.output(self._gpio_trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self._gpio_trigger, GPIO.LOW)
        
        GPIO.output(self._gpio_trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self._gpio_trigger, GPIO.LOW)

        
        pulse_start_time = time.time()
        pulse_end_time = time.time()
        #--- Wait for the answer
        while GPIO.input(self._gpio_echo)==0:
            pulse_start_time = time.time()
            
        time0= time.time()
        while GPIO.input(self._gpio_echo)==1:
            pulse_end_time = time.time()
            
        self._last_time_reading = time.time()
        self._is_reading = False

        pulse_duration = pulse_end_time - pulse_start_time
        distance = pulse_duration * self._speed_sound
        
        if distance > self._range_max:
            distance = self._range_max
            
        if distance < self._range_min:
            distance = self._range_min
            
        return(distance)

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

    
