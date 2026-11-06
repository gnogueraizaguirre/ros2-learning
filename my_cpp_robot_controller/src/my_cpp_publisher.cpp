#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class MyCppPublisher: public rclcpp::Node
{
public:
    MyCppPublisher() : Node("MyCppPublisher"), robot_name_("SPD-1")
    {
        publisher_ = create_publisher<std_msgs::msg::String>("news",10); // starts the topic
        timer_ = create_wall_timer(0.5s,std::bind(&MyCppPublisher::publishNews, this)); // bruh
        RCLCPP_INFO(get_logger(), "Topic started"); //why the fuck are some of these in all caps
    }
 
private:
    void publishNews(){
        auto msg = std_msgs::msg::String();
        msg.data = std::string("Hi, this is ") + robot_name_;
        publisher_->publish(msg); // Arrow
    }
    std::string robot_name_;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;  // This creates the publisher
    rclcpp::TimerBase::SharedPtr timer_;
};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyCppPublisher>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

