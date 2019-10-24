import rospy
import actionlib

from operate_gripper_skill_msgs.msg import OperateGripperSkillAction, OperateGripperSkillResult, OperateGripperSkillFeedback
from ur_msgs.srv import SetIO, SetIORequest

class OperateGripperSkill(object):

    def __init__(self, action_name='OperateGripperSkill'):

        self.action_name = action_name
        self.operate_gripper_skill_server = actionlib.SimpleActionServer(self.action_name, OperateGripperSkillAction, self.execute_skill, False)
        self.operate_gripper_skill_server.start()
        self.percentage = 0
        self.outcomes = ["success", "failed"]

    def execute_skill(self, goal):
        
        rospy.sleep(1.0) #We don't know 
        request = SetIORequest()
        request.fun = 1
        request.state = 1
        service = rospy.ServiceProxy("/ur_hardware_interface/set_io", SetIO)
        if goal.close:
            request.pin = 0
        else:
            request.pin = 1

        answer = service.call(request)
        print(answer)
        if(answer.success == False):
            self.aborted("failed")
        rospy.sleep(0.5)
        request.state = 0
        answer = service.call(request)
        if(answer.success == False):
            self.aborted("failed")
        self.success("success")
        rospy.sleep(0.5)


    def feedback(self, status=None):
        feedback = OperateGripperSkillFeedback()
        feedback.percentage = self.percentage
        feedback.skillStatus = status if status else 'OperateGripperSkill Executing'
        self.operate_gripper_skill_server.publish_feedback(feedback)
        self.log_info(feedback)

    def success(self, status=None, outcome='succeeded'):
        result_status = status if status else 'OperateGripperSkill executed successfully'
        result = self.result_constructor(percentage=100, status=result_status, outcome=outcome)
        self.operate_gripper_skill_server.set_succeeded(result, result.skillStatus)

    def aborted(self, status=None, outcome='aborted'):
        result_status = status if status else 'OperateGripperSkill aborted'
        result = self.result_constructor(status=result_status, outcome=outcome)
        self.operate_gripper_skill_server.set_aborted(result, result.skillStatus)

    def check_preemption(self):
        if self.operate_gripper_skill_server.is_preempt_requested():
            result = self.result_constructor(status='OperateGripperSkill Preempted', outcome='preempted')
            self.operate_gripper_skill_server.set_preempted(result, result.skillStatus)
            return

    def result_constructor(self, status, percentage=None, outcome=None):
        result = OperateGripperSkillResult()
        result.percentage = percentage if percentage else self.percentage
        result.skillStatus = status
        result.outcome = outcome
        self.log_info(result)
        return result

    @staticmethod
    def log_info(status):
        info = '[OperateGripperSkill] Percentage: ' + str(status.percentage) + '%. Status: ' + status.skillStatus
        rospy.loginfo(info)
        return info
