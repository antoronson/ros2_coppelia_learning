from py_src.logger import PLCLogger
import pyads

class plc_connector:
    def __init__ (self, target_ams_id, target_port):
        self.logger = PLCLogger()
        self.logger.info("Logging PLC Connector")
        self.logger.info("------------------------------------")
        self.logger.info("Try connecting to PLC")
        self.plc = pyads.Connection(target_ams_id, target_port)
        

    def connect(self):
        try:
            self.plc.open()
        except Exception as e:
            self.logger.error(f"Failed opening connection to PLC {e}")


    @property
    def is_connected(self):
        try:
            state, _ = self.plc.read_state()
            return state in [pyads.ADSSTATE_RUN, pyads.ADSSTATE_CONFIG]
        except (pyads.ADSError, AttributeError) as e:
            self.logger.error(f"connecting pyads to twincat faces ads error {e}")
            return False
        