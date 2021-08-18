import os, sys

import cv2, Leap, math, ctypes
import numpy as np
import time
from datetime import datetime, date
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

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

FINGER_TYPES = {0 : 'THUMB', 1 : 'INDEX', 2 : 'MIDDLE', 3 : 'RING', 4 : 'PINKY'}
BONE_TYPES = {0 : 'TYPE_METACARPAL ', 1 : 'TYPE_PROXIMAL ', 2 : 'TYPE_INTERMEDIATE ', 3 : 'TYPE_DISTAL'}

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
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                for hand in frame.hands:
                    handType = "Left Hand" if hand.is_left else "Right hand"
                    pltClr = 'blue' if hand.is_left else 'red'
                    ax.plot(hand.palm_position.x, hand.palm_position.y, hand.palm_position.z, marker='o', color=pltClr)
                    f.write(handType + "Hand ID: " + str(hand.id) + "\n")
                    printXYZ(f, "Palm Position: ", hand.palm_position)
                    printXYZ(f, "Palm Direction: ", hand.direction)

                    f.write("Pitch: " + str(hand.direction.pitch) + "\n")
                    f.write("Yaw: " + str(hand.direction.yaw) + "\n")
                    f.write("Roll: " + str(hand.direction.roll) + "\n")
                    f.write("\n")
                    fingers = hand.fingers
                    for finger in fingers:
                        if finger.is_valid:
                            f.write("Finger Type: " + FINGER_TYPES[finger.type] + "\n")
                            for i in range(0, 4):
                                bone = finger.bone(i)
                                bone_start = bone.prev_joint
                                bone_end = bone.next_joint

                f.close()
                plt.show()
                if cv2.waitKey(10000) == ord('q'):
                    plt.close()
                cv2.destroyAllWindows()
                break

def printXYZ(file, descr, position):
    file.write( descr + \
    "x: " + str(position.x) + \
    "y: " + str(position.y) + \
    "z: " + str(position.z) + \
    "\n")


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