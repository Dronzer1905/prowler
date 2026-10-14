#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import TwistStamped

class teleop(Node):
    def __init__(self):
        super().__init__('joy_teleop')

        #xbox joystick params
        self.linear_axis=1
        self.angular_axis=0
        self.turbo_button=5

        #velocity limits
        self.max_linear_vel=1
        self.turbo_linear_vel=2
        self.max_angular_vel=1.2
        self.deadzone=0.08

        self.joy_sub=self.create_subscription(Joy,'/joy', self.joy_callback,10)
        self.cmd_pub=self.create_publisher(TwistStamped,'/cmd_vel',10)

        self.get_logger().info("prowler teleopration started")

    def apply_deadzone(self,value:float)-> float:
        if abs(value)<self.deadzone:
            return 0.0
        else:
            return value

    def joy_callback(self, msg: Joy):
        if len(msg.axes)<=max(self.linear_axis, self.angular_axis):
            return
        
        raw_linear=self.apply_deadzone(msg.axes[self.linear_axis])
        raw_angular=self.apply_deadzone(msg.axes[self.angular_axis])

        is_turbo=(len(msg.buttons)>self.turbo_button and msg.buttons[self.turbo_button]==1)

        if is_turbo:
            linear_scale=self.turbo_linear_vel
        else:
            linear_scale=self.max_linear_vel


        cmd_msg= TwistStamped()
        cmd_msg.header.stamp=self.get_clock().now().to_msg()
        cmd_msg.header.frame_id='base_link'
        cmd_msg.twist.linear.x= raw_linear * linear_scale
        cmd_msg.twist.angular.z=raw_angular * self.max_angular_vel

        self.cmd_pub.publish(cmd_msg)


def main(args=None):
    rclpy.init(args=args)
    node=teleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()