#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"
#include "std_msgs/msg/string.hpp"
#include "example_interfaces/srv/set_bool.hpp"

using namespace std::placeholders;
     
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
        reset_counter_ = create_service<example_interfaces::srv::SetBool>("ResetCounter", std::bind(&CounterNode::resetCounterCallback, this, _1,_2));
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

    void resetCounterCallback(const example_interfaces::srv::SetBool::Request::SharedPtr request,
                              const example_interfaces::srv::SetBool::Response::SharedPtr response){
        if (request->data == true){
            counter_ = 0;
            response->success =1;
            response->message = "Counter restarted successfully";
        }
        else{
            response->success =0;
            response->message = "Counter not restarted";
        }
        RCLCPP_INFO(get_logger(), "Request received: %d", int(request->data));
    }
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::Subscription<std_msgs::msg::Int32>::SharedPtr subscriber_;
    rclcpp::Service<example_interfaces::srv::SetBool>::SharedPtr reset_counter_;
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

