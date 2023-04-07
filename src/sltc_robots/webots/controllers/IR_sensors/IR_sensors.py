import rospy
from controller import Robot, DistanceSensor
from std_msgs.msg import Int8MultiArray

class assistantRobot():
    def __init__(self):
        self.robot = Robot()

        self.time_step = int(self.robot.getBasicTimeStep())

        ### IR ###
        self.IR1 = self.robot.getDevice("IR1")    
        self.IR2 = self.robot.getDevice("IR2")  
        self.IR3 = self.robot.getDevice("IR3")  
        self.IR4 = self.robot.getDevice("IR4")  
        self.IR5 = self.robot.getDevice("IR5")  
        self.IR6 = self.robot.getDevice("IR6")  
        self.IR7 = self.robot.getDevice("IR7")  
        self.IR8 = self.robot.getDevice("IR8")    
        self.IR_sensors = [self.IR1, self.IR2, self.IR3, self.IR4, self.IR5, self.IR6, self.IR7, self.IR8]  
        for ir in self.IR_sensors:
            ir.enable(int(self.robot.getBasicTimeStep()))

        self.IR_values = [0, 0, 0, 0, 0, 0, 0, 0]
        self.IR_bool_values = [0, 0, 0, 0, 0, 0, 0, 0]
        self.IR_threshold = 300


        ### ROS ###
        rospy.init_node("IR_Sensor_array")

        self.IR_val = Int8MultiArray()

        self.IRPub = rospy.Publisher("IR_values_bool", Int8MultiArray, queue_size=10)
    
    def getIRreadings(self):
        for ir in range(8):
            self.IR_values[ir] = self.IR_sensors[ir].getValue()
        self.getIRboolreadings()
    
    def getIRboolreadings(self):
        for ir in range(8):
            self.IR_bool_values[ir] = int(self.IR_values[ir] < self.IR_threshold)
        self.IR_val.data = self.IR_bool_values
        self.IRPub.publish(self.IR_val)


if __name__ == "__main__":
    assistant_robot = assistantRobot()
    
    num_devices = assistant_robot.robot.getNumberOfDevices()

    while assistant_robot.robot.step(assistant_robot.time_step) != -1 and not rospy.is_shutdown():
        assistant_robot.getIRreadings()
        print(assistant_robot.IR_bool_values)
    
    