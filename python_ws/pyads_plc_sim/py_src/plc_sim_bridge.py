from .plc_connector import plc_connector
from .plc_signals import PLC_Signals
from .logger import PLCLogger
import threading
import time

class PlcSimBridge:
    def __init__(self, target_ams, target_port):
        self.logger = PLCLogger("SIM_BRIDGE")
        self.plc = plc_connector(target_ams, target_port)
        self.wait_and_connect_to_plc()
        self.signals = PLC_Signals
        self.io_data={}
        all_keys = list(self.signals.MAPPING_PLC_INPUTS.keys()) + \
                    list(self.signals.MAPPING_PLC_OUTPUTS.keys())
        for key in all_keys:
            self.io_data[key] = None
    

    def wait_and_connect_to_plc(self):
        while True:
            self.logger.info("Attempting to connect to PLC")
            try:
                self.plc.connect()
                if self.plc.is_connected:
                    self.logger.info("Connection successful")
                    break
            except Exception as e:
                self.logger.error(f"Connecting to PLC faces exception: {e}")
        
            self.logger.info("Attempting reconnect after 5 seconds")
            time.sleep(5)


    def read_from_plc(self):
        self.logger.info("Reading from PLC")
        if self.plc.isAlive:
            for key, config in self.signals.MAPPING_PLC_OUTPUTS.items():
                try:
                    val = self.plc.read_variable(config["plc"], config["type"])
                    self.io_data[key] = val
                except Exception as e:
                    self.logger.error(f"Failed to sync input {key}: {e}")
        else:
            self.logger.error(f"PLC is Not Communicating")

    def write_to_plc(self):
        self.logger.info("Writing to PLC")
        if self.plc.isAlive:
            for key, config in self.signals.MAPPING_PLC_INPUTS.items():
                if key in self.io_data:
                    val = self.io_data.get(key)
                    if val is not None:
                        try:
                            self.plc.write_variable(config["plc"], val, config["type"])
                        except Exception as e:
                            self.logger.error(f"Failed to write output {key}: {e}")
                    else:
                        self.logger.error(f"Cannot write {key} to PLC: Value is Nones")
        else:
            self.logger.error(f"Writing fails as plc is not alive")

    def run_step(self):
        self.read_from_plc()


        #TODO do the action block here
        self.io_data["conveor_is_moving"] = self.io_data["move_conveyor"]
        self.io_data["conveyor_is_stopped"] = self.io_data["stop_conveyor"]
        self.write_to_plc()