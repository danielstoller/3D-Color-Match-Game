# 3D Color Match

This project involves creating a 3D color matching game using an MPU6050 IMU sensor with Arduino for real-time input and PyOpenGL, PyGame, and Tkinter in Python for visualization. The game requires players to match the color of a 3D model of the IMU with the background color by adjusting the color components using tilt inputs from the IMU sensor.

[![Watch the Video](https://img.youtube.com/vi/dbV-Rf0EUzg/0.jpg)](https://youtu.be/dbV-Rf0EUzg)


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

5. There are 6 different modes:
      1. Pitch and Roll: Don't click on a difficulty to see real time pitch and roll angles
      2. Tutorial: Learn how to play the game
      3. Closeness: Given how far away the player is from the correct color
      4. Normal: No help given and can't lose
      5. Timer: Player has to finish a color within the given amount of time. Extra time rolls over to the next round
      6. Limited Moves and Timer: Player only has a certain number of moves to find the correct color. Timer does not roll over to the next round

## Additional Notes

- Customize the Arduino code if using a different IMU sensor.
  
- Serial outputs must have the structure "$roll/pitch"
  
- Do not have Serial Moniter open when running the Python code.

- Make sure to install the necessary Python libraries before running the Python code.

- Experiment with different values under the comment "####ADJUSTABLE####" to enhance the gaming experience.

## Credits

This project utilizes the following open-source projects:

- CarbonAeronautics: [Part-XV-1DKalmanFilter](https://github.com/CarbonAeronautics/Part-XV-1DKalmanFilter)
- MA-Lugo: [PyIMU_3Dvisualizer](https://github.com/MA-Lugo/PyIMU_3Dvisualizer)

Make sure to check out their respective GitHub repositories for these projects and show your support to the original authors.

Enjoy the game!

