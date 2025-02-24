import launch
import launch_ros

def generate_launch_description():
  action_declare_face_locations_model = launch.actions.DeclareLaunchArgument('face_locations_model', default_value='cnn')
  action_node_face_detect = launch_ros.actions.Node(
    package='demo_python_service',
    executable='face_detect_node',
    parameters=[{'face_locations_model': launch.substitutions.LaunchConfiguration('face_locations_model', default='hog')}],
    output='log',
  )
  action_node_face_detect_client = launch_ros.actions.Node(
    package='demo_python_service',
    executable='face_detect_client_node',
    output='screen',
  )
  launch_description = launch.LaunchDescription([
    action_declare_face_locations_model,
    action_node_face_detect,
    action_node_face_detect_client,
  ])
  return launch_description