#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"


class MyNode : public rclcpp::Node {
    public:
        MyNode() : Node("my_cpp_node"), counter_(0){
            RCLCPP_INFO(get_logger(), "hi from a class");
            timer_ = create_wall_timer(std::chrono::seconds(1), 
                                        std::bind(&MyNode::timer_callback,this));
        }
    private:
        void timer_callback(){
            RCLCPP_INFO(get_logger(), "Time %d",counter_);
            counter_++;
        }
        rclcpp::TimerBase::SharedPtr timer_;
        int counter_;
}; // Important semi-colon

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNode>(); //Creation of the node
    rclcpp::spin(node);                     // wheeee
    rclcpp::shutdown();
    return 0;
}