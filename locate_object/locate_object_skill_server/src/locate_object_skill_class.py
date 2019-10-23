import rospy
import actionlib

from locate_object_skill_msgs.msg import LocateObjectSkillAction, LocateObjectSkillResult, LocateObjectSkillFeedback

class LocateObjectSkill(object):

    def __init__(self, action_name='LocateObjectSkill'):

        self.action_name = action_name
        self.locate_object_skill_server = actionlib.SimpleActionServer(self.action_name, LocateObjectSkillAction, self.execute_skill, False)
        self.locate_object_skill_server.start()
        self.percentage = 0
        self.outcomes = ["success", "failed"]

    def execute_skill(self, goal):
        '''
        The execution of the skill should be coded here.
        In order to save you time, the methods check_preemption(), feedback(), success() and aborted() should be used.
        The check_preemption() method should be called periodically.
        The variable self.percentage should be updated when there is an evolution in the execution of the skill.
        feedback() method should be called when there is an evolution in the execution of the skill.
        '''
        pass

    def feedback(self, status=None):
        feedback = LocateObjectSkillFeedback()
        feedback.percentage = self.percentage
        feedback.skillStatus = status if status else 'LocateObjectSkill Executing'
        self.locate_object_skill_server.publish_feedback(feedback)
        self.log_info(feedback)

    def success(self, status=None, outcome='succeeded'):
        result_status = status if status else 'LocateObjectSkill executed successfully'
        result = self.result_constructor(percentage=100, status=result_status, outcome=outcome)
        self.locate_object_skill_server.set_succeeded(result, result.skillStatus)

    def aborted(self, status=None, outcome='aborted'):
        result_status = status if status else 'LocateObjectSkill aborted'
        result = self.result_constructor(status=result_status, outcome=outcome)
        self.locate_object_skill_server.set_aborted(result, result.skillStatus)

    def check_preemption(self):
        if self.locate_object_skill_server.is_preempt_requested():
            result = self.result_constructor(status='LocateObjectSkill Preempted', outcome='preempted')
            self.locate_object_skill_server.set_preempted(result, result.skillStatus)
            return

    def result_constructor(self, status, percentage=None, outcome=None):
        result = LocateObjectSkillResult()
        result.percentage = percentage if percentage else self.percentage
        result.skillStatus = status
        result.outcome = outcome
        self.log_info(result)
        return result

    @staticmethod
    def log_info(status):
        info = '[LocateObjectSkill] Percentage: ' + str(status.percentage) + '%. Status: ' + status.skillStatus
        rospy.loginfo(info)
        return info
