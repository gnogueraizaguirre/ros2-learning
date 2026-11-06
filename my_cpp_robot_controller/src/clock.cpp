#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include <chrono>
#include <ctime>
#include <iomanip>
#include <sstream>

using namespace std::chrono_literals;

class MyClock : public rclcpp::Node 
{
public:
    MyClock() : Node("Clock_Publisher") 
    {
        publisher_ = create_publisher<std_msgs::msg::String>("time",10);
        timer_ = create_wall_timer(1s,std::bind(&MyClock::publishTime,this));
        RCLCPP_INFO(get_logger(), "Clock started");
    }
 
private:
    void publishTime(){
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);

        std::stringstream ss;
        ss << std::put_time(std::localtime(&time), "%H:%M:%S");

        auto msg = std_msgs::msg::String();
        msg.data = ss.str();

        publisher_->publish(msg);
    }
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyClock>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}