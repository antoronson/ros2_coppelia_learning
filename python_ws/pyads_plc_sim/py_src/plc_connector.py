from .logger import PLCLogger
import pyads
import threading
import time


class plc_connector:
    def __init__ (self, target_ams_id, target_port):
        self.logger = PLCLogger("PLC_CONN")
        self.logger.info("Logging PLC Connector")
        self.logger.info("------------------------------------")
        self.logger.info("Try connecting to PLC")
        self.plc = pyads.Connection(target_ams_id, target_port)
        self.isAlive = False
        self._stop_watchdog = threading.Event()
        self._watchdog_thread = threading.Thread(target=self._connection_watchdog, daemon=True)
        self._watchdog_thread.start()

    def connect(self):
        try:
            self.plc.open()
        except Exception as e:
            self.logger.error(f"Failed opening connection to PLC {e}")

    
    def _connection_watchdog(self):
        while not self._stop_watchdog.is_set():
            try:
                self.isAlive = self.is_connected
            except Exception:
                self.isAlive = False
            
            time.sleep(0.5)

    @property
    def is_connected(self):
        try:
            state, _ = self.plc.read_state()
            return state in [pyads.ADSSTATE_RUN, pyads.ADSSTATE_CONFIG]
        except (pyads.ADSError, AttributeError) as e:
            self.logger.error(f"connecting pyads to twincat faces ads error {e}")
            return False
        
    def read_variable(self, symbol_name, plc_type = pyads.PLCTYPE_BOOL):
        try:
            return self.plc.read_by_name(symbol_name, plc_type)
        except pyads.ADSError as e:
            self.logger.error(f"Reading {symbol_name} with datatype {plc_type} return error {e}")
            return None
    

    def write_variable(self, symbol_name, value, plc_type=pyads.PLCTYPE_BOOL):
        try:
            self.plc.write_by_name(symbol_name, value, plc_type)
        except pyads.ADSError as e:
            self.logger.error(f"Writing {symbol_name} with value {value} and Datatype {plc_type} return error {e}")
    
