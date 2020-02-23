import Leap, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import time
from datetime import datetime, date

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
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

            for finger in hand.fingers:
                print('Type: ' + self.finger_names[finger.type] + " ID: " + str(finger.id) \
                + ' Length: ' + str(finger.length) + ' Width: ' + str(finger.width))
                for b in range(0, 4):
                    bone = finger.bone(b)
                    print('Bone name: ' + self.bone_names[bone.type] + ' Start:' + str(bone.prev_joint) + ' End: ' + str(bone.next_joint) \
                    + ' Direction: ' + str(bone.direction))

f = 0

def main():
    # Create a sample listener and controller

    listener = SampleListener()
    controller = Leap.Controller()

    # Keep this process running until Enter is pressed
    while True:
        fileName = input('Введите имчя файла: ')
        fileDate = datetime.strftime(datetime.now(), "%Y%m%d %H%M%S")
        global f
        f = open(fileName + ' ' + fileDate + '.txt', 'w') # открываем для записи (writing)
        controller.add_listener(listener)
        try:
            input('')
        except KeyboardInterrupt:
            pass
        finally:
        # Remove the sample listener when done
            controller.remove_listener(listener)
            print('GG')
            f.close()


if __name__ == "__main__":
    main()
