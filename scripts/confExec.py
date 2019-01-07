#! /usr/bin/env python

import rospy

from std_msgs.msg import String
import actionlib

from snav_msgs.msg import LandGoal
from snav_msgs.msg import LandAction
from snav_msgs.msg import TakeoffGoal
from snav_msgs.msg import TakeoffAction
from snav_msgs.msg import ExecuteMissionGoal
from snav_msgs.msg import ExecuteMissionAction

class confExec:
    def __init__(self):
        rospy.init_node("drone_confirmed_execution")
        self.currentCommand = ""
        self.prevCommand = ""
        self.execTime = 0.0
        self.prevExectime = 0.0
        self.currentServClient = None
        self.goal = None

        rospy.Subscriber("command", String, self.commandCB)
        self.respPub = rospy.Publisher("response", String, queue_size=10)
        rospy.spin()

    def commandCB(self, msg):
        self.currentCommand = msg.data.split(',')[0]
        if len(msg.data.split(',')) > 1:
            if int(msg.data.split(',')[1]) < 1546769553:
                self.execTime = int(msg.data.split(',')[1]) + rospy.get_rostime().secs
            else:
                self.execTime = int(msg.data.split(',')[1])
        print "Got command: " + str(self.currentCommand) + " at time: " + str(self.execTime)

        if self.execTime == self.prevExectime:
            return

        if self.prevCommand == "":
            if self.currentCommand == "Land":
                confMsg = String()
                confMsg.data = "Confirmed Land"
                self.respPub.publish(confMsg)
                self.prevCommand = self.currentCommand
                self.prevExectime = self.execTime
                self.initiateLand()

            if self.currentCommand == "Takeoff":
                confMsg = String()
                confMsg.data = "Confirmed Takeoff"
                self.respPub.publish(confMsg)
                self.prevCommand = self.currentCommand
                self.prevExectime = self.execTime
                self.initiateTakeoff()


            if self.currentCommand == "Execute":
                confMsg = String()
                confMsg.data = "Confirmed Execute"
                self.respPub.publish(confMsg)
                self.prevCommand = self.currentCommand
                self.prevExectime = self.execTime
                self.initiateExecTrajectory()

            if self.currentCommand == "Cancel":
                self.currentServClient.cancel_goal()


            if self.currentCommand == "Abort":
                self.sendAbort()

        # if (self.prevCommand == "Takeoff" or self.prevCommand == "Execute") and self.currentCommand == "Confirm":
        #     self.sendAction()
        #     self.prevCommand = ""


        return

    def initiateTakeoff(self):
        self.currentServClient = actionlib.SimpleActionClient("takeoff", TakeoffAction)
        self.goal = TakeoffGoal()
        self.prevCommand = ""
        self.sendAction()
        return

    def initiateLand(self):
        self.currentServClient = actionlib.SimpleActionClient("land", LandAction)
        self.goal = LandGoal()
        self.prevCommand = ""
        self.sendAction()
        return

    def initiateExecTrajectory(self):
        self.currentServClient = actionlib.SimpleActionClient("execute_mission", ExecuteMissionAction)
        self.goal = ExecuteMissionGoal()
        self.prevCommand = ""
        self.sendAction()
        return

    def sendAction(self):
        currTime = rospy.get_rostime().secs
        if abs(currTime - self.execTime) > 10:
            return
        while self.execTime > currTime:
            currTime = rospy.get_rostime().secs
        self.currentServClient.send_goal(self.goal)
        return

    def sendAbort(self):
        self.currentServClient.cancel_goal()
        return


ce = confExec()
