###########
# READ ME #
###########

IMPORTANT NOTES: 


Code.py
==========
Main file where server is run. This is where the ESP32 connects to the Wifi network and binds to the TCP protocol. 
Parsing of HTML requests and distribution of HTML files done here. 

Index.html
============
This is the homepage where you can access all other webpages and functions. 

Health.html
==========
Webpage that contains the code to display sensor readings. The webpage has a javascript script that periodically updates 
values from database and refreshes html webpage of the client. 

Water.html
==========
Webpage that contains the code to display water readings and interface to control watering system. There is a selection
bar that allows the user to preset a water level to water. Then a button that once pressed will send an html request with 
selected water level. The button will respond with feedback on sucess of request. 

Light.html
==========
Webpage that contains the code to display light readings and interface to control lighting system. 
On the page the current light level is displayed and two buttons for on and off as well. When one of the
buttons is pressed it sends a request to either turn on or off the light. 

Settings.html
==========
Webpage that contains the code to display settings GUI and interface to control settings for the system, sensors, and notifications.

