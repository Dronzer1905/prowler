import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'prowler'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='Prowler Gazebo Sim joystick teleop and SLAM Toolbox package',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            # Format: '<executable_name> = <package_name>.<script_filename_without_py>:main'
            'joy_teleop = prowler.joy_teleop:main',
        ],
    },
)