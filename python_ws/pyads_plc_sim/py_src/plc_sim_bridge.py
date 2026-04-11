from .plc_connector import plc_connector
from .plc_signals import PLC_Signals
from .logger import PLCLogger
import threading
import time


class PlcSimBridge:
    def __init__(self, target_ams, target_port):
        self.logger = PLCLogger("SIM_BRIDGE")
        self.plc = plc_connector(target_ams, target_port)
        self.wait_for_plc()          # ← just WAIT, don't connect (watchdog does it)
        self.signals = PLC_Signals

        ##################################
        # We separate input and output
        # to handle it better
        ##################################
        self.input_data = {}
        self.output_data = {}
        self.input_keys = list(self.signals.MAPPING_PLC_INPUTS.keys())
        self.output_keys = list(self.signals.MAPPING_PLC_OUTPUTS.keys())
        for key, config in self.signals.MAPPING_PLC_INPUTS:
            # self.logger.info(f"Input Key: {key}")
            config["handle"] = self.get_var_handle(config["plc"])
            self.input_data[key] = None

        for key, config in self.signals.MAPPING_PLC_OUTPUTS:
            # self.logger.info(f"Output Key: {key}")
            self.output_data[key] = None
            config["handle"] = self.get_var_handle(config["plc"])

    #############################
    # Get handle of the var
    #############################
    def get_var_handle(self, var_name):
        if not self.plc.isAlive:
            self.logger.error(
                f"Error While reading handle  of var {var_name}. PLC is not alive")
            return None
        return (self.plc.get_handle(var_name))

    #############################
    # Release PLC handle
    #############################
    def release_plc_handle(self):
        for key, config in self.signals.MAPPING_PLC_INPUTS:
            if config["handle"] is not None:
                self.plc.release_handle(config["handle"])
                config["handle"] = None
    #############################
    # Wait for PLC to autoconnect
    # from the watchdog
    ##############################

    def wait_for_plc(self):
        """Wait until the watchdog establishes connection."""
        self.logger.info("Attempting to connect to PLC")
        while not self.plc.isAlive:
            self.logger.info("Waiting for PLC connection...")
            time.sleep(1)
        self.logger.info("Connection successful")

    def read_from_plc(self):
        self.logger.info("Reading from PLC")
        if self.plc.isAlive:
            for key, config in self.signals.MAPPING_PLC_OUTPUTS.items():
                try:
                    val = self.plc.read_by_handle(
                        config["handle"], config["type"])
                    self.output_data[key] = val
                except Exception as e:
                    self.logger.error(f"Failed to sync input {key}: {e}")
        else:
            self.logger.error("PLC is Not Communicating")

    def write_to_plc(self):
        self.logger.info("Writing to PLC")
        if self.plc.isAlive:
            for key, config in self.signals.MAPPING_PLC_INPUTS.items():
                val = self.input_data.get(key)
                if val is not None:
                    try:
                        self.plc.write_to_handle(
                            config["handle"], val, config["type"])
                    except Exception as e:
                        self.logger.error(f"Failed to write output {key}: {e}")
                else:
                    self.logger.error(
                        f"Cannot write {key} to PLC: Value is None")
        else:
            self.logger.error("Writing fails as plc is not alive")

    def run_step(self):
        self.read_from_plc()

        # TODO: do the action block here
        self.set_key_value("conveyor_is_moving",
                           self.get_key_value("move_conveyor"))
        self.set_key_value("conveyor_is_stopped",
                           self.get_key_value("stop_conveyor"))

        for key in self.input_keys:
            if self.get_key_value(key) is None:
                self.set_key_value(key, False)

        self.write_to_plc()

    def get_key_value(self, key):
        if key in self.input_keys:
            self.logger.info(f"{key} is found in input key list")
            try:
                value = self.input_data[key]
                return value
            except Exception as e:
                self.logger.error(
                    f"Error while reading the input key value {key}: {e}")
                return None

        if key in self.output_keys:
            self.logger.info(f"{key} is found in output key  list")
            try:
                value = self.output_data[key]
                return value
            except Exception as e:
                self.logger.error(
                    f"Error while reading the output key value {key}: {e}")
                return None
        self.logger.warn("Key {key} not in the list defined")
        return None

    def set_key_value(self, key, value):
        # set key value only sets to output as it is logically not possible to set an input from plc
        if key in self.input_keys:
            try:
                self.input_data[key] = value
            except Exception as e:
                self.logger.error(
                    f"Error faced while writing {value} to the {key}: {e}")

        else:
            self.logger.warn(f"{key} is not a valid output key")
