from py_src.plc_connector import plc_connector
from py_src.plc_signals import PLC_Signals
from py_src.logger import PLCLogger
class PlcSimBridge:
    def __init__(self):
        self.logger = PLCLogger("SIM_BRIDGE")
        self.plc = plc_connector("192.168.2.137.1.1", 851)
        self.signals = PLC_Signals
        self.is_running = False
    
    def connect(self):
        self.logger("Attempting to connect to PLC")
        self.plc.connect()

