class PLC_Signals:
    """
        Output Signals to the Plc program
    """
    to_plc_move_conveyor = "GVL_IO.Conveyor_Outputs.bMoveConveyor"
    to_plc_stop_conveyor = "GVL_IO.Conveyor_Outputs.bStopConveyor"
    to_plc_enable_conveyor = "GVL_IO.Conveyor_Outputs.bEnableConveyor"


    """Input Signals from the PLC Program
    	bConveyorIsMoving	:BOOL;
	    bConveyorStopped	:BOOL;
	    bPartDetected		:BOOL;
	    bPartAvailable2Move	:BOOL;
	    bRobInSpace			:BOOL;
    """
    from_plc_conveyor_is_moving = "GVL_IO.Conveyor_Inputs.bConveyorIsMoving"
    from_plc_comveyor_is_stopped = "GVL_IO.Conveyor_Inputs.bConveyorStopped"
    from_plc_part_detected = "GVL_IO.Conveyor_Inputs.bPartDetected"
    from_plc_PartAvailable_to_move = "GVL_IO.Conveyor_Inputs.bPartAvailable2Move"
    from_plc_rob_in_space = "GVL_IO.Conveyor_Inputs.bRobInSpce"
