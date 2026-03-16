import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    base_path = '/home/anto/'
    scene_file = ('git_trade/ros2_coppelia_learning/coppeliasim_ws'
                  '/project1_coppelia_ros2_testing/vision_stream_restream.ttt')
    scene_file_path = os.path.join(base_path, scene_file)

    coppelia_sim = 'CoppeliaSim_Edu_V4_10/coppeliaSim.sh'
    coppelia_sim_path = os.path.join(base_path, coppelia_sim)

    launch_coppelia = ExecuteProcess(
        cmd=[coppelia_sim_path, scene_file_path],
        output='screen'
    )

    launch_grayscale_node = Node(
        package='color_to_grayscale_restreamer',
        namespace='grayscale_processor',
        executable='pub_grayscale',
        output='screen'
    )

    return LaunchDescription([
        launch_coppelia,
        launch_grayscale_node
    ])
