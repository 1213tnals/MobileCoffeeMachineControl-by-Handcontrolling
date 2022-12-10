import rospy
import serial
import time
from std_msgs.msg import Int32                               #I used ros topic type Int32

py_serial = serial.Serial(port='/dev/ttyUSB0', baudrate=9600,)     #connect to arduino(this baudrate is for arduino mega)
command = "Z"


#Ros topic callback funtion for speed data 
def callbackSpeed(data):                                     
    global Speed_command

    if(data.data<=60):                                                   
        Speed_command = "A"
    elif(data.data<=80):                                                      
        Speed_command = "B"
    else:                                                    
        Speed_command = "C"    


#Ros topic callback funtion for angle data
def callbackAngle(data):                                     
    global Angle_command

    if(data.data<=-15 and Speed_command == "A"):             #left, low                            
        Angle_command = "D"
    elif(data.data<=-15 and Speed_command == "B"):           #left, mid                                          
        Angle_command = "E"
    elif(data.data<=-15 and Speed_command == "C"):           #left, fast                                             
        Angle_command = "F"
    elif(data.data>15 and Speed_command == "A"):             #right, low                                          
        Angle_command = "G"
    elif(data.data>15 and Speed_command == "B"):             #right, mid                                          
        Angle_command = "H"
    elif(data.data>15 and Speed_command == "C"):             #right, fast                                         
        Angle_command = "I"
    elif(Speed_command == "A"):                              #forward, low                                     
        Angle_command = "J"
    elif(Speed_command == "B"):                              #forward, mid                         
        Angle_command = "K"
    else:                                                    #forward, fast
        Angle_command = "L"

    #rospy.loginfo('I received Angle: %d', data.data)


#Ros topic callback funtion for mode data. And result command send to arduino by Serial
def callbackMode(data):                                      
    Mode_command = "Z"

    if(data.data == 0):                                       
        Mode_command = "S"                                   #stop
        py_serial.write(Mode_command.encode())
    elif(data.data == 5):                                                    
        Mode_command = "R"                                   #run
        py_serial.write(Mode_command.encode())
    elif(data.data == 10):
        Mode_command = "A"                                   #coffee make
        py_serial.write(Mode_command.encode())
    
    else:
        if(Angle_command == "D"):                               
            Mode_command = "D"
            py_serial.write(Mode_command.encode())
        elif(Angle_command == "E"):             
            Mode_command = "E"
            py_serial.write(Mode_command.encode())
        elif(Angle_command == "F"):             
            Mode_command = "F"
            py_serial.write(Mode_command.encode())
        elif(Angle_command == "G"):             
            Mode_command = "G"
            py_serial.write(Mode_command.encode())
        elif(Angle_command == "H"):             
            Mode_command = "H"
            py_serial.write(Mode_command.encode())
        elif(Angle_command == "I"):             
            Mode_command = "I"
            py_serial.write(Mode_command.encode())
        elif(Angle_command == "J"):             
            Mode_command = "J"
            py_serial.write(Mode_command.encode())
        elif(Angle_command == "K"):             
            Mode_command = "K"
            py_serial.write(Mode_command.encode())
        elif(Angle_command == "L"):             
            Mode_command = "L"
            py_serial.write(Mode_command.encode())


    rospy.loginfo('I send message to Arduino: %c', Mode_command)


#Ros topic Subscribing part function
def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('User/Hand_Speed', Int32, callbackSpeed)
    rospy.Subscriber('User/Hand_Angle', Int32, callbackAngle)
    rospy.Subscriber('User/Hand_Mode', Int32, callbackMode)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()