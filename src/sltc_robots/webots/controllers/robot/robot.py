import rospy
from controller import Robot
from std_msgs.msg import String
class assistantRobot():
    def __init__(self):
        self.robot = Robot()

        self.time_step = int(self.robot.getBasicTimeStep())

        ### motors ###
        self.left_motor = self.robot.getDevice('left wheel motor')
        self.right_motor = self.robot.getDevice('right wheel motor')
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))

        self.left_speed = 3.0
        self.right_speed = 3.0

        ### ROS ###
        rospy.init_node("motors")
        self.velPub = rospy.Subscriber("cmd_vel", String, self.setSpeed)
    
    def setSpeed(self, msg):
        self.left_speed, self.right_speed = list(map(int, msg.data.split(',')))
    
    def robot_vel(self):
        self.left_motor.setVelocity(self.left_speed)
        self.right_motor.setVelocity(self.right_speed)


if __name__ == "__main__":
    assistant_robot = assistantRobot()
    
    while assistant_robot.robot.step(assistant_robot.time_step) != -1:
        assistant_robot.robot_vel()
    
    