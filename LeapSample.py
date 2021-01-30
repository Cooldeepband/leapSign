import Leap, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import time
from datetime import datetime, date
import cv2, Leap, math, ctypes
import numpy as np

counter = 0

def make_npimage(image):
    #wrap image data in numpy array
    i_address = int(image.data_pointer)
    ctype_array_def = ctypes.c_ubyte * image.height * image.width
    # as ctypes array
    as_ctype_array = ctype_array_def.from_address(i_address)
    # as numpy array
    as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
    img = np.reshape(as_numpy_array, (image.height, image.width))
    
    return img


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    keyPressed = False
    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        image_list = Leap.ImageList()
        image_list = controller.images
        left_image = image_list[0]
        right_image = image_list[1]
        if not image_list.is_empty:
            if self.keyPressed:
                keyPressed = False
                print("Valid!")
        for hand in frame.hands:
            handType = "Left Hand" if hand.is_left else "Right hand"
            timer = int(round(time.time() * 1000))
            f.write(handType + "Hand ID " + str(hand.id) + " Palm Position " + str(hand.palm_position) + str(timer) + "\n")
            #print(handType + "Hand ID " + str(hand.id) + " Palm Position " + str(hand.palm_position))

            normal = hand.palm_normal
            direction = hand.direction

            #print("Pitch " + str(direction.pitch * Leap.RAD_TO_DEG))
            arm = hand.arm
           # print("Arm Direction: " + str(arm.direction) + " Wrist position: " \
           # + str(arm.wrist_position) + " Elbow Position: " + str(arm.elbow_position))
    def on_images(self, controller):
        print( "Images available")
        images = controller.images
        left_image = images[0]
        right_image = images[1]
    def keyboardInt(self):
        keyPressed = True
    def imgFinished(self):
        return self.keyPressed

f = 0

def main():
    # Create a sample listener and controller

    listener = SampleListener()
    controller = Leap.Controller()
    config2 = controller.config
    #controller.set_policy(Leap.Controller.POLICY_DEFAULT)
    controller.set_policy(Leap.Controller.POLICY_IMAGES)

    # Keep this process running until Enter is pressed
    while True:
        fileName = input('Введите имчя файла: ')
        fileDate = datetime.strftime(datetime.now(), "%Y%m%d %H%M%S")
        global f
        f = open(fileName + ' ' + fileDate + '.txt', 'w') # открываем для записи (writing)
        controller.add_listener(listener)
        try:
            a = input()
        except KeyboardInterrupt:
            pass
        finally:
        # Remove the sample listener when done
            print(a)
            listener.keyboardInt()
            flag = listener.imgFinished()
            while not flag:
                flag = listener.imgFinished()
            controller.remove_listener(listener)
            print('GG')
            f.close()

if __name__ == "__main__":
    main()
