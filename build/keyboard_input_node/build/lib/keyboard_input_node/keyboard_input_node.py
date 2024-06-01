import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import sys
import select
import termios
import tty

class KeyboardInputNode(Node):
    def __init__(self):
        super().__init__('keyboard_input_node')
        self.publisher = self.create_publisher(String, 'led_command', 10)
        self.get_logger().info('Keyboard Input Node has been started.')

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
        return key

    def publish_command(self, command):
        msg = String()
        msg.data = command
        self.publisher.publish(msg)
        self.get_logger().info(f'Published command: {command}')

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardInputNode()
    try:
        while rclpy.ok():
            key = node.get_key()
            if key == 'o':
                node.publish_command('on')
            elif key == 'f':
                node.publish_command('off')
            elif key == '\x03':  # Ctrl+C to exit
                break
    except Exception as e:
        node.get_logger().error(f'Exception: {str(e)}')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

