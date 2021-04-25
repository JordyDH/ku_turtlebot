import cv2
import numpy as np
from scipy.stats import itemfreq
import rclpy
import cv2 as cv
import numpy as np
from cv_bridge import CvBridge
from rclpy.node import Node
from std_msgs.msg import *
from sensor_msgs.msg import *
FPS = 10



class traffic_sign_detection(Node):
    
    def __init__(self):
        super().__init__('detection_visualizer')
        self.get_logger().info('detection service')
        
        #subscription
        self.subscription = self.create_subscription(Image,'webcam',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

        #publisher
        self.publisher_traffic_sign= self.create_publisher(Image, 'webcam_det', 10)

        self.bridge = CvBridge()

    def listener_callback(self, msg):
    
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(gray, 37)
        #return the center coordinates and the radius of the circles
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,
                                1, 50, param1=120, param2=40)

        if not circles is None:
            circles = np.uint16(np.around(circles))
            max_r, max_i = 0, 0
            for i in range(len(circles[:, :, 2][0])):
                #choose the bigest circle 
                if circles[:, :, 2][0][i] > 50 and circles[:, :, 2][0][i] > max_r:
                    max_i = i
                    max_r = circles[:, :, 2][0][i]
            x, y, r = circles[:, :, :][0][max_i]
            if y > r and x > r:
                #extract the pixels inside the circle
                square = cv_image[y-r:y+r, x-r:x+r] 
                
                #K-mean for two clusters
                dominant_color = self.get_dominant_color(square, 2)
                #check the red color
                if dominant_color[2] > 50:
                    print("STOP")
                    cv2.putText(cv_image, "STOP",(120,35), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2, cv2.LINE_AA)
                #check the blue color
                elif dominant_color[0] > 80:
                    zone_0 = square[square.shape[0]*3//8:square.shape[0]
                                    * 5//8, square.shape[1]*1//8:square.shape[1]*3//8]
                    cv2.imshow('Zone0', zone_0)
                    zone_0_color = self.get_dominant_color(zone_0, 1)

                    zone_1 = square[square.shape[0]*1//8:square.shape[0]
                                    * 3//8, square.shape[1]*3//8:square.shape[1]*5//8]
                    cv2.imshow('Zone1', zone_1)
                    zone_1_color = self.get_dominant_color(zone_1, 1)

                    zone_2 = square[square.shape[0]*3//8:square.shape[0]
                                    * 5//8, square.shape[1]*5//8:square.shape[1]*7//8]
                    cv2.imshow('Zone2', zone_2)
                    zone_2_color = self.get_dominant_color(zone_2, 1)
                    

                    if zone_1_color[2] < 60:
                        if sum(zone_0_color) > sum(zone_2_color):
                            print("LEFT")
                            cv2.putText(cv_image, "LEFT",(120,35), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2, cv2.LINE_AA)

                        else:
                            print("RIGHT")
                            cv2.putText(cv_image, "RIGHT",(120,35), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2, cv2.LINE_AA)

                    else:
                        if sum(zone_1_color) > sum(zone_0_color) and sum(zone_1_color) > sum(zone_2_color):
                            print("FORWARD")
                            cv2.putText(cv_image, "FORWARD",(120,35), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2, cv2.LINE_AA)

                        elif sum(zone_0_color) > sum(zone_2_color):
                            print("FORWARD ")
                            cv2.putText(cv_image, "FORWARD",(120,35), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2, cv2.LINE_AA)

                        else:
                            print("FORWARD ")
                            cv2.putText(cv_image, "FORWARD",(120,35), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2, cv2.LINE_AA)

                else:
                    cv2.putText(cv_image, "NOTIHNIG",(120,35), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,255),2, cv2.LINE_AA)
                    print("N/A")

            for i in circles[0, :]:
                cv2.circle(cv_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(cv_image, (i[0], i[1]), 2, (0, 0, 255), 3)
        
        msg_to_webcam_test = self.bridge.cv2_to_imgmsg(cv_image, encoding="passthrough")
        self.publisher_traffic_sign.publish(msg_to_webcam_test)


    def get_dominant_color(self , image, n_colors=1):
        pixels = np.float32(image).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS
        flags, labels, centroids = cv2.kmeans(
            pixels, n_colors, None, criteria, 10, flags)
        palette = np.uint8(centroids)
        #return the color of the cluster with the most elements in it 
        return palette[np.argmax(itemfreq(labels)[:, -1])]


def main(args=None):
    rclpy.init(args=args)
    
    image_detection = traffic_sign_detection()
    
    rclpy.spin(image_detection)
    
    image_detection.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
