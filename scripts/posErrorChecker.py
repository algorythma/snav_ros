#! /usr/bin/env python

import rospy
import actionlib

from geometry_msgs.msg import PoseStamped as ps
from snav_msgs.msg import LandAction
from snav_msgs.msg import LandGoal

class posErrorChecker:
    def __init__(self):
        rospy.init_node("posErrorChecker")
        rospy.Subscriber("pose", ps, self.poseCB)
        rospy.Subscriber("desired_pose", ps, self.desiredPoseCB)

        self.landAction = actionlib.SimpleActionClient("land", LandAction)

        self.desPose = ps()
        self.curPose = ps()

        self.xCntr = 0
        self.yCntr = 0
        self.zCntr = 0

        self.currErrorX = 0.0
        self.prevErrorX = 0.0

        self.currErrorY = 0.0
        self.prevErrorY = 0.0

        self.currErrorZ = 0.0
        self.prevErrorZ = 0.0

        self.maxCntr = 200
        self.maxEmCntr = 2 * self.maxCntr

        self.landSent = 0

        rospy.spin()

    def poseCB(self, msg):
        self.currErrorX = self.desPose.pose.position.x - self.curPose.pose.position.x
        self.currErrorY = self.desPose.pose.position.y - self.curPose.pose.position.y
        self.currErrorZ = self.desPose.pose.position.z - self.curPose.pose.position.z

        if (abs(self.currErrorX) > abs(self.prevErrorX)):
            self.xCntr += 1
        else:
            self.xCntr = 0
            self.landSent = 0
        if  (abs(self.currErrorY) > abs(self.prevErrorY)):
            self.yCntr += 1
        else:
            self.yCntr = 0
            self.landSent = 0
        if (abs(self.currErrorZ) > abs(self.prevErrorZ)):
            self.zCntr += 1
        else:
            self.zCntr = 0
            self.landSent = 0

        if self.xCntr > self.maxCntr:
            print "X Error is increasing"
        if self.yCntr > self.maxCntr:
            print "Y Error is increasing"
        if self.zCntr > self.maxCntr:
            print "Z Error is increasing"

        if self.xCntr > self.maxEmCntr:
            print "Land becasue of x error increase"
            if self.landSent < 2:
                self.landAction.send_goal(LandGoal())
                self.landSent += 1
        if self.yCntr > self.maxEmCntr and self.landSent < 2:
            print "Land becasue of y error increase"
            if self.landSent < 2:
                self.landAction.send_goal(LandGoal())
                self.landSent += 1
        if self.zCntr > self.maxEmCntr and self.landSent < 2:
            print "Land becasue of z error increase"
            if self.landSent < 2:
                self.landAction.send_goal(LandGoal())
                self.landSent += 1

        self.prevErrorX = self.currErrorX
        self.prevErrorY = self.currErrorY
        self.prevErrorZ = self.currErrorZ
        return

    def desiredPoseCB(self, msg):
        self.desPose = msg
        return