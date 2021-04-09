colcon build --packages-select main_package
colcon build --packages-select my_robot_interfaces
colcon build --packages-select vision_msgs
colcon build --packages-select object_msgs
. install/setup.bash
