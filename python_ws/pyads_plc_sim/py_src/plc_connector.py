from .logger import PLCLogger
import pyads
import threading
import time


class plc_connector:
    def __init__(self, target_ams_id, target_port):
        self.target_ams_id = target_ams_id
        self.target_port = target_port
        self.logger = PLCLogger("PLC_CONN")
        self.logger.info("Logging PLC Connector")
        self.logger.info("------------------------------------")
        self.logger.info("Try connecting to PLC")
        self.plc = pyads.Connection(self.target_ams_id, self.target_port)
        self.isAlive = False
        self._lock = threading.Lock()
        self._stop_watchdog = threading.Event()
        self._watchdog_thread = threading.Thread(
            target=self._connection_watchdog, daemon=True)
        self._watchdog_thread.start()

    def connect(self):
        try:
            self.plc.open()
        except Exception as e:
            self.logger.error(f"Failed opening connection to PLC {e}")

    def disconnect_plc(self):

        try:
            if self.plc and self.plc.is_open:
                self.plc.close()
        except Exception as e:
            self.logger.error(f"Failed closing connection to plc {e}")

    def _connection_watchdog(self):
        while not self._stop_watchdog.is_set():
            plc_is_connected = self.is_connected
            if not plc_is_connected:
                self.logger.warn(
                    "PLC Connection lost. Attempting to reconnect")
                self._reconnect()
                self.isAlive = self.is_connected
            else:
                self.isAlive = True
                # time.sleep(0.1)

            time.sleep(1)

    def _reconnect(self):
        with self._lock:
            try:
                self.disconnect_plc()
                time.sleep(0.5)
                self.plc = pyads.Connection(
                    self.target_ams_id, self.target_port)
                self.connect()
            except Exception as e:
                self.logger.error(f"Reconnection to PLC failed {e}")

    @property
    def is_connected(self):
        if self.plc is None:
            return False

        if self.plc.is_open is None:
            return False
        try:
            if not self.plc.is_open:
                return False

            result = self.plc.read_state()

            if result is None:
                return False
            state, _ = result
            return state in [pyads.ADSSTATE_RUN, pyads.ADSSTATE_CONFIG]
        except (pyads.ADSError, AttributeError) as e:
            self.logger.error(
                f"connecting pyads to twincat faces ads error {e}")
            return False

    def read_by_handle(self, handle, plc_type=pyads.PLCTYPE_BOOL):
        try:
            return (self.plc.read_by_name('', plc_type, handdle=handle))
        except pyads.ADSError as e:
            self.logger.error(
                f"Reading {handle}, with datatype {plc_type} return error: {e}")

     def write_to_handle(self, handle,value, plc_type=pyads.PLCTYPE_BOOL):
        try:
            return (self.plc.write_by_name('', value, plc_type, handle=handle))
        except pyads.ADSError as e:
            self.logger.error(
                f"Reading {handle}, with datatype {plc_type} return error: {e}")
            
    def read_variable(self, symbol_name, plc_type=pyads.PLCTYPE_BOOL):
        try:
            return self.plc.read_by_name(symbol_name, plc_type)
        except pyads.ADSError as e:
            self.logger.error(
                f"Reading {symbol_name} with datatype {plc_type} return error {e}")
            return None

    def write_variable(self, symbol_name, value, plc_type=pyads.PLCTYPE_BOOL):
        try:
            self.plc.write_by_name(symbol_name, value, plc_type)
        except pyads.ADSError as e:
            self.logger.error(
                f"Writing {symbol_name} with value {value} and \
                    Datatype {plc_type} return error {e}")
