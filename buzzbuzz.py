import numpy as np
import cv2
import flask
#import the libraries used
import time
import pigpio
import os
import RPi.GPIO as GPIO
GPIO.cleanup()

app = flask.Flask(__name__)
app.config["DEBUG"]=True

#create an instance of the pigpio library
pi = pigpio.pi()

#define the pin used by the Buzzer
#this pin will be used by the pigpio library
#which takes the pins in GPIO forms
#we will use GPIO18, which is pin 12
buzzer = 18

#set the pin used by the buzzer as OUTPUT
pi.set_mode(buzzer, pigpio.OUTPUT)

GPIO.setmode(GPIO.BOARD)

#define the pins used by the ultrasonic module
trig = 11
echo = 13

#set the trigger pin as OUTPUT and the echo as INPUT
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

def calculate_distance():
    #set the trigger to HIGH
    GPIO.output(trig, GPIO.HIGH)

    #sleep 0.00001 s and the set the trigger to LOW
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    #save the start and stop times
    start = time.time()
    stop = time.time()

    #modify the start time to be the last time until
    #the echo becomes HIGH
    while GPIO.input(echo) == 0:
        start = time.time()

    #modify the stop time to be the last time until
    #the echo becomes LOW
    while  GPIO.input(echo) == 1:
        stop = time.time()

    #get the duration of the echo pin as HIGH
    duration = stop - start

    #calculate the distance
    distance = 34300/2 * duration

    if distance < 0.5 and distance > 400:
        return 0
    else:
        #return the distance
        print(distance)
        return distance

@app.route('/start',methods=['POST'])
def start():
    try:
        pi.hardware_PWM(buzzer, 500, 500000)
        time.sleep(0.05)

        #turn off the buzzer and wait 50 ms
        pi.hardware_PWM(buzzer, 0, 0)
        time.sleep(0.05)
                    
        cv2.startWindowThread()
        cap = cv2.VideoCapture(1)
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        while True:
            ret, frame = cap.read()
            
            if calculate_distance() < 25:
                frame2 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                # apply threshold. all pixels with a level larger than 80 are shown in white. the others are shown in black:
                ret,frame2 = cv2.threshold(frame2,80,255,cv2.THRESH_BINARY)
            
                #turn on the buzzer at a frequency of
                #500Hz for 50 ms
                print("Distance less than 25")
                
                boxes, weights = hog.detectMultiScale(frame2, winStride =(8,8))
                
                #for(xA, yA, xB, yB)in boxes:
                 #   cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                
                if len(boxes) > 0:
                    pi.hardware_PWM(buzzer, 500, 500000)
                    time.sleep(0.05)

                    #turn off the buzzer and wait 50 ms
                    pi.hardware_PWM(buzzer, 0, 0)
                    time.sleep(0.05)

            else:
                print("Distance mode than 25")
                #turn off the buzzer
                pi.hardware_PWM(buzzer, 0, 0)
            
            #cv2.imshow('frame', frame)
            
            #wait 100 ms before the next run
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        #turn off the buzzer
        pi.write(buzzer, 0)
        #stop the connection with the daemon
        pi.stop()


if __name__=="__main__":
    app.run(host=os.getenv('IP','0.0.0.0'), port=int(os.getenv('PORT', 80)))

GPIO.cleanup()        
