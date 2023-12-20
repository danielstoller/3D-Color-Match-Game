# 3D Color Match

This project involves creating a 3D color matching game using an MPU6050 IMU sensor with Arduino for real-time input and PyOpenGL, PyGame, and Tkinter in Python for visualization. The game requires players to match the color of a 3D object with the background color by adjusting the color components using tilt inputs from the IMU sensor.

## Prerequisites

To set up and run this project, you'll need the following:

- **Hardware:**
  - MPU6050 IMU sensor
  - Arduino (e.g., Arduino Pro Micro)
  
  For Arduino Pro Micro, connect the MPU6050 to the using the following pinout:
  - VCC -> VCC
  - GND -> GND
  - SCL -> Digital Pin 3
  - SDA -> Digital Pin 2

- **Software:**
  - Python installed on your machine
  - The following libraries installed: PyOpenGL, PyGame, PySerial, and Tkinter
  - Install the required Python libraries using:
    ```bash
    pip install PyOpenGL PyGame PySerial tk
    ```

## Usage

1. Connect the MPU6050 IMU sensor to the Arduino Pro Micro following the provided pinout.

2. Upload the provided Arduino code to your Arduino board.

3. Run the Python code on your machine after installing the required libraries.

4. Adjust the color components of the 3D object by tilting the sensor to match the background color.

## Additional Notes

- Make sure to install the necessary Python libraries before running the Python code.

- Customize the Arduino code if using a different IMU sensor or microcontroller.

- Experiment with different difficulty levels and rollover times to enhance the gaming experience.

## Credits

This project utilizes the following open-source projects:

- [CarbonAeronautics: Part-XV-1DKalmanFilter](https://github.com/CarbonAeronautics/Part-XV-1DKalmanFilter)
- [MA-Lugo: PyIMU_3Dvisualizer](https://github.com/MA-Lugo/PyIMU_3Dvisualizer)

Make sure to check out the respective GitHub repositories for these projects and show your support to the original authors.

Enjoy the game!

