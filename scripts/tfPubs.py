import rospy
import tf
from geometry_msgs.msg import PoseStamped as ps

class swarmtfPubs:
    def __init__(self):
        rospy.init_node("swarmTF_")
        self.poseSub = rospy.Subscriber("pose", ps, self.poseCB)
        ns = rospy.get_namespace()
        self.drName = ns + "base_link"
        self.odom   = ns + "odom"
        rospy.spin()

    def poseCB(self, msg):
        tfBR = tf.TransformBroadcaster()
        tfBR.sendTransform((msg.pose.position.x, msg.pose.position.y, msg.pose.position.z),
                           (msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w),
                         rospy.Time.now(),
                         self.drName,
                         self.odom
                         )

s = swarmtfPubs()