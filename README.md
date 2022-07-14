# Objective:

- To print a 3D model based on free hand sketch that we draw
  on the android device.
- To create a braille text based on the text given on the android.

# Components used:

## Hardware

    - Anet 3D printer
    - Raspberry pi 4

## Software

    - Python3
    - Java

# Flow Chart

![Flow chart](https://github.com/mukesh2k/Backend-JSON/blob/master/Screenshot%20from%202022-07-14%2019-53-29.png?raw=true)

# Workflow

A dedicated android application [(3D Print Assist andoid App source code)](https://github.com/mukesh2k/3DPrinterAssist) is created to produce a appropriate transparent PNG based on our handsketch that is drawn on the mobile screen. For braille frame text is taken as the input by the app. Once the input (either handsketch or braille) is taken it is sent to the raspberrypi via FTP. Mobile must be connected to the WIFI access point provided by the raspberry pi.

Once the file is received it is converted to appropirate PNG. For braille the text as converted to the respective braille letters and placed on transparent empty PNG with required amount of spacing and line breaks.

The PNG file needs to be converted to STL file which is the 3D model file, for this we will be taking the color information from the PNG images and determine the height of the 3D model in each coordinate points.

Once STL is produced, it needs to be converted to the GCODE. Gcode is a machinary language the the 3D printer can understand. This process is done with the help of slicers. We have used prusaslicer to do this process.

The produced Gcodes are sent to printer via USB (/dev/ttyUSB0). Serial module along with multithreading is used to send the gcode to the machine.

For developing android application Java language is used.
For image processing in raspberrypi 4 Python language is used.

# Results

## Braille and handsketch

![input and output](https://github.com/mukesh2k/Backend-JSON/blob/master/Screenshot%20from%202022-07-14%2019-55-07.png?raw=true)

## Input

![Input](https://raw.githubusercontent.com/mukesh2k/Backend-JSON/master/1656570531_90_1.png)

## Output

![Output](https://github.com/mukesh2k/Backend-JSON/blob/master/IMG-20220630-WA0012.jpg?raw=true)

## [3Dprinter printing video](https://youtu.be/bLeWTOQuhFA)

# Detailed report

[Report PDF](https://drive.google.com/file/d/1gkfGjXBpk6l-GH2g6b9c9cZxtUGMpUc1/view?usp=sharing) Click this to view the report pdf
