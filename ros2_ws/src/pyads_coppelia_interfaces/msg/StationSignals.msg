#pyads part
bool move_conveyor
bool stop_conveyor
bool enable_conveyor

#coppelia_sim part
bool conveyor_is_moving     #link to conv changing position
bool conveyor_is_stopped    #link to the inverted of above
bool part_detected          #link to second proximity sens
bool part_available_to_move #link to first proximity sens
bool rob_in_space           # TODO: link to robot

# Metadata
builtin_interfaces/Time stamp
string source          # "plc" or "sim"
