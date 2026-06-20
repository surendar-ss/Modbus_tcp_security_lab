"""
modbus_master.py
-----------------
Acts like a normal SCADA/HMI poller: connects to the PLC (our slave),
reads the Temperature and Setpoint holding registers using function
code 03 (Read Holding Registers), and prints them.

This is the "legitimate traffic" baseline. Run this AFTER modbus_slave.py
is already running.
"""

from pymodbus.client.sync import ModbusTcpClient

HOST = "127.0.0.1"
PORT = 5020

def main():
    client = ModbusTcpClient(HOST, port=PORT)

    if not client.connect():
        print("[MASTER] Could not connect to slave. Is modbus_slave.py running?")
        return

    print(f"[MASTER] Connected to PLC at {HOST}:{PORT}")

    # Function code 03: Read Holding Registers
    # address=0 is the starting offset, count=2 reads Temperature + Setpoint
    result = client.read_holding_registers(address=0, count=2, slave=0)

    if result.isError():
        print(f"[MASTER] Error reading registers: {result}")
    else:
        temperature = result.registers[0]
        setpoint = result.registers[1]
        print(f"[MASTER] Temperature register = {temperature}")
        print(f"[MASTER] Setpoint register    = {setpoint}")

    client.close()
    print("[MASTER] Connection closed.")

if __name__ == "__main__":
    main()