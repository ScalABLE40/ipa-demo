#!/usr/bin/env python

import rospy
import traceback
from locate_object_skill_class import LocateObjectSkill


if __name__ == "__main__":

    rospy.init_node('locate_object_skill')

    try:
        actionName = rospy.get_param('~action_name')
    except Exception as e:
        raise KeyError('Unable to access ROS parameter server for ' + str(actionName))

    try:
        LocateObjectSkill = LocateObjectSkill(actionName)
        rospy.spin()

    except Exception as e:
        rospy.logerr('[LocateObjectSkill] Error: %s', str(e))
        rospy.logdebug(traceback.format_exc())
        quit()
