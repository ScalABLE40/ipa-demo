## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    packages=['operate_gripper_skill', 'operate_gripper_skill_class'],
    package_dir={'': 'src'},
)

setup(**setup_args)