import rospy
import serial
import time
from std_msgs.msg import Int32

py_serial = serial.Serial(port='/dev/ttyUSB0', baudrate=9600,)
command = "Z"

def callbackSpeed(data):
    global Speed_command

    if(data.data<=60):                                                        # !!!!!
        Speed_command = "A"
        py_serial.write(Speed_command.encode())

    elif(data.data<=80):                                                        # !!!!!
        Speed_command = "B"
        py_serial.write(Speed_command.encode())
    else:                                                        # !!!!!
        Speed_command = "C"    
        py_serial.write(Speed_command.encode())
    
    rospy.loginfo('I received Speed: %d', data.data)


def callbackAngle(data):
    Angle_command = "Z"

    if(data.data<=-15 and Speed_command == "A"):             #left, low                             # !!!!!
        Angle_command = "D"
        py_serial.write(Angle_command.encode())
    elif(data.data<=-15 and Speed_command == "B"):           #left, mid                                          
        Angle_command = "E"
        py_serial.write(Angle_command.encode())
    elif(data.data<=-15 and Speed_command == "C"):           #left, fast                                             
        Angle_command = "F"
        py_serial.write(Angle_command.encode())
    elif(data.data>15 and Speed_command == "A"):             #right, low                                          
        Angle_command = "G"
        py_serial.write(Angle_command.encode())
    elif(data.data>15 and Speed_command == "B"):             #right, mid                                          
        Angle_command = "H"
        py_serial.write(Angle_command.encode())
    elif(data.data>15 and Speed_command == "C"):             #right, fast                                         
        Angle_command = "I"
        py_serial.write(Angle_command.encode())
    elif(Speed_command == "A"):                              #forward, low                                     
        Angle_command = "J"
        py_serial.write(Angle_command.encode())
    elif(Speed_command == "B"):                              #forward, mid                         
        Angle_command = "K"
        py_serial.write(Angle_command.encode())
    else:                                                    #forward, fast
        Angle_command = "L"
        py_serial.write(Angle_command.encode())                                                      # !!!!!

    rospy.loginfo('I received Angle: %d', data.data)
        
    rospy.loginfo('I send Angle message to Arduino Angle: %s', Angle_command)

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('User/Hand_Speed', Int32, callbackSpeed)
    rospy.Subscriber('User/Hand_Angle', Int32, callbackAngle)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
