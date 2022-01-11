# team-project-fetele-cochetele
team-project-fetele-cochetele created by GitHub Classroom

# Human proximity detection

The Android Things human proximity detection will detect the presence of other human within the field of vision of the camera and will notify by sound the user if a set distance is reached

# Demo

![ezgif com-gif-maker](https://user-images.githubusercontent.com/57748364/114662210-f7547400-9d00-11eb-899d-6af36481f628.gif)

[(See our demo on youtube)][demo-yt]



[demo-yt]: https://www.youtube.com/watch?v=0lkIRkQS8oY

[Demo - human proximity detection.zip](https://github.com/at-cs-ubbcluj-ro/team-project-fetele-cochetele/files/6350579/Demo.-.human.proximity.detection.zip)


# Schematics

![aaaaaaaaaaaaaaaaaaaaaaaaaaaa_bb](https://user-images.githubusercontent.com/41358240/115546208-6a378f00-a2ad-11eb-8fe7-a5dd1199bc8e.png)

# Pre-requisites

- Raspberry Pi compatible board
- Breadboard 830p
- 1 x passive buzzer
- Diode
- Transistor
- 1 x 1000Ω resistor
- 6 x male-to-male jumper wires
- 5 x female-to-male jumper wires
- Ultrasonic module HC-SR04+
- USB camera

# Setup and Build

1. Assemble components according to schematics above
2. Connect a USB camera to the Raspberry Pi
3. Install the necessary libraries for python

# Running

1. Run the command "sudo pigpiod"
2. Run the buzzbuzz.py server
3. Compile and run the mobile application to send the starting signal or send a post request to the "/start" endpoint
