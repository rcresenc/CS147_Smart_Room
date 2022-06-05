# CS147_Smart_Room
CS 147 final project


Smart room adds more security and monoitorization to any given room. Using a photoresistor and a sound detector we are able to track how much light and the level of sound is present in the room. The information is stored and presented using a flask application located inside an AWS server which is designed in regards with the final project requirements. The flask application currently contains two main paths to display the incoming sensory information. First we have the '/home' page which displays the focused room's activity. It states the current light and sound qualitative levels which are present inside the room. The home page also displays a bar graph for the quantitative data that had been collected for the latest hour. The second main page is a data table containing all sensory data that is being collected. The data displays the time in which data is collected along with the analog values for both sound and light in which the sensors picked up. This page has the capabilities to manually store the displayed data to the cloud server by just a press of a button. The application is also designed to automatically save the data after a certain number of entries are collected. In addition to theese two paths we also include pathways in which display an analysis on past days in which the sensors had been running for. Any given page shows a bar graph containing the average amoount of sound and light that had been picked up each hour of the given day. 


How to run Flask App:

export FLASK_APP=room

python3 -m flask run --host=0.0.0.0
