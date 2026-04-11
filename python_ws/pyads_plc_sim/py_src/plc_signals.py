import pyads


class PLC_Signals:
    """
        Output Signals to the Plc program
    """
    MAPPING_PLC_OUTPUTS = {
        "move_conveyor": {"plc": "GVL_IO.Conveyor_Outputs.bMoveConveyor",      "type": pyads.PLCTYPE_BOOL, "handle": None},
        "stop_conveyor": {"plc": "GVL_IO.Conveyor_Outputs.bStopConveyor",      "type": pyads.PLCTYPE_BOOL, "handle": None},
        "enable_conveyor": {"plc": "GVL_IO.Conveyor_Outputs.bEnableConveyor",    "type": pyads.PLCTYPE_BOOL, "handle": None}
    }

    """Input Signals from the PLC Program
    	bConveyorIsMoving	:BOOL;
	    bConveyorStopped	:BOOL;
	    bPartDetected		:BOOL;
	    bPartAvailable2Move	:BOOL;
	    bRobInSpace			:BOOL;
    """
    MAPPING_PLC_INPUTS = {
        "conveyor_is_moving": {"plc": "GVL_IO.Conveyor_Inputs.bConveyorIsMoving",  "type": pyads.PLCTYPE_BOOL, "handle": None},
        "conveyor_is_stopped": {"plc": "GVL_IO.Conveyor_Inputs.bConveyorStopped",   "type": pyads.PLCTYPE_BOOL, "handle": None},
        "part_detected": {"plc": "GVL_IO.Conveyor_Inputs.bPartDetected",      "type": pyads.PLCTYPE_BOOL, "handle": None},
        "part_available_to_move": {"plc": "GVL_IO.Conveyor_Inputs.bPartAvailable2Move", "type": pyads.PLCTYPE_BOOL, "handle": None},
        "rob_in_space": {"plc": "GVL_IO.Conveyor_Inputs.bRobInSpace",        "type": pyads.PLCTYPE_BOOL, "handle": None}
    }
