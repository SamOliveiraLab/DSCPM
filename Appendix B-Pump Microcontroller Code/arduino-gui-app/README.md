# Arduino GUI Application

This project is a GUI application designed to enable serial communication with an Arduino. It features controls for managing a variable called flow rate and direction, allowing for easy interaction and monitoring.

## Project Structure

```
arduino-gui-app
├── src
│   ├── main.py              # Entry point for the application
│   ├── gui
│   │   └── app.py           # GUI implementation
│   ├── serial
│   │   └── communication.py  # Serial communication management
│   └── utils
│       └── simulator.py      # Simulated functions for testing
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd arduino-gui-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

The GUI will open, allowing you to control the flow rate and direction. Use the slider and text box to set the flow rate, and toggle the switch to change the direction.

## Future Development

- Implement the actual serial communication in `communication.py`.
- Enhance the GUI with additional features as needed.
- Consider adding error handling for serial communication.

## Notes

# Arduino GUI Application

This project is a GUI application designed to enable serial communication with an Arduino. It features controls for managing a variable called flow rate and direction, allowing for easy interaction and monitoring.

## Project Structure

```
arduino-gui-app
├── src
│   ├── main.py              # Entry point for the application
│   ├── gui
│   │   └── app.py           # GUI implementation
│   ├── serial
│   │   └── communication.py  # Serial communication management
│   └── utils
│       └── simulator.py      # Simulated functions for testing
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd arduino-gui-app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```bash
python src/main.py
```

The GUI will open, allowing you to control the flow rate and direction. Use the slider and text box to set the flow rate, and toggle the switch to change the direction.

## Future Development

- Implement the actual serial communication in `communication.py`.
- Enhance the GUI with additional features as needed.
- Consider adding error handling for serial communication.

## Notes
