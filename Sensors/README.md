This is a README for the sensors subsytem of our Project
Author: Harsh Ajwani
Last Updated: 02/22/2023

The sensors.py file contains all the code for this subsystem. All other files are test scripts. All pin numbers are for testing purposes and subject to change.

The plantheight() function is triggered by the micro controller to check if the plant is too close to the grow lights. The function will use the a ultrasonic sensor to detect the distance of the plant from the lights. If the distance is less than 3 inches, it will return true so the Microcontroller can notify the user that the height of the grow lights need to be increased.

The waterlevel() function is used continuously to see the water level in the tank. A second ultrasonic sensor will be used to do this. First, we will measure the initial distance before the tank is filled. This value will be defined as a constant. Next, we will measure the distance of the water from the sensor. The difference in these two values will be the water level in the tank and returned to the Microcontroller. 

The soilmoisturelevel() function is used to continuosuly check the moisture level of the soil. This will be done using the STEMMA Soil Sensor. We will initially check water and air moisture levels that are defined as constants on top. The sensor will measure the moisture level in Raw Capacitance Units. We will use the constants to change this to Volumetric Water Content, the ratio of the volume of water to the unit volume of soil. This will allow the Microcontroller to trigger the pump if soil moisture is low. 

The airtemperature() function is used to continuously check the air temperature around the plant. This will also be done using the STEMMA Soil Sensor. This will allow the Microcontroller to turn off the grow lights incase of overheating and also allow us to make sure the environment is suitable for plant growth.