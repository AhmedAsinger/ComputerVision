import cv2
import numpy as np
import time
import serial.threaded
import keyboard
import threading


def send_signal(signal):
    ser.write(signal.encode())


ser = serial.Serial('COM8', 9600)
time.sleep(5)

framewidth = 1080
frameheight = 720

# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('http://192.168.100.11:81/stream')
cap = cv2.VideoCapture('http://192.168.1.130:8080/video')

cap.set(3, framewidth)
cap.set(4, frameheight)


def empty(a):
    pass


# Track-back values
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 121, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 100, 255, empty)

# Global variables for keyboard events and shape detection
key_pressed = ''
shape_detected = False


# Thread to detect keyboard events
def keyboard_thread():
    global key_pressed

    while True:
        if keyboard.is_pressed('up'):
            key_pressed = 'U'
        elif keyboard.is_pressed('down'):
            key_pressed = 'D'
        elif keyboard.is_pressed('l'):
            key_pressed = 'L'
        else:
            key_pressed = ''
        time.sleep(0.1)  # Adjust sleep time as needed


# Send signal to Arduino for square
def send_square_signal():
    length1 = len(b'R')
    ser.write(length1.to_bytes(2, byteorder='big'))
    ser.write(b'R')
    ack = ser.readline().decode().strip()
    # Perform actions for square


# Send signal to Arduino for circle
def send_circle_signal():
    length2 = len(b'C')
    ser.write(length2.to_bytes(2, byteorder='big'))
    ser.write(b'C')
    ack = ser.readline().decode().strip()
    # Perform actions for circle


# Send signal to Arduino for triangle
def send_triangle_signal():
    length2 = len(b'T')
    ser.write(length2.to_bytes(2, byteorder='big'))
    ser.write(b'T')
    ack = ser.readline().decode().strip()
    # Perform actions for triangle


# Thread to perform object detection
def detection_thread():
    global shape_detected

    while True:
        success, img = cap.read()
        imgContour = img.copy()
        imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
        threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
        imgcanny = cv2.Canny(imgGray, threshold1, threshold2)
        kernel = np.ones((5, 5), np.uint8)
        imgdialation = cv2.dilate(imgcanny, kernel, iterations=1)
        getContours(imgdialation, imgContour)
        cv2.imshow('Object Detection', imgContour)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Perform contour detection and send signals
def getContours(img, imgContour):
    global key_pressed, shape_detected
    global key_pressed, shape_detected

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 25000 and not shape_detected:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print("Sides = ", len(approx))
            sides = int(len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.putText(imgContour, "Points : " + str(len(approx)), (100, 25), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area : " + str(int(area)), (100, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

            if sides == 4:
                print("Square...")
                threading.Thread(target=send_square_signal).start()
                shape_detected = True
                break
            elif sides == 8:
                print("Circle...")
                threading.Thread(target=send_circle_signal).start()
                shape_detected = True
                break
            elif sides > 9:
                print("No object detected yet")
            elif sides == 3:
                print("Triangle")
                threading.Thread(target=send_triangle_signal).start()
                shape_detected = True
                break

    if key_pressed == 'U':
        print("Open Gripper Fingers")
        send_signal('U')
    elif key_pressed == 'D':
        print("Close Gripper Fingers")
        send_signal('D')
    elif key_pressed == 'L':
        print("Stop Gripper Fingers")
        send_signal('L')


# Start the keyboard and detection threads
keyboard_thread = threading.Thread(target=keyboard_thread)
detection_thread = threading.Thread(target=detection_thread)

keyboard_thread.start()
detection_thread.start()

# Wait for the threads to finish (e.g., when 'q' key is pressed)
keyboard_thread.join()
detection_thread.join()

# Release the video capture, destroy the windows, and close the serial connection
cap.release()
cv2.destroyAllWindows()
ser.close()
