# ESP32-CAM_thermometer
Using an ESP32-CAM to monitor a liquid thermometer

Accompanying [YouTube video](https://youtu.be/_NWB49mpcyM)

This video describes how to set up an ESP32-CAM  to record the temperature of a glass thermometer. Images from the ESP32 video stream over a wifi and processed using Python OpenCV. 

The original project used a ESP32 development board and an OV5624 camera shield (https://youtu.be/TBst0CGrtAo) but image acquisition was much more reliable using an ESP32-CAM, shown here.

For analysis, the received image of the thermometer is processed using the Python OpenCV package, using the following steps. 

1. A mask made which contains only pixels that are the same (or close to) the color of the thermometer liquid. 
2. The mask image is processed so that the regions which contain pixels are expanded.  This fills small gaps in thermometer liquid region so that a continuous area of pixels is created.
3. Areas containing pixels are identified, and those of the correct area are measured. A size threshold is filter out small areas. The size of the remaing rectangles encompassing  the thermometer liquid is used to determine the temperature, following a calibration based on pixel locations of defined temperatures from a regular image.

The ESP32-CAM is an Aideepen ESP32-CAM: https://www.amazon.com/gp/product/B08P2578LV
