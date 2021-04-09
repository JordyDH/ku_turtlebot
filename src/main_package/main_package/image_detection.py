import sys

import cv2
import cv_bridge
import numpy as np
import message_filters
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy
from sensor_msgs.msg import *
from object_msgs.msg import *
from vision_msgs.msg import Detection2DArray
from std_msgs.msg import *

VIDEO_FILE = "data/stop_sign.mp4"
class subImageDetection(Node):

    def __init__(self):
        super().__init__('detection_visualizer')
        self._bridge = cv_bridge.CvBridge()
        
        #quality of service 
        output_image_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE,
            depth=1) 
        self._image_pub = self.create_publisher(Image, 'webcam_det', output_image_qos) 
        # self.recevived_image  =  self.create_subscription(Image, 'webcam', self.on_detections, 10)
        self._image_sub = message_filters.Subscriber(self, Image, 'webcam')
        # self._detections_sub = message_filters.Subscriber(self, Detection2DArray, '~/detections')
        self._synchronizer = message_filters.ApproximateTimeSynchronizer(
            (self._image_sub, self._detections_sub), 5, 0.01)#queue_size=5 , slop=0.1   
        
        self._synchronizer.registerCallback(self.on_detections) #output
        
    def on_detections(self, image_msg ,detections_msg):
        print("here1")
        self.get_logger().info('Frame')
        print("here2")
        cv_image = self._bridge.imgmsg_to_cv2(image_msg)
        print("here3")
        # Draw boxes on image
        print(len(detections_msg.detections))
        for detection in detections_msg.detections:
            max_class = None
            max_score = 0.0
            for hypothesis in detection.results:
                if hypothesis.score > max_score:
                    max_score = hypothesis.score
                    max_class = hypothesis.id
            if max_class is None:
                print("Failed to find class with highest score", file=sys.stderr)
                return

            cx = detection.bbox.center.x
            cy = detection.bbox.center.y
            sx = detection.bbox.size_x
            sy = detection.bbox.size_y
            print("cx", cx , "cy", cy , "sx")
            min_pt = (round(cx - sx / 2.0), round(cy - sy / 2.0))
            max_pt = (round(cx + sx / 2.0), round(cy + sy / 2.0))
            color = (0, 255, 0)
            thickness = 1
            cv2.rectangle(cv_image, min_pt, max_pt, color, thickness)

            label = '{} {:.3f}'.format(max_class, max_score)
            pos = (min_pt[0], max_pt[1])
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(cv_image, label, pos, font, 0.75, color, 1, cv2.LINE_AA)

        self._image_pub.publish(self._bridge.cv2_to_imgmsg(cv_image, encoding="bgr8"))


def main(args=None):
    rclpy.init(args=args)
    
    image_detection = subImageDetection()
    
    rclpy.spin(image_detection)
    
    image_detection.destroy_node()
    rclpy.shutdown()