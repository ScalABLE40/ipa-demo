import rospy
import actionlib
from sensor_msgs.msg import JointState
from moveit_msgs.srv import GetCartesianPath, GetCartesianPathRequest 
from moveit_msgs.msg import ExecuteTrajectoryAction, ExecuteTrajectoryGoal
from move_to_skill_msgs.msg import MoveToSkillAction, MoveToSkillResult, MoveToSkillFeedback

def RequestPlan(goal_pose):

    plan = None

    def get_last_joint_state():
        state = rospy.wait_for_message("/joint_states", JointState, timeout=5)
        return state

    def setup_request():
        request = GetCartesianPathRequest()
        request.group_name = "arm"
        request.waypoints = [goal_pose.pose]
        request.max_step = 0.01
        request.jump_threshold = 0.0
        request.avoid_collisions = True
        request.start_state.joint_state = get_last_joint_state()
        print(request)
        return request

    def plan():
        rospy.wait_for_service("/compute_cartesian_path")
        proxy = rospy.ServiceProxy("/compute_cartesian_path",GetCartesianPath)
        answer = proxy.call(setup_request())
        if(answer.error_code.val != 1):
            rospy.logerr("[GenerateCartesianPlan] Planning failed")
        plan = answer.solution
        fraction = answer.fraction
        if(fraction < 0.3):
            rospy.loginfo(plan)
            rospy.loginfo(fraction)
            rospy.logerr("[GenerateCartesianPlan] Planning fraction is different than 1")
            return False
        return True

    return plan(), plan

def ExecutePlan(plan):

    ac_ = actionlib.SimpleActionClient("/execute_trajectory", ExecuteTrajectoryAction)
    goal = ExecuteTrajectoryGoal()
    goal.trajectory = plan
    result = ac_.send_goal_and_wait(goal, execute_timeout=rospy.Duration(60.0))
    return result.error_code.val


class MoveToSkill(object):

    def __init__(self, action_name='MoveToSkill'):

        self.action_name = action_name
        self.move_to_skill_server = actionlib.SimpleActionServer(self.action_name, MoveToSkillAction, self.execute_skill, False)
        self.move_to_skill_server.start()
        self.percentage = 0
        self.outcomes = ["success", "failed"]

    def execute_skill(self, goal):
        result_, plan_ = RequestPlan(goal)
        if(result_ == False):
            self.aborted(outcome="failed")
        else:
            self.percentage = 50
            self.feedback("Plan Done")
            result_ = ExecutePlan(plan_)
            if(result_ == 1):
                self.percentage = 100
                self.feedback("Execution Done")
                self.success(outcome="success")
            else:
                self.aborted(outcome="failed")

        

    def feedback(self, status=None):
        feedback = MoveToSkillFeedback()
        feedback.percentage = self.percentage
        feedback.skillStatus = status if status else 'MoveToSkill Executing'
        self.move_to_skill_server.publish_feedback(feedback)
        self.log_info(feedback)

    def success(self, status=None, outcome='succeeded'):
        result_status = status if status else 'MoveToSkill executed successfully'
        result = self.result_constructor(percentage=100, status=result_status, outcome=outcome)
        self.move_to_skill_server.set_succeeded(result, result.skillStatus)

    def aborted(self, status=None, outcome='aborted'):
        result_status = status if status else 'MoveToSkill aborted'
        result = self.result_constructor(status=result_status, outcome=outcome)
        self.move_to_skill_server.set_aborted(result, result.skillStatus)

    def check_preemption(self):
        if self.move_to_skill_server.is_preempt_requested():
            result = self.result_constructor(status='MoveToSkill Preempted', outcome='preempted')
            self.move_to_skill_server.set_preempted(result, result.skillStatus)
            return

    def result_constructor(self, status, percentage=None, outcome=None):
        result = MoveToSkillResult()
        result.percentage = percentage if percentage else self.percentage
        result.skillStatus = status
        result.outcome = outcome
        self.log_info(result)
        return result

    @staticmethod
    def log_info(status):
        info = '[MoveToSkill] Percentage: ' + str(status.percentage) + '%. Status: ' + status.skillStatus
        rospy.loginfo(info)
        return info
