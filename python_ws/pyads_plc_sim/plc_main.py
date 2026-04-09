from .py_src.plc_sim_bridge import PlcSimBridge
import time
def main():
    ams_id ="192.168.2.137.1.1"
    port = 851
    sim_bridge = PlcSimBridge(ams_id, port)
    try:
        while True:
            sim_bridge.run_step()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Shutting down Bridge")
    
if __name__ == '__main__':
    main()