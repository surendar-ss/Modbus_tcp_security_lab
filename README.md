# Modbus TCP: Unauthenticated Write Demonstration

A minimal Modbus TCP lab showing the protocol's most fundamental security
gap:it has no authentication, no authorization, and no encryption.
Any client that can reach the right IP and port can read or write any
register there is no way for the device to tell a legitimate SCADA
master apart from an attacker.

## What's in this repo

 File | Role 
modbus_slave.py  : Simulated PLC. Exposes Temperature (register 0) and Setpoint (register 1) as Modbus holding registers over TCP. 
modbus_master.py :Legitimate HMI/SCADA poller. Reads both registers using function code 03. 
modbus_attack.py : A completely separate, uncredentialed script. Sends function code 06 (Write Single Register) to overwrite the Setpointwith nothing proving it's allowed to. 
my_modbus_capture.pcapng : Wireshark capture of the full sequence: legitimate read → unauthorized write → legitimate read again. 
attack_proof.png :Wireshark screenshot showing the decoded attack packet function code, register number, and the malicious value, in plaintext.

## What the attack looks like in Wireshark

![Wireshark capture showing unauthenticated write](attack_proof.png)

The PLC accepted a write to register 1 with the value `9999`  no
authentication field exists anywhere in the frame.

## How to run it

```bash
pip install -r requirements.txt

# Terminal 1
python3 modbus_slave.py

# Terminal 2 — run these one at a time
python3 modbus_master.py     # Setpoint = 100
python3 modbus_attack.py     # overwrites Setpoint to 9999, no auth check
python3 modbus_master.py     # Setpoint = 9999 -- the write succeeded
```

To capture your own traffic for Wireshark:

```bash
sudo tcpdump -i lo -w my_modbus_capture.pcapng port 5020
# (run the three scripts above in another terminal while this is capturing)
```

Open the resulting ."pcapng" in Wireshark and filter on " tcp.port == 5020".
Every field function code, register address, register value is
visible in plaintext.

## What the capture shows

Decoded from the actual bytes on the wire:

Legitimate read: client sends function code 03, address 0,
  count 2. PLC replies with Temperature= 42, Setpoint= 100both
  values sent unencrypted.
Unauthorized write : a separate script sends function code 06,
  address 1, value 9999. There is no field in the Modbus TCP frame
  for a credential, token, or signature he PLC has no way to check
  whether this command is legitimate.
Read after the attack : Setpoint now reads 9999. The "real" HMI
  has no idea the value was changed by something other than itself.

In a real plant, register 1 might be a pressure setpoint, a valve
position, or a safety interlock threshold. Function code 06 (or 16,
Write Multiple Registers) lets anyone on the network segment change it.


## Limitations of this demo

Runs on 127.0.0.1 (loopback) for safety and simplicity — no real
  network or hardware involved.
This is not a tool for attacking real industrial equipment.
  Never run "modbus_attack.py" style scripts against a live PLC,
  SCADA system, or any device you don't own and have explicit
  permission to test. Unauthorized access to industrial control
  systems is illegal and can cause real physical harm.
For a closer to real lab, the same scripts work unmodified against
  a real PLC's Modbus TCP port (typically 502) on an isolated test
  bench just change HOST/PORT 
