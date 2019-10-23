import sys
import rospy

from task_manager_common.skill_class import SkillSetup, SkillExecution, SkillAnalysis

class LocateObjectSkillSetup(SkillSetup):
    pass

class LocateObjectSkillExecution(SkillExecution):
    pass

class LocateObjectSkillAnalysis(SkillAnalysis):
    def set_outcomes(self, outcomes=None):
        return ['preempted', 'aborted', 'succeeded', "success", "failed"]
