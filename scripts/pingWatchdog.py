#! /usr/bin/env python

import  os

import rospy
import actionlib
from snav_msgs.msg import LandAction
from snav_msgs.msg import LandGoal

class landChecker:
    def __init__(self):
        rospy.init_node("watchdog", anonymous=True)
        self.hostName = "KL-29"
        self.toCnt = 0
        self.maxTo = 2
        self.sentLand = 0

        self.landClient = actionlib.SimpleActionClient("land", LandAction)

        self.run()

    def run(self):
        while not rospy.is_shutdown():
            resp = os.system("ping -c 1 " + self.hostName + " > /dev/null 2>&1")
            if resp == 0:
                self.toCnt = 0
                self.sentLand = 0
            else:
                self.toCnt += 1

            if self.toCnt >= self.maxTo:
                #print "Lost connection"
                if self.sentLand < 2:
                    self.sentLand += 1
                    self.initiateLand()

    def initiateLand(self):
        print "Sending land"
        self.landClient.send_goal(LandGoal())
        return


lc = landChecker()