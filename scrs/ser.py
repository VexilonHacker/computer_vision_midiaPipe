import serial

# Open the serial port
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    try:
        # Read data from the serial port
        data = ser.readline().decode('utf-8').strip()
        print(data)
    except Exception as e:
        print(f"Error: {e}")
        break

# Close the serial port
ser.close()

