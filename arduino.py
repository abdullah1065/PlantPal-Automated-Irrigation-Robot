def test(param):
    import serial
    import time

    ser = serial.Serial('/dev/ttyACM0', 9600)

    try:
        last_pump_state = False
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                parts = line.split(", ")
                if len(parts) == 2:
                    moisture_level = int(parts[0].split(": ")[1])
                    water_level = int(parts[1].split(": ")[1])
                    # Control pump based on soil moisture
                    if moisture_level > param and not last_pump_state:  # Dry soil threshold
                        ser.write("TURN_ON_PUMP\n".encode())
                        last_pump_state = True
                    elif moisture_level < param and last_pump_state:  # Wet soil threshold
                        ser.write("TURN_OFF_PUMP\n".encode())
                        last_pump_state = False
                        return
            time.sleep(1)