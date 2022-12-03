import rospy
import serial
import time
from std_msgs.msg import Int32

py_serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600,)

def callback(data):
    rospy.loginfo('I received %d', data.data)

    if(data.data==1):                                                        # !!!!!
            #command = "F"
            py_serial.write(data.data.encode())
            time.sleep(0.1)

    if(data.data==2):                                                        # !!!!!
            #command = "B"
            py_serial.write(data.data.encode())
            time.sleep(0.1)

    if(data.data==3):                                                        # !!!!!
            #command = "L"
            py_serial.write(data.data.encode())
            time.sleep(0.1)

    if(data.data==4):                                                        # !!!!!
            #command = "R"
            py_serial.write(data.data.encode())
            time.sleep(0.1)



def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('User/Hand', Int32, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
