#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using namespace std::chrono_literals;
using namespace std::placeholders;
     
class AddTwoIntsClientNode : public rclcpp::Node{
public:
    AddTwoIntsClientNode() : Node("AddTwoInts_Client_CPP") 
    {
        client_ = create_client<example_interfaces::srv::AddTwoInts>("AddTwoInts_CPP");
    }

    void callAddTwoInts(int a, int b){
        while (!client_->wait_for_service(1s)){
            RCLCPP_WARN(get_logger(), "Waiting for service...");
        }

        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a = a;
        request->b = b;

        client_->async_send_request(request, std::bind(&AddTwoIntsClientNode::callbackAddTwoIntResponse, this, _1));
    }
 
private:
    void callbackAddTwoIntResponse(rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future){
        auto response = future.get();
        RCLCPP_INFO(get_logger(), "Sum: %d", int(response->sum));
    }
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
};
 
int main(int argc, char **argv){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AddTwoIntsClientNode>(); 
    node->callAddTwoInts(86,65);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
