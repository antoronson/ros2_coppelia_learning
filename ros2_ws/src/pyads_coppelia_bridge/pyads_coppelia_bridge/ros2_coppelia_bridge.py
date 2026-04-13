import rclpy
from rclpy.node import Node
from pyads_coppelia_interfaces.msg import StationSignals
import threading


class Ros2_Coppelia_Bridge(Node):
    def __init__(self):
        super().__init__('ros2_transport')
        self._feedback = {}
        self._lock = threading.lock()
        self.publisher = self.create_publisher(
            StationSignals,
            'station/output',
            10
        )
        self.subscription = self.create_subscription(
            StationSignals,
            'station/input',
            self._coppelia_callback,
            10
        )

    def _coppelia_callback(self, msg: StationSignals):
        msg = StationSignals()
        self._feedback
