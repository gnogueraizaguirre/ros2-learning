#include "rclcpp/rclcpp.hpp"
#include "my_robot_interfaces/msg/hardware_status.hpp"

using namespace std::chrono_literals;
     
class HardwareStatusPublisher : public rclcpp::Node 
{
public:
    HardwareStatusPublisher() : Node("hardware_status_Publisher") {
        publisher_ = create_publisher<my_robot_interfaces::msg::HardwareStatus>("hardware_status",10);
        timer_ = create_wall_timer(1s, std::bind(&HardwareStatusPublisher::publishHardwareUpdate, this));
        RCLCPP_INFO(get_logger(), "Publisher started");
    }
 
private:
    void publishHardwareUpdate(){
        auto msg = my_robot_interfaces::msg::HardwareStatus();
        msg.temperature = 26.7;
        msg.motors_ready = true;
        msg.debug_message = "ground control to cpp. All good";
        publisher_->publish(msg);
    }

    rclcpp::Publisher<my_robot_interfaces::msg::HardwareStatus>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HardwareStatusPublisher>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

