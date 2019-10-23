import sys
import rospy

from task_manager_common.skill_class import SkillSetup, SkillExecution, SkillAnalysis

class MoveToSkillSetup(SkillSetup):
    pass

class MoveToSkillExecution(SkillExecution):
    pass

class MoveToSkillAnalysis(SkillAnalysis):
    def set_outcomes(self, outcomes=None):
        return ['preempted', 'aborted', 'succeeded', "success", "failed"]
