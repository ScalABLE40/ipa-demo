#!/usr/bin/env python

import rospy
import traceback
from move_to_skill_class import MoveToSkill


if __name__ == "__main__":

    rospy.init_node('move_to_skill')

    try:
        actionName = rospy.get_param('~action_name')
    except Exception as e:
        raise KeyError('Unable to access ROS parameter server for ' + str(actionName))

    try:
        MoveToSkill = MoveToSkill(actionName)
        rospy.spin()

    except Exception as e:
        rospy.logerr('[MoveToSkill] Error: %s', str(e))
        rospy.logdebug(traceback.format_exc())
        quit()
