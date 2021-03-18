#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import rclpy
import cv2 as cv
import numpy as np
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *

class Sonar():

    def __init__(self, gpio_trigger, gpio_echo, range_min=10, range_max=400):
        super().__init__('sonar_publisher')
        self.get_logger().info('sonar service Starting')
        self.publisher_webcam = self.create_publisher(Int32, 'sonar', 10)
        
        GPIO.setmode(GPIO.BCM)
        self._gpio_trigger  = gpio_trigger
        self._gpio_echo     = gpio_echo
        self._range_min     = range_min
        self._range_max     = range_max
        self._is_reading    = False
        
        self._speed_sound   = 17150.0 #- divided by 2 in cm/s
        
        self._last_time_reading = 0
        self._timeout       = range_max/self._speed_sound*2

        GPIO.setup(gpio_trigger, GPIO.OUT)
        GPIO.setup(gpio_echo, GPIO.IN)

        #- Waiting for sensor to settle
        GPIO.output(gpio_trigger, GPIO.LOW)
        
        self.timer = self.create_timer(1/FPS, self.timer_callback)
        time.sleep(1)
    def timer_callback(self):
        _,frame = self.cam.read()
        msg = self.bridge.cv2_to_imgmsg(frame, encoding="passthrough")
        self.publisher_webcam.publish(msg)
        
        

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
    sonar_publisher = Sonar()
    PIN_TRIGGER = 5
    PIN_ECHO = 6


    sonar = Sonar(PIN_TRIGGER, PIN_ECHO)
    rclpy.spin(sonar_publisher)	#Spin : laat de node actief blijven
    
    while True:
        d = sonar.get_range()
        if d>0: print ("Distance = %5.1f cm"%d)
    sonar_publisher.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()

    
