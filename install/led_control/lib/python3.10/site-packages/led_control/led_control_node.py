import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class LEDControlNode(Node):
    def __init__(self):
        super().__init__('led_control_node')
        self.subscription = self.create_subscription(
            String,
            'led_command',
            self.listener_callback,
            10)
        self.serial_port = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.get_logger().info('LED Control Node has been started.')

    def listener_callback(self, msg):
        command = msg.data.lower()
        if command == 'on':
            self.serial_port.write(b'ON\n')
            self.get_logger().info('Turning LED ON')
        elif command == 'off':
            self.serial_port.write(b'OFF\n')
            self.get_logger().info('Turning LED OFF')
        else:
            self.get_logger().warn('Unknown command')

def main(args=None):
    rclpy.init(args=args)
    node = LEDControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

