import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    prowler_share = get_package_share_directory('prowler')
    tb3_gazebo_share = get_package_share_directory('turtlebot3_gazebo')
    slam_toolbox_share = get_package_share_directory('slam_toolbox')

    slam_params_file = os.path.join(
        prowler_share, 'config', 'mapper_params_online_async.yaml'
    )

    set_tb3_model = SetEnvironmentVariable(
        name='TURTLEBOT3_MODEL',
        value=os.environ.get('TURTLEBOT3_MODEL', 'waffle')
    )

    # 1. Start TurtleBot3 World in Gazebo Sim (Harmonic)
    tb3_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(tb3_gazebo_share, 'launch', 'turtlebot3_world.launch.py')
        )
    )

    # 2. Start joy_node to read the Xbox controller
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'use_sim_time': True,
            'deadzone': 0.05,
            'autorepeat_rate': 20.0,
        }],
        output='screen'
    )

    # 3. Start your custom prowler joy_teleop node
    joy_teleop_node = Node(
        package='prowler',
        executable='joy_teleop',
        name='joy_teleop',
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    # 4. Start SLAM Toolbox (Online Async Mode with Lifecycle Autostart)
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_share, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'autostart': 'true',
            'slam_params_file': slam_params_file,
        }.items()
    )

    rviz_config_file = os.path.join(
        prowler_share, 'config', 'prowler_slam.rviz'
    )

    # 5. Start RViz2 with your saved layout
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        set_tb3_model,
        tb3_sim,
        joy_node,
        joy_teleop_node,
        slam_toolbox,
        rviz_node,
    ])