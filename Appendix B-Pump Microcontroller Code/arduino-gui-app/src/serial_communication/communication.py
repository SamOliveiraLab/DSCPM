import serial
import random
import time
from datetime import datetime

# Initialize serial communication
# Adjust the COM port and baud rate as per your Arduino setup
# ser = serial.Serial(port='COM3', baudrate=9600, timeout=1)


def communicate(command):
    """
    Communicates with the Arduino: sends a command, waits for a response, and logs data.
    """
    try:
        # Encode the command
        data = encode(command)

        # Send the encoded command one at a time
        for i in data:
            tx(i)
            time.sleep(0.1)  # Delay between sending each character

        # Wait for completion with a timeout
        # remove input cammond when doing hardware integreation
        active_data = rx(command)

        # Decode the received data
        active_value = decode(active_data)

        # Log the communication to a file
        log_data(command, active_value)

    except Exception as e:
        print(f"Error in communication: {e}")


def tx(data):
    """
    Sends encoded data to the Arduino using the serial Tx line.
    """
    if data is not None:
        # ser.write(data.encode())  # Convert to bytes and send over serial
        print(f"Sent: {data}")
    else:
        print("Readonly mode - no data sent.")


def rx(data):  # remove input cammond when doing hardware integreation
    """
    Reads encoded data from the Arduino using the serial Rx line with timeout functionality.
    """
    timeout = 5  # seconds
    start_time = time.time()

    while True:
        if time.time() - start_time > timeout:
            print("Timeout waiting for response from Arduino.")
            return None  # Indicate a timeout occurred

        # Simulate reading from Arduino (replace with actual serial reading in production)
        # response = ser.readline().decode().strip()  # Uncomment this in actual implementation

        if data is None:
            response = 8 * random.randint(-75, 75)  # Simulated response
        else:
            response = data  # Simulated response

        if response:  # Check if a response is received
            # print(f"Received: {response}")
            return response  # Return the received response


def encode(command):
    """
    Encodes a command into the format expected by the Arduino and returns a vector.

    Input:
        command: signed float or None
            - Positive -> [123, absolute value of the command]
            - Negative -> [321, absolute value of the command]
            - Zero -> [stop: -1, 0]
            - None -> [readonly: None, None]  # Read-only mode

    Special Case:
        If the absolute value of the command equals 123 or 321 (reserved codes),
        adjusts the flow rate by +1 or -1, respectively.

    Output:
        A vector [code, value], where `code` is the direction command and `value` is the flow rate.
    """
    if command is None:
        return [None, None]  # Read-only mode

    try:
        # Convert the command to a float
        command = float(command)
        direction = 123 if command > 0 else 321 if command < 0 else -1
        flow_rate = abs(command)

        # Adjust flow rate if it equals a reserved code
        if flow_rate == 123:
            flow_rate += 1
        elif flow_rate == 321:
            flow_rate -= 1

        return [direction, flow_rate]
    except ValueError:
        # Handle invalid input
        return ["Invalid", None]


def decode(data):
    """
    Decodes the data received from the Arduino.
    """
    try:
        # Assuming the Arduino sends only the active_value
        return float(data)  # Convert to float for numerical logging
    except ValueError:
        print("Failed to decode data.")
        return None


def log_data(command, active_value):
    """
    Logs data to a file in the specified format: datetime, set_value (command), active_value.
    """
    if active_value is not None:
        with open("pump_log.csv", "a") as log_file:
            log_file.write(
                f"{datetime.now()}, {command}, {active_value}\n")
        print(
            f"Logged: {datetime.now()}, {command}, {active_value}")


# Example usage
""" if __name__ == "__main__":
    print("Starting Arduino communication. Type 'exit' to quit.")
    try:
        while True:
            user_command = input(
                "Enter a command (): ").strip()
            if user_command.lower() == "exit":
                print("Exiting program.")
                break
            communicate(user_command)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")
 """
