import launch
import launch.actions
import launch.substitutions
import launch_ros.actions


def generate_launch_description():
    return launch.LaunchDescription([
	launch_ros.actions.Node(
		package='main_package', executable='talker', output='screen',
		name=['talker']),
	launch_ros.actions.Node(
		package='main_package', executable='listener', output='screen',
		name=['listener']),
	launch_ros.actions.Node(
		package='main_package', executable='webcam', output='screen',
		name=['webcam']),
	launch_ros.actions.Node(
		package='main_package', executable='road-sign-recognition', output='screen',
		name=['road-sign-recognition']),
    ])
