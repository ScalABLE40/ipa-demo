#!/usr/bin/env python

import rospy
import traceback
from operate_gripper_skill_class import OperateGripperSkill


if __name__ == "__main__":

    rospy.init_node('operate_gripper_skill')

    try:
        actionName = rospy.get_param('~action_name')
    except Exception as e:
        raise KeyError('Unable to access ROS parameter server for ' + str(actionName))

    try:
        OperateGripperSkill = OperateGripperSkill(actionName)
        rospy.spin()

    except Exception as e:
        rospy.logerr('[OperateGripperSkill] Error: %s', str(e))
        rospy.logdebug(traceback.format_exc())
        quit()
