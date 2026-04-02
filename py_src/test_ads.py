import pyads
from logger import PLCLogger

TARGET_AMS_ID = '192.168.2.137.1.1' # Link the ams id of the twincat plc
TARGET_PORT   = pyads.PORT_TC3PLC1

plc = pyads.Connection(TARGET_AMS_ID, TARGET_PORT)
def main():
    log= PLCLogger()
    log.info("Try to open the ads port and check communication with plc")
    try:

        plc.open()

        state = plc.read_state()
        log.info(f"Recorded state is {state}")
        #print(f"PLC State: {state}")

    finally:
        plc.close()


if __name__ == '__main__':
    main()