import random
import time


class FakeArduino:
    def __init__(self):
        # Simulating the state variables from your Arduino code
        self.on = 1  # System ON by default
        self.pos = 5  # Initial servo position
        self.fwd = 0  # Direction (0 or 1)
        self.infuse = 1  # Infusion mode
        self.flowrate = 1.5  # Default flow rate in µL/min
        self.valvestate = 0  # Initial valve state
        self.amountpumped = 0  # Total volume pumped in µL
        self.newdelay = 100  # Default delay
        self.uLperdeg = 0.1  # Simulated µL per degree of servo movement

    def process_command(self, command):
        """
        Simulates the processing of commands received over serial.
        """
        if command == "0":
            self.turn_off()
        elif command == "123":
            self.turn_on()
        elif command == "321":
            self.switch_direction()
        elif command.isdigit():
            self.change_flowrate(int(command))
        else:
            return "Invalid Command"
        return self.get_status()

    def turn_off(self):
        """Simulates turning the system off."""
        self.on = 0
        return "System turned OFF. Position saved."

    def turn_on(self):
        """Simulates turning the system on."""
        self.on = 1
        return "System turned ON."

    def switch_direction(self):
        """Simulates switching the pumping direction."""
        self.fwd = 1 - self.fwd
        self.infuse = 1 - self.infuse
        return f"Direction switched. Fwd: {self.fwd}, Infuse: {self.infuse}"

    def change_flowrate(self, flowrate):
        """Simulates changing the flow rate."""
        self.flowrate = flowrate
        self.calculate_new_delay()
        return f"Flow Rate Changed to {self.flowrate} µL/min"

    def calculate_new_delay(self):
        """Calculates a new delay based on the flow rate."""
        self.newdelay = max(10, int(60000 / (self.uLperdeg * self.flowrate)))

    def get_status(self):
        """Returns the simulated status as a string."""
        return f"Pos: {self.pos}, Fwd: {self.fwd}, Infuse: {self.infuse}, Flowrate: {self.flowrate} µL/min, Amount Pumped: {self.amountpumped} µL, Delay: {self.newdelay} ms"

    def simulate_movement(self):
        """Simulates movement and updates internal state."""
        if self.on == 1:
            if self.fwd == 0:
                self.pos += 1
                self.amountpumped += self.uLperdeg
            else:
                self.pos -= 1
                self.amountpumped -= self.uLperdeg

            # Clamp position between min and max values
            if self.pos < 5:
                self.pos = 5
                self.fwd = 0  # Reverse direction
            elif self.pos > 70:
                self.pos = 70
                self.fwd = 1  # Reverse direction

        return self.get_status()


# Simulated communication interface
def simulate_serial_communication():
    arduino = FakeArduino()
    print("Simulated Arduino Ready. Type 'exit' to quit.")
    try:
        while True:
            command = input(
                "Enter command (0 to turn off, 123 to turn on, 321 to switch direction, or a flow rate): ").strip()
            if command.lower() == "exit":
                print("Exiting simulation.")
                break

            response = arduino.process_command(command)
            print(f"Arduino Response: {response}")

            # Simulate movement after each command
            movement_status = arduino.simulate_movement()
            print(f"Simulated Movement: {movement_status}")
    except KeyboardInterrupt:
        print("\nSimulation interrupted. Exiting.")


# Run the simulation
if __name__ == "__main__":
    simulate_serial_communication()
