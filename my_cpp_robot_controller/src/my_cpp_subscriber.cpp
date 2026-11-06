#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

class MyCPPSubscriber : public rclcpp::Node // MODIFY NAME
{
public:
    MyCPPSubscriber() : Node("time_Subscriber") // MODIFY NAME
    {
        subscriber_ = create_subscription<std_msgs::msg::String>(
            "time",
            10,
            std::bind(&MyCPPSubscriber::callbackMsgReceived, // This is hard to remember
            this, // this is this
            std::placeholders::_1)); // or using namespace std::placeholders you just write _1
        RCLCPP_INFO(get_logger(), "Subscriber has been started");
    }
 
private:
    void callbackMsgReceived(const std_msgs::msg::String::SharedPtr msg){
        RCLCPP_INFO(get_logger(), "%s", msg->data.c_str());
    }

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;
};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyCPPSubscriber>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

