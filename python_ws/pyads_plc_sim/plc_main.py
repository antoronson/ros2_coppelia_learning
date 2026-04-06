from .py_src.plc_sim_bridge import PlcSimBridge

def main():
    ams_id ="192.168.2.137.1.1"
    port = 851
    sim_bridge = PlcSimBridge(ams_id, port)
    sim_bridge.run_step()

    
if __name__ == '__main__':
    main()