import sys
import rospy

from task_manager_common.skill_class import SkillSetup, SkillExecution, SkillAnalysis

class OperateGripperSkillSetup(SkillSetup):
    pass

class OperateGripperSkillExecution(SkillExecution):
    pass

class OperateGripperSkillAnalysis(SkillAnalysis):
    def set_outcomes(self, outcomes=None):
        return ['preempted', 'aborted', 'succeeded', "success", "failed"]
