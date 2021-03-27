import os, sys

import cv2, Leap, math, ctypes
import numpy as np
import time
from datetime import datetime, date\

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

def run(controller):
    fileName = input('Введите имя файла: ')
    fileDate = datetime.strftime(datetime.now(), "%Y%m%d %H%M%S")
    while(True):
        frame = controller.frame()
        if frame.images[0].is_valid and frame.images[1].is_valid:
            #display images
            image1 = make_npimage(frame.images[0])
            image2 = make_npimage(frame.images[1])
            cv2.imshow('Left Camera', image1)
            cv2.imshow('Right Camera', image2)
            if cv2.waitKey(1) == ord('a'):
                imageDestL = 'C:/prgprojects/' + fileName + fileDate + '_L' + '.jpg'
                imageDestR = 'C:/prgprojects/' + fileName + fileDate + '_R' + '.jpg'
                cv2.imwrite(imageDestL, image1)
                cv2.imwrite(imageDestR, image2)
                f = open(fileName + ' ' + fileDate + '.txt', 'w')
                for hand in frame.hands:
                    handType = "Left Hand" if hand.is_left else "Right hand"
                    f.write(handType + "Hand ID: " + str(hand.id) + "\n")
                    f.write(" Palm Position: " + str(hand.palm_position) + "\n")
                    f.write("Direction: " + hand.palm_direction + "\n")
                    f.write("Pitch: " + hand.direction.pitch + "\n")
                    f.write("Yaw: " + hand.direction.yaw + "\n")
                    f.write("Roll: " + hand.direction.roll + "\n")
                    f.write("\n")
                f.close()
                cv2.destroyAllWindows()
                break


def main():
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)
    while(True):
        try:
            run(controller)
        except KeyboardInterrupt:
            sys.exit(0)
    print("Exit")
if __name__ == '__main__':
    main()