import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class ImageProcessor:
    def process_image(self, cv_image):
        if cv_image is None or cv_image.size == 0:
            return None
        return (cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY))


class Image2Grayscale(Node):
    def __init__(self):
        super().__init__('image_grayscale_processor')

        self.bridge = CvBridge()
        self.image_processor = ImageProcessor()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.publisher = self.create_publisher(
            Image,
            '/camera/image_gray',
            10
        )
        self.get_logger().info('Grayscale Node has started')

    def image_callback(self, msg):
        self.get_logger().info(f'Received Image: {msg.width} x {msg.height},'
                               f'Encodincg: {msg.encoding},'
                               f'Step:  {msg.step}')

        current_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray_frame = self.image_processor.process_image(current_frame)
        gray_msg = self.bridge.cv2_to_imgmsg(gray_frame, encoding='mono8')
        gray_msg.header = msg.header

        self.publisher.publish(gray_msg)
        self.get_logger().info('Published Grayscale Image')


def main(args=None):
    rclpy.init(args=args)
    img_to_grayscalenode = Image2Grayscale()
    rclpy.spin(img_to_grayscalenode)
    img_to_grayscalenode.destroy_node()
    rclpy.shutdown()
