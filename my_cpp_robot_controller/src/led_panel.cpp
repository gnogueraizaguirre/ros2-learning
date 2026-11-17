#include "rclcpp/rclcpp.hpp"
#include <vector>
#include "my_robot_interfaces/msg/led_panel.hpp"
#include "my_robot_interfaces/srv/switch.hpp"

using namespace std::chrono_literals;
     
class LedPanelNode : public rclcpp::Node 
{
public:
    LedPanelNode() : Node("led_panel") {
        declare_parameter<std::vector<bool>>("led_states", {false,false,false});  // In case i want to start it with other leds, for some reason
        led_panel_ = get_parameter("led_states").as_bool_array();
        led_panel_state_ = create_publisher<my_robot_interfaces::msg::LedPanel>("led_panel_state", 10);
        led_panel_service_ = create_service<my_robot_interfaces::srv::Switch>("switch_led_panel", std::bind(&LedPanelNode::switch_led_panel_callback, 
                                            this, std::placeholders::_1, std::placeholders::_2));
        timer_ = create_wall_timer(1s, std::bind(&LedPanelNode::publish_led_panel_state, this));
    }   
 
private:
    void switch_led_panel_callback( const my_robot_interfaces::srv::Switch::Request::SharedPtr request,
                                    const my_robot_interfaces::srv::Switch::Response::SharedPtr){
        if (request->led_number < 0 || request->led_number > 2){
            RCLCPP_INFO(get_logger(), "Received led index out of bounds");
            return;
        }
                                     
        led_panel_[request->led_number] = request->status; // i should really add comments to some of this stuff
        RCLCPP_INFO(get_logger(), "Received request to switch led %d to state %d", request->led_number, request->status);
    }
    void publish_led_panel_state(){
        auto msg = my_robot_interfaces::msg::LedPanel();
        msg.lights = led_panel_;
        led_panel_state_->publish(msg);
    }
    
    std::vector<bool> led_panel_;
    rclcpp::Publisher<my_robot_interfaces::msg::LedPanel>::SharedPtr led_panel_state_;
    rclcpp::Service<my_robot_interfaces::srv::Switch>::SharedPtr led_panel_service_;
    rclcpp::TimerBase::SharedPtr timer_;
};
 
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LedPanelNode>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

