This is a README for the sensors subsytem of our Project
Author: Harsh Ajwani
Last Updated: 02/17/2023

The sensors.py file contains all the code for this subsystem. All other files are test scripts

The plantheight() function is triggered by the micro controller to check if the plant is too close to the grow lights. The function will use the a ultrasonic sensor to detect the distance of the plant from the lights. If the distance is less than 3 inches, it will return true so the Microcontroller can notify the user that the height of the grow lights need to be increased.

The waterlevel() function is used continuously to see the water level in the tank. A second ultrasonic sensor will be used to do this. First, we will measure the initial distance before the tank is filled. This value will be defined as a constant. Next, we will measure the distance of the water from the sensor. The difference in these two values will be the water level in the tank and returned to the Microcontroller. 