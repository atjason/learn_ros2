import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Fetch default path.
    urdf_tutorial_path = get_package_share_directory("fishbot")
    default_model_path = urdf_tutorial_path + "/urdf/fishbot.urdf.xacro"
    # default_rviz_path = urdf_tutorial_path + '/config/display_robot_model.rviz'
    default_gazebo_world_path = urdf_tutorial_path + "/world/custom_room.world"

    # Declare launch parameter.
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name="model",
        default_value=str(default_model_path),
        description="URDF absolute path.",
    )
    # Generate new parameter based on model.
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(
            ["xacro ", launch.substitutions.LaunchConfiguration("model")],
        ),
        value_type=str,
    )
    robot_state_publisher_node = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )

    # Include another launch file view `IncludeLaunchDescription`
    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            [get_package_share_directory("gazebo_ros"), "/launch", "/gazebo.launch.py"]
        ),
        launch_arguments=[("world", default_gazebo_world_path), ("verbose", "true")],
    )

    # Load gazebo robot.
    action_spawn_entity = launch_ros.actions.Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "/robot_description", "-entity", "fishbot"],
    )
    # joint_state_publisher_node = launch_ros.actions.Node(
    #   package='joint_state_publisher',
    #   executable='joint_state_publisher',
    # )
    # rviz_node = launch_ros.actions.Node(
    #   package='rviz2',
    #   executable='rviz2',
    #   arguments=['-d', default_rviz_path],
    # )

    # 加载并激活 fishbot_joint_state_broadcaster 控制器
    load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "fishbot_joint_state_broadcaster",
        ],
        output="screen",
    )

    # 加载并激活 fishbot_effort_controller 控制器
    # load_fishbot_effort_controller = launch.actions.ExecuteProcess(
    #     cmd=[
    #         "ros2",
    #         "control",
    #         "load_controller",
    #         "--set-state",
    #         "active",
    #         "fishbot_effort_controller",
    #     ],
    #     output="screen",
    # )

    load_fishbot_diff_drive_controller = launch.actions.ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "fishbot_diff_drive_controller",
        ],
        output="screen",
    )

    return launch.LaunchDescription(
        [
            action_declare_arg_mode_path,
            # joint_state_publisher_node,
            robot_state_publisher_node,
            action_launch_gazebo,
            action_spawn_entity,
            # 事件动作，当加载机器人结束后执行
            launch.actions.RegisterEventHandler(
                event_handler=launch.event_handlers.OnProcessExit(
                    target_action=action_spawn_entity,
                    on_exit=[load_joint_state_controller],
                )
            ),
            # launch.actions.RegisterEventHandler(
            #     event_handler=launch.event_handlers.OnProcessExit(
            #         target_action=load_joint_state_controller,
            #         on_exit=[load_fishbot_effort_controller],
            #     )
            # ),
            launch.actions.RegisterEventHandler(
                event_handler=launch.event_handlers.OnProcessExit(
                    target_action=load_joint_state_controller,
                    on_exit=[load_fishbot_diff_drive_controller],
                )
            ),
            # rviz_node,
        ]
    )
