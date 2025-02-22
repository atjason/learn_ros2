#include <QApplication>
#include <QLabel>
#include <QString>
#include "rclcpp/rclcpp.hpp"
#include "status_interfaces/msg/system_status.hpp"

using SystemStatus = status_interfaces::msg::SystemStatus;

class SysStatusDisplay: public rclcpp::Node {
    public:
        SysStatusDisplay(): Node("sys_status_display") {
            subscription = this->create_subscription<SystemStatus>(
                "sys_status", 10, [&](const SystemStatus::SharedPtr msg) -> void {
                    label->setText(get_qstr_from_msg(msg));
                }
            );
            label = new QLabel(get_qstr_from_msg(std::make_shared<SystemStatus>()));
            label->show();
        }
    
        QString get_qstr_from_msg(const SystemStatus::SharedPtr msg) {
            std::stringstream show_str;
            show_str
                << '=================================\n'
                << 'Date:\t' << msg->stamp.sec << '\ts\n'
                << 'CPU:\t' << msg->cpu_percent << '\t%\n';
            return QString::fromStdString(show_str.str());
        } 
    
    private:
        rclcpp::Subscription<SystemStatus>::SharedPtr subscription;
        QLabel* label;
};

int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);

    auto node = std::make_shared<SysStatusDisplay>();
    std::thread spin_thread([&]() -> void { rclcpp::spin(node); });
    spin_thread.detach();
    
    app.exec();
    rclcpp::shutdown();
    return 0;
}