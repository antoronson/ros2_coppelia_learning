import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class SimTimeSubscriber(Node):
    def __init__(self):
        super().__init__('simulation_time_subscriber')
        self.subscription = self.create_subscription(
                    Float32,
                    'coppelia_bridge', 
                    self.listner_callback,
                    10
        )
        self.subscription

    def listner_callback(self, msg):
        self.get_logger().info(f'Current Simulation time: {msg.data}')

    
def main(args=None):
    rclpy.init(args=args)
    sim_time_subscriber = SimTimeSubscriber()
    rclpy.spin(sim_time_subscriber)


    sim_time_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()