from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext,
)
from pymodbus.server.sync import StartTcpServer

HOST = "127.0.0.1"
PORT = 5020  # Real Modbus TCP uses port 502; 5020 avoids needing root

def build_context():
    # 10 holding registers starting at address 0.
    # index 0 = Temperature (42), index 1 = Setpoint (100)
    initial_values = [42, 100] + [0] * 8
    block = ModbusSequentialDataBlock(0, initial_values)

    store = ModbusSlaveContext(hr=block, zero_mode=True)  # hr = holding registers
    context = ModbusServerContext(slaves=store, single=True)
    return context

if __name__ == "__main__":
    context = build_context()
    print(f"[SLAVE] Starting Modbus TCP server on {HOST}:{PORT}")
    print("[SLAVE] Holding register 0 = Temperature (42)")
    print("[SLAVE] Holding register 1 = Setpoint (100)")
    print("[SLAVE] No authentication. No encryption. Anyone who can reach")
    print("[SLAVE] this port can read AND write these registers.")
    StartTcpServer(context=context, address=(HOST, PORT))
