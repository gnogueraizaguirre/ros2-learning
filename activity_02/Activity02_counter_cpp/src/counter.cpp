#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"
#include "std_msgs/msg/string.hpp"

     
class CounterNode : public rclcpp::Node 
{
public:
    CounterNode() : Node("counter_node"), counter_(0)
    {
        publisher_ = create_publisher<std_msgs::msg::String>("count",10); //Topic for the count
        subscriber_ = create_subscription<std_msgs::msg::Int32>(
            "numbers",
            10,
            std::bind(&CounterNode::numbers_callback,
            this,
            std::placeholders::_1)
        );
        RCLCPP_INFO(get_logger(), "Counter Node has started");
    }
 
private:
    void numbers_callback(const std_msgs::msg::Int32::SharedPtr number){
        RCLCPP_INFO(get_logger(), "Number received: %d", number->data);
        counter_ += number->data;
        auto msg = std_msgs::msg::String();
        msg.data = "Current count: " + std::to_string(counter_);
        publisher_->publish(msg);
    }
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr subscriber_;
    int counter_;

};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<CounterNode>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

